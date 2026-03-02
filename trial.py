from LaserPy_Quantum.SpecializedComponents.PhotonPairGenerator import PhotonPairGeneratorCrystal
from LaserPy_Quantum.utils.RefractiveMaterials import Birefringent, SellmeierFormula
from LaserPy_Quantum.Photon import Photon

from LaserPy_Quantum.Constants import UniversalConstants
from numpy import pi

# deff = 2.2e-12
# Crystal_length = 2e-3


BBO = Birefringent(
    SellmeierFormula((2.7359,0.01878,0.01822,0.01354)),
    SellmeierFormula((2.3753,0.01224,0.01667,0.01516)),
    name="BBO"
)

SPDC = PhotonPairGeneratorCrystal(
    refractive_material= BBO,
    SPDC_type= 'II',
)

#print(BBO.n(810e-9, 'H'))
#exit()

############################################################################

pump = Photon(
    frequency = 2 * pi * UniversalConstants.C.value/ 405e-9,
    field = 3e4 + 0j,
    photon_number = 1e5
)

SPDC.simulate(pump)

