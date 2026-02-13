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
    def __qubits_check(qubits: tuple[Photon, ...]):
        if(len(set(qubits)) != len(qubits)):
            raise IndexError(f"{qubits!r} cannot contain duplicates.")

    @staticmethod
    def _n_qubit_gate(gate_name: str, matrix: ndarray, qubits: tuple[Photon, ...]):
        Gates.__qubits_check(qubits)
        
        QE = qubits[-1].qubit()
        qubit_idx = []
        for qubit in qubits:
            if QE is not qubit.qubit(): 
                raise AssertionError(f"{qubits[-1]!r} is not entangled with {qubit!r}.")
            qubit_idx.append(qubit.qubit_index)

        return QE.apply_gate(gate_name, tuple(qubit_idx))._n_qubit_gate(matrix, tuple(qubit_idx))

    @staticmethod
    def _gate(gate_name: str, matrix: ndarray, target: Photon, control1: Photon|None = None, control2: Photon|None = None):        
        # Ensure the target has an entangler
        QE = target.qubit()
        
        if control1 and control2:
            Gates.__qubits_check((control1, control2, target))

            # Ensure the control has an entangler and are in same state            
            if QE is not control1.qubit(): raise AssertionError(f"{target!r} is not entangled with {control1!r}.")
            elif QE is not control2.qubit(): raise AssertionError(f"{target!r} is not entangled with {control2!r}.")

            # Apply the 3-qubit gate
            qubit_idx = (target.qubit_index, control1.qubit_index, control2.qubit_index)
            QE.apply_gate(gate_name, qubit_idx)._triple_qubit_gate(matrix, *qubit_idx)
        elif control1:
            Gates.__qubits_check((control1, target))

            # Ensure the control has an entangler and are in same state            
            if QE is not control1.qubit(): raise AssertionError(f"{target!r} is not entangled with {control1!r}.") 
            
            # Apply the 2-qubit gate
            qubit_idx = (target.qubit_index, control1.qubit_index)
            QE.apply_gate(gate_name, qubit_idx)._double_qubit_gate(matrix, *qubit_idx)
        else:
            # Apply the 1-qubit gate
            QE.apply_gate(gate_name, (target.qubit_index,))._single_qubit_gate(matrix, target.qubit_index)

############################################################################

    @staticmethod
    def Measure(target: Photon, shots: int = 1):
        if(shots <= 0): raise ValueError("shots cannot be less than 1.")

        QE = target.qubit()
        return QE.apply_gate("M", (target.qubit_index,))._measure_gate(target.qubit_index, shots)

    @staticmethod
    def Measure_All(target: Photon, shots: int = 1):
        if(shots <= 0): raise ValueError("shots cannot be less than 1.")

        QE = target.qubit()
        return QE.apply_gate("MA")._measure_all_gate(shots)

############################################################################

    @staticmethod
    def I(target: Photon) -> None:
        """Identity gate: |Ψ> -> |Ψ>"""
        matrix = array([[1, 0], 
                        [0, 1]], dtype=complex)
        Gates._gate(f"i", matrix, target)

    @staticmethod
    def X(target: Photon) -> None:
        """Pauli-X gate (Bit-flip): |0> -> |1> and |1> -> |0>"""
        matrix = array([[0, 1], 
                        [1, 0]], dtype=complex)
        Gates._gate(f"x", matrix, target)

    @staticmethod
    def Y(target: Photon) -> None:
        """Pauli-Y gate: |0> -> i|1> and |1> -> -i|0>"""
        matrix = array([[0, -1j], 
                        [1j, 0]], dtype=complex)
        Gates._gate(f"y", matrix, target)

    @staticmethod
    def Z(target: Photon) -> None:
        """Pauli-Z gate (Phase-flip): |0> -> |0> and |1> -> -|1>"""
        matrix = array([[1, 0], 
                        [0, -1]], dtype=complex)
        Gates._gate(f"y", matrix, target)

    @staticmethod
    def H(target: Photon) -> None:
        """Hadamard gate: |0> -> |+> and |1> -> |->"""
        matrix = array([[1,  1], 
                        [1, -1]], dtype=complex) / sqrt(2)
        Gates._gate(f"h", matrix, target)

    @staticmethod
    def Rx(target: Photon, theta: float) -> None:
        """Rotation around the X-axis."""
        matrix = array([[cos(theta/2), -1j * sin(theta/2)],
                        [-1j * sin(theta/2), cos(theta/2)]], dtype=complex)
        Gates._gate(f"rx[{theta:.4f}]", matrix, target)

    @staticmethod
    def Ry(target: Photon, theta: float) -> None:
        """Rotation around the Y-axis."""
        matrix = array([[cos(theta/2), -sin(theta/2)],
                        [sin(theta/2), cos(theta/2)]], dtype=complex)
        Gates._gate(f"ry[{theta:.4f}]", matrix, target)

    @staticmethod
    def Rz(target: Photon, theta: float) -> None:
        """Rotation around the Z-axis."""
        matrix = array([[exp(-1j * theta/2), 0],
                        [0, exp(1j * theta/2)]], dtype=complex)
        Gates._gate(f"rz[{theta:.4f}]", matrix, target)

    @staticmethod
    def P(target: Photon, theta: float) -> None:
        """Phase shift: |1> to e^{i*theta}|1>."""
        matrix = array([[1, 0],
                        [0, exp(1j * theta)]], dtype=complex)
        Gates._gate(f"p[{theta:.4f}]", matrix, target)

    @staticmethod
    def U(target: Photon, theta: float, phi: float, lmbda: float) -> None:
        """Universal Rotation gate"""
        matrix = array([[cos(theta / 2),  -exp(1j * lmbda) * sin(theta / 2)], 
                        [exp(1j * phi) * sin(theta / 2), exp(1j * (phi + lmbda)) * cos(theta / 2)]], dtype=complex)
        Gates._gate(f"u[{theta:.4f},{phi:.4f},{lmbda:.4f}]", matrix, target)

############################################################################

    @staticmethod
    def CNOT(target: Photon, control: Photon) -> None:
        """CNOT gate: |T> -> X|C>"""
        cnot_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
        Gates._gate(f"cx", cnot_matrix, target, control)

    @staticmethod
    def CZ(target: Photon, control: Photon) -> None:
        """CZ gate: |11> -> -|11>"""
        cz_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1]
        ], dtype=complex)
        Gates._gate(f"cz", cz_matrix, target, control)

    @staticmethod
    def SWAP(target: Photon, control: Photon) -> None:
        """Swap gate: |i...j> -> |j...i>"""
        swap_matrix = array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ], dtype=complex)
        Gates._gate(f"swap", swap_matrix, target, control)

    @staticmethod
    def CPHASE(target: Photon, control: Photon, theta: float) -> None:
        """Controlled Phase Shift gate: |11> -> e^{i*theta}|11>"""
        cp_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, exp(1j * theta)]
        ], dtype=complex)
        Gates._gate(f"cp[{theta:.4f}]", cp_matrix, target, control)

    @staticmethod
    def CCNOT(target: Photon, control1: Photon, control2: Photon) -> None:
        """CCNOT gate"""
        ccnot_matrix = array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ], dtype=complex)
        Gates._gate(f"ccnot", ccnot_matrix, target, control1, control2)
