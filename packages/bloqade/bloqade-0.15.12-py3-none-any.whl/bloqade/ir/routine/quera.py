from collections import OrderedDict
from pydantic.v1.dataclasses import dataclass
import json

from bloqade.builder.typing import LiteralType
from bloqade.ir.routine.base import RoutineBase, __pydantic_dataclass_config__
from bloqade.submission.quera import QuEraBackend
from bloqade.submission.mock import MockBackend
from bloqade.submission.load_config import load_config
from bloqade.task.batch import RemoteBatch
from bloqade.task.quera import QuEraTask

from beartype.typing import Tuple, Union, Optional
from beartype import beartype


@dataclass(frozen=True, config=__pydantic_dataclass_config__)
class QuEraServiceOptions(RoutineBase):
    @beartype
    def device(self, config_file: Optional[str], **api_config):
        if config_file is not None:
            with open(config_file, "r") as f:
                api_config = {**json.load(f), **api_config}

        backend = QuEraBackend(**api_config)

        return QuEraHardwareRoutine(self.source, self.circuit, self.params, backend)

    def aquila(self) -> "QuEraHardwareRoutine":
        backend = QuEraBackend(**load_config("Aquila"))
        return QuEraHardwareRoutine(self.source, self.circuit, self.params, backend)

    def cloud_mock(self) -> "QuEraHardwareRoutine":
        backend = QuEraBackend(**load_config("Mock"))
        return QuEraHardwareRoutine(self.source, self.circuit, self.params, backend)

    @beartype
    def mock(
        self, state_file: str = ".mock_state.txt", submission_error: bool = False
    ) -> "QuEraHardwareRoutine":
        backend = MockBackend(state_file=state_file, submission_error=submission_error)
        return QuEraHardwareRoutine(self.source, self.circuit, self.params, backend)


@dataclass(frozen=True, config=__pydantic_dataclass_config__)
class QuEraHardwareRoutine(RoutineBase):
    backend: Union[QuEraBackend, MockBackend]

    def _compile(
        self,
        shots: int,
        args: Tuple[LiteralType, ...] = (),
        name: Optional[str] = None,
    ) -> RemoteBatch:
        from bloqade.compiler.passes.hardware import (
            analyze_channels,
            canonicalize_circuit,
            assign_circuit,
            validate_waveforms,
            generate_ahs_code,
            generate_quera_ir,
        )

        circuit, params = self.circuit, self.params
        capabilities = self.backend.get_capabilities()

        tasks = OrderedDict()

        for task_number, batch_params in enumerate(params.batch_assignments(*args)):
            assignments = {**batch_params, **params.static_params}
            final_circuit, metadata = assign_circuit(circuit, assignments)

            level_couplings = analyze_channels(final_circuit)
            final_circuit = canonicalize_circuit(final_circuit, level_couplings)

            validate_waveforms(level_couplings, final_circuit)
            ahs_components = generate_ahs_code(
                capabilities, level_couplings, final_circuit
            )

            task_ir = generate_quera_ir(ahs_components, shots).discretize(capabilities)

            tasks[task_number] = QuEraTask(
                None,
                self.backend,
                task_ir,
                metadata,
                ahs_components.lattice_data.parallel_decoder,
            )

        batch = RemoteBatch(source=self.source, tasks=tasks, name=name)

        return batch

    @beartype
    def run_async(
        self,
        shots: int,
        args: Tuple[LiteralType, ...] = (),
        name: Optional[str] = None,
        shuffle: bool = False,
        **kwargs,
    ) -> RemoteBatch:
        """
        Compile to a RemoteBatch, which contain
            QuEra backend specific tasks,
            and run_async through QuEra service.

        Args:
            shots (int): number of shots
            args (Tuple): additional arguments
            name (str): custom name of the batch
            shuffle (bool): shuffle the order of jobs

        Return:
            RemoteBatch

        """
        batch = self._compile(shots, args, name)
        batch._submit(shuffle, **kwargs)
        return batch

    @beartype
    def run(
        self,
        shots: int,
        args: Tuple[LiteralType, ...] = (),
        name: Optional[str] = None,
        shuffle: bool = False,
        **kwargs,
    ) -> RemoteBatch:
        batch = self.run_async(shots, args, name, shuffle, **kwargs)
        batch.pull()
        return batch

    @beartype
    def __call__(
        self,
        *args: LiteralType,
        shots: int = 1,
        name: Optional[str] = None,
        shuffle: bool = False,
        **kwargs,
    ) -> RemoteBatch:
        return self.run(shots, args, name, shuffle, **kwargs)
