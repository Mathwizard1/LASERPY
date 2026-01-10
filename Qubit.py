from LaserPy_Quantum import Photon
from LaserPy_Quantum.QuantumOptics.Gates import Gates

A = Photon()
B = Photon()
C = Photon()

#Gates.H(A)

def entangle(photon_tuple: tuple[Photon,...]):
    QE = photon_tuple[0].set_qubit()
    for photon in photon_tuple[1:]:
        QE = QE + photon.set_qubit()
entangle((A, B))

Gates.H(B)
Gates.Y(B)

print(B.quantum_entangler)

print(C.quantum_entangler)

