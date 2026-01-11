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
        # Ensure the target has an entangler
        QE = target.qubit()
        
        if control:
            # Ensure the control has an entangler and are in same state
            QE_control = control.qubit()
            
            if QE != QE_control: QE = QE + QE_control 
            
            # Apply the 2-qubit gate
            QE.quantum_state._double_qubit_gate(matrix, target.qubit_index, control.qubit_index)
        else:
            # Apply the 1-qubit gate
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
    def CNOT(target: Photon, control: Photon) -> None:
        """CNOT gate: |T> -> X|C>"""
        cnot_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
        Gates._gate(cnot_matrix, target, control)