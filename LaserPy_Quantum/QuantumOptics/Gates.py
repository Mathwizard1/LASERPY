from __future__ import annotations

from numpy import (
    ndarray,
    array, 
    sqrt,
)

from ..Photon import Photon

class Gates:
    @staticmethod
    def _gate(matrix: ndarray, target: Photon, control: Photon|None = None):
        QE = target.set_qubit()
        if(control):
            pass
        else:
            QE.quantum_state._single_qubit_gate(matrix, target.qubit_index)

    @staticmethod
    def I(target: 'Photon') -> None:
        """Identity gate: |Ψ> -> |Ψ>"""
        matrix = array([[1, 0], 
                        [0, 1]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def X(target: 'Photon') -> None:
        """Pauli-X gate (Bit-flip): |0> -> |1> and |1> -> |0>"""
        matrix = array([[0, 1], 
                        [1, 0]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Y(target: 'Photon') -> None:
        """Pauli-Y gate: |0> -> i|1> and |1> -> -i|0>"""
        matrix = array([[0, -1j], 
                        [1j, 0]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Z(target: 'Photon') -> None:
        """Pauli-Z gate (Phase-flip): |0> -> |0> and |1> -> -|1>"""
        matrix = array([[1, 0], 
                        [0, -1]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def H(target: 'Photon') -> None:
        """Hadamard gate: |0> -> |+> and |1> -> |->"""
        matrix = array([[1,  1], 
                        [1, -1]], dtype=complex) / sqrt(2)
        Gates._gate(matrix, target)

    @staticmethod
    def CNOT(target: Photon, control:Photon) -> None:
        pass