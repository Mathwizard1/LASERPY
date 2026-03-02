from LaserPy_Quantum import Clock
from LaserPy_Quantum import Connection, Simulator
from LaserPy_Quantum import (
    StaticWave,
    ArbitaryWaveGenerator
)
from LaserPy_Quantum import CurrentDriver
from LaserPy_Quantum import Laser

from LaserPy_Quantum.SpecializedComponents.PhotonPairGenerator import PhotonPairGeneratorCrystal
from LaserPy_Quantum.utils.RefractiveMaterials import Birefringent, SellmeierFormula

# Control Constants (all in SI units)
dt = 1e-12
t_unit = 1e-9
t_final = t_unit * 10
sampling_rate = 2

RESET_MODE = True

# Current Constants
I_th = 0.0178
MASTER_BASE_DC = 1.4 * I_th

# Steady above lasing current
mBase = StaticWave("mBase", MASTER_BASE_DC)

AWG = ArbitaryWaveGenerator()
AWG.set(mBase)

############################################################################

BBO = Birefringent(
    SellmeierFormula((2.7359,0.01878,0.01822,0.01354)),
    SellmeierFormula((2.3753,0.01224,0.01667,0.01516)),
    name="BBO"
)

SPDC = PhotonPairGeneratorCrystal(
    refractive_material= BBO,
    SPDC_type= 'II',
)

############################################################################

current_driver = CurrentDriver(AWG)
current_driver.set(mBase)

laser = Laser(name= "pump_laser")

simulator_clock = Clock(dt, sampling_rate)
simulator_clock.set(t_final)

simulator = Simulator(simulator_clock)

############################################################################

simulator.set((
    Connection(simulator_clock, current_driver),
    Connection(current_driver, laser),
    Connection(laser, SPDC),
))

simulator.reset(True)

simulator.simulate()
time_data = simulator.get_data()

laser.display_data(time_data)

exit(code= 0)

