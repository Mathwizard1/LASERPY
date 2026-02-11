from LaserPy_Quantum import Photon
from LaserPy_Quantum.QuantumOptics.Gates import Gates

from numpy import pi

# N-Qubit system
n_photons = 3

photon_list = []
for _ in range(n_photons):
    photon_list.append(Photon())

photons: tuple[Photon, ...] = tuple(photon_list)

def entangle(photon_tuple: tuple[Photon,...]):
    QE = photon_tuple[0].qubit()
    for photon in photon_tuple[1:]:
        QE = QE + photon.qubit()
entangle(photons)

print(photons[0].quantum_entangler)

Gates.H(photons[0])
#Gates.CNOT(C, A)

print(photons[0].quantum_entangler)

results = Gates.Measure_All(photons[-1], shots= 1024)
print(results)