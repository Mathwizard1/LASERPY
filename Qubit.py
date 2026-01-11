from LaserPy_Quantum import Photon
from LaserPy_Quantum.QuantumOptics.Gates import Gates

A = Photon()
B = Photon()
C = Photon()

def entangle(photon_tuple: tuple[Photon,...]):
    QE = photon_tuple[0].qubit()
    for photon in photon_tuple[1:]:
        QE = QE + photon.qubit()
entangle((A, B, C))

Gates.H(A)
Gates.CNOT(B, A)
Gates.CNOT(C, A)

print(C.quantum_entangler)

