from __future__ import annotations

from numpy import (
    ndarray,
    array, kron, eye,
)

class QuantumState:
    def __init__(self, n: int, state: ndarray|None = None) -> None:
        self.n_qubits = n
        self._state: ndarray = array([1.0 + 0j] + [0.0 + 0j] * ((1 << n) - 1), dtype=complex) if(state is None) else state

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.n_qubits} qubits:\n" + str(self._state) + ")\n"

    def __add__(self, other: QuantumState) -> QuantumState:
        merged_n = self.n_qubits + other.n_qubits
        merged_state = kron(self._state, other._state)
        result = QuantumState(merged_n, merged_state)
        return result

    # def __del__(self):
    #     print(f"DEBUG: QS id:{id(self)} has been destroyed.")

    def _single_qubit_gate(self, matrix: ndarray, target: int):
        """Tensor: I(1..k-1) ⊗ G ⊗ I(k+1..n)"""
        i_left = eye(2**target)
        i_right = eye(2**(self.n_qubits - target - 1))
        operator = kron(kron(i_left, matrix), i_right)
        self._state = operator @ self._state

    def _double_qubit_gate(self, matrix: ndarray, target: int, control: int):
        pass

# class FullStateVector(QuantumState):
#     def __init__(self, n: int = 1, state: ndarray|None = None) -> None:
#         state = state if(state) else array([1.0 + 0j] + [0.0 + 0j] * ((1 << n) - 1), dtype=complex)

#         super().__init__(n, state)

#     def __add__(self, other: QuantumState) -> QuantumState:
#         merged_n = self.n_qubits + other.n_qubits
#         merged_state = kron(self._state, other._state)
#         result = QuantumState(merged_n, merged_state)
#         return result

#     def _single_qubit_gate(self, matrix: ndarray, target: int):
#         pass

#     def _double_qubit_gate(self, matrix: ndarray, control: int, target: int):
#         pass