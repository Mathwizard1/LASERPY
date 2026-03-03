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

# QFT setup
def setup(photon_tuple: tuple[Photon,...]):
    Gates.H(photon_tuple[0])
    Gates.CNOT(photon_tuple[1], photon_tuple[0])
    
#setup(photons)
print(photons[0].quantum_entangler)

# QFT loop
for i in range(n_photons):
    Gates.H(photons[i])
    for j in range(i + 1, n_photons):
        Gates.CPHASE(photons[i], photons[j], pi / (2 ** i))

for i in range(n_photons):
    if(i != n_photons - i - 1):  
        Gates.SWAP(photons[i], photons[- i - 1])

print(photons[0].quantum_entangler)

results = Gates.Measure_All(photons[0])
print(results)