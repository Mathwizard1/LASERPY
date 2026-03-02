from __future__ import annotations

from LaserPy_Quantum.Photon import Photon

from .Entangler import QuantumStateModel, QuantumEntangler

class QuantumCircuit(QuantumEntangler):
    def __init__(self, photons: tuple[Photon, ...], quantum_state: QuantumStateModel | None = None, sync=True) -> None:
        super().__init__(photons, quantum_state, sync)

        self._gates_data: list[str] = []

    def __add__(self, other: QuantumEntangler) -> QuantumEntangler:
        return super().__add__(other)

    def apply_gate(self, gate_name: str, qubits: tuple[int, ...] | None = None) -> QuantumStateModel:
        return super().apply_gate(gate_name, qubits)