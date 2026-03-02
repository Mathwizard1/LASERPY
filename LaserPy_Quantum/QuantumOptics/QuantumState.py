from __future__ import annotations

from collections import Counter

from numpy import (
    random,

    ndarray,
    sqrt, zeros_like,
    array, kron, moveaxis,
)

class QuantumState:
    def __init__(self, n: int, state: ndarray|None = None) -> None:
        self.n_qubits = n
        self._state: ndarray = array([1.0 + 0j] + [0.0 + 0j] * ((1 << n) - 1), dtype=complex) if(state is None) else state

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.n_qubits} qubits):\n{str(self._state)}\n"

    def __add__(self, other: QuantumState) -> QuantumState:
        merged_n = self.n_qubits + other.n_qubits
        merged_state = kron(self._state, other._state)
        result = QuantumState(merged_n, merged_state)
        return result

    # def __del__(self):
    #     print(f"DEBUG: QS id:{id(self)} has been destroyed.")

    def _single_qubit_gate(self, matrix: ndarray, target: int):
        state = self._state.reshape([2] * self.n_qubits)
        state = moveaxis(state, target, 0)

        # 1-qubit reshape
        remainder_shape = state.shape[1:]
        state = state.reshape(2, -1)
        
        # Apply the 2x2 matrix: |ψ'⟩ = U|ψ⟩
        state = matrix @ state

        state = state.reshape((2,) + remainder_shape)
        self._state = moveaxis(state, 0, target).flatten()

    def _double_qubit_gate(self, matrix: ndarray, target: int, control: int):
        state = self._state.reshape([2] * self.n_qubits)
        state = moveaxis(state, (control, target), (0, 1))

        # 2-qubit reshape
        remainder_shape = state.shape[2:]
        state = state.reshape(4, -1)
        
        # Apply the 4x4 matrix: |ψ'⟩ = U|ψ⟩
        state = matrix @ state

        state = state.reshape((2, 2) + remainder_shape)
        self._state = moveaxis(state, (0, 1), (control, target)).flatten()

    def _triple_qubit_gate(self, matrix: ndarray, target: int, control1: int, control2: int):
        state = self._state.reshape([2] * self.n_qubits)
        state = moveaxis(state, (control1, control2, target), (0, 1, 2))

        # 3-qubit reshape
        remainder_shape = state.shape[3:]
        state = state.reshape(8, -1)

        # Apply 8x8 matrix: |ψ'⟩ = U|ψ⟩
        state = matrix @ state

        state = state.reshape((2, 2, 2) + remainder_shape)
        self._state = moveaxis(state, (0, 1, 2), (control1, control2, target)).flatten()

    def _n_qubit_gate(self, matrix: ndarray, qubits: tuple[int, ...]):
        n = len(qubits)
        order_qubits = range(n)

        state = self._state.reshape([2] * self.n_qubits)
        state = moveaxis(state, qubits, order_qubits)

        # n-qubit reshape
        remainder_shape = state.shape[n:]
        state = state.reshape(2 ** n, -1)

        # Apply (2^N)x(2^N) matrix: |ψ'⟩ = U|ψ⟩
        state = matrix @ state

        state = state.reshape((2,) * len(qubits) + remainder_shape)
        self._state = moveaxis(state, order_qubits, qubits).flatten()

############################################################################

    # TODO: Make Measurements module measure gate
    def _measure_gate(self, target: int, shots: int = 1) -> str | list[str]:
        return "Not implemented yet"
        # Sample and collapse
        outcomes: list[int] = []

        for _ in range(shots):
            # Compute fresh probabilities
            step = 1 << (target + 1)
            mask0 = ~(1 << target)
            mask1 = 1 << target

            probs_raw = array([
                sum(abs(self._state[mask0::step])**2),
                sum(abs(self._state[mask1::step])**2)
                ])

            probs = probs_raw / sum(probs_raw)

            # Sample
            k = random.choice([0, 1], p=probs)
            outcomes.append(int(k))

            # Collapse
            if k == 0:
                self._state[mask1::step] = 0.0 + 0j
            else:
                self._state[mask0::step] = 0.0 + 0j

            # Renormalize
            self._state *= 1.0 / sqrt(probs_raw[k])

        return list(map(str, outcomes))

    def _measure_all_gate(self, shots: int = 1) -> str | dict[str, int]:
        probs = abs(self._state) ** 2
        outcomes = random.choice(2 ** self.n_qubits, size=shots, p=probs)

        if shots == 1:
            k = outcomes[0]

            # Ordering based on qubit setup
            bitstring = format(k, f'0{self.n_qubits}b')           
            
            # Collapse
            self._state = zeros_like(self._state)
            self._state[k] = 1.0  
            return bitstring

        counts = Counter()
        for k in outcomes:
            bitstring = format(k, f'0{self.n_qubits}b')
            counts[bitstring] += 1
        return dict(counts)
