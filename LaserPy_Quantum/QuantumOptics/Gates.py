from __future__ import annotations

from numpy import (
    ndarray,
    array,
    cos, sin, exp, 
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
    def Measure(target: Photon, shots: int = 1):
        if(shots <= 0): raise ValueError("shots cannot be less than 1.")

        QE = target.qubit()
        return QE.quantum_state._measure_gate(target.qubit_index, shots)

    @staticmethod
    def Measure_All(target: Photon, shots: int = 1):
        if(shots <= 0): raise ValueError("shots cannot be less than 1.")

        QE = target.qubit()
        return QE.quantum_state._measure_all_gate(shots)

    @staticmethod
    def I(target: Photon) -> None:
        """Identity gate: |Ψ> -> |Ψ>"""
        matrix = array([[1, 0], 
                        [0, 1]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def X(target: Photon) -> None:
        """Pauli-X gate (Bit-flip): |0> -> |1> and |1> -> |0>"""
        matrix = array([[0, 1], 
                        [1, 0]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Y(target: Photon) -> None:
        """Pauli-Y gate: |0> -> i|1> and |1> -> -i|0>"""
        matrix = array([[0, -1j], 
                        [1j, 0]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Z(target: Photon) -> None:
        """Pauli-Z gate (Phase-flip): |0> -> |0> and |1> -> -|1>"""
        matrix = array([[1, 0], 
                        [0, -1]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Rx(target: Photon, theta: float) -> None:
        """Rotation around the X-axis."""
        matrix = array([[cos(theta/2), -1j * sin(theta/2)],
                        [-1j * sin(theta/2), cos(theta/2)]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Ry(target: Photon, theta: float) -> None:
        """Rotation around the Y-axis."""
        matrix = array([[cos(theta/2), -sin(theta/2)],
                        [sin(theta/2), cos(theta/2)]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def Rz(target: Photon, theta: float) -> None:
        """Rotation around the Z-axis."""
        matrix = array([[exp(-1j * theta/2), 0],
                        [0, exp(1j * theta/2)]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def P(target: Photon, theta: float) -> None:
        """Phase shift: |1> to e^{i*theta}|1>."""
        matrix = array([[1, 0],
                        [0, exp(1j * theta)]], dtype=complex)
        Gates._gate(matrix, target)

    @staticmethod
    def H(target: Photon) -> None:
        """Hadamard gate: |0> -> |+> and |1> -> |->"""
        matrix = array([[1,  1], 
                        [1, -1]], dtype=complex) / sqrt(2)
        Gates._gate(matrix, target)

    @staticmethod
    def U(target: Photon, theta: float, phi: float, lmbda: float) -> None:
        """Universal Rotation gate"""
        matrix = array([[cos(theta / 2),  -exp(1j * lmbda) * sin(theta / 2)], 
                        [exp(1j * phi) * sin(theta / 2), exp(1j * (phi + lmbda)) * cos(theta / 2)]], dtype=complex)
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

    @staticmethod
    def CZ(target: Photon, control: Photon) -> None:
        """CZ gate: |11> -> -|11>"""
        cz_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1]
        ], dtype=complex)
        Gates._gate(cz_matrix, target, control)

    @staticmethod
    def CPHASE(target: Photon, control: Photon, theta: float) -> None:
        """Controlled Phase Shift gate: |11> -> e^{i*theta}|11>"""
        cp_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, exp(1j * theta)]
        ], dtype=complex)
        Gates._gate(cp_matrix, control, target)

    @staticmethod
    def SWAP(target: Photon, control: Photon) -> None:
        """Swap gate: |i...j> -> |j...i>"""
        if(target is control): return # No self swap

        swap_matrix = array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ], dtype=complex)
        Gates._gate(swap_matrix, target, control)