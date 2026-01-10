from __future__ import annotations

from .QuantumState import QuantumState

class QuantumEntangler:
    def __init__(self, photons: tuple[Photon,...], quantum_state: QuantumState|None= None, sync= True) -> None:
        self.photons: tuple[Photon,...] = photons
        self.quantum_state = quantum_state if(quantum_state) else QuantumState(len(photons))

        if sync: self.sync_qubits()

    def __repr__(self) -> str:
        string = "QuantumEntangler:\n"
        for photon in self.photons:
            string += f"photon:{photon.photon_id} qubit:{photon.qubit_index}\n"
        string += str(self.quantum_state)
        return string
    
    def __add__(self, other: QuantumEntangler) -> QuantumEntangler:
        if not set(self.photons).isdisjoint(other.photons):
            print("DEBUG: Quantum States are already entangled.\n")
            return self

        photons = self.photons + other.photons
        quantum_state = self.quantum_state + other.quantum_state

        result = QuantumEntangler(photons, quantum_state)
        return result

    def sync_qubits(self):
        for idx, photon in enumerate(self.photons):
            photon.quantum_entangler = self
            photon.qubit_index = idx

    # def __del__(self):
    #     print(f"DEBUG: QE id:{id(self)} has been destroyed.")

from ..Photon import Photon