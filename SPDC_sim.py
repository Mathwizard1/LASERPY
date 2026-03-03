from LaserPy_Quantum import Clock
from LaserPy_Quantum import Connection, Simulator
from LaserPy_Quantum import (
    StaticWave,
    ArbitaryWaveGenerator
)
from LaserPy_Quantum import CurrentDriver
from LaserPy_Quantum import Laser

from LaserPy_Quantum.SpecializedComponents import SinglePhotonDetector

from LaserPy_Quantum.SpecializedComponents.PhotonPairGenerator import PhotonPairGeneratorCrystal
from LaserPy_Quantum.utils.RefractiveMaterials import Birefringent, SellmeierFormula

from numpy import pi

############################################################################
# Switch Laser Type

from LaserPy_Quantum.Constants import LaserPyConstants
LaserPyConstants.load_from_json("SPDC_Constants.json")

############################################################################

# Control Constants (all in SI units)
dt = 1e-12
t_unit = 1e-9
sampling_rate = 2

# Current Constants
I_th = 0.0178
MASTER_BASE_DC = 5 * I_th

# Steady above lasing current
mBase = StaticWave("mBase", MASTER_BASE_DC)

AWG = ArbitaryWaveGenerator()
AWG.set(mBase)

############################################################################

BBO = Birefringent(
    SellmeierFormula((2.7359,0.01878,0.01822,0.01354)),
    SellmeierFormula((2.3753,0.01224,0.01667,0.01516)),
    crystal_angle= 0.86,
    name="BBO"
)

SPDC = PhotonPairGeneratorCrystal(
    refractive_material= BBO,
    SPDC_type= 'II',
)

############################################################################

# best_angle = 0.0
# theta = 0.0
# while(theta < pi):
#     BBO.set(theta)
    
#     theta += pi / 20

# exit(0)

############################################################################

current_driver = CurrentDriver(AWG)
current_driver.set(mBase)

laser = Laser(name= "pump_laser")
SPD = SinglePhotonDetector()

simulator_clock = Clock(dt, sampling_rate)
simulator_clock.set(t_unit * 5)

simulator = Simulator(simulator_clock)

simulator.set((
    Connection(simulator_clock, current_driver),
    Connection(current_driver, laser),
    Connection(laser, SPD),
))

simulator.reset(True)

simulator.simulate()
time_data = simulator.get_data()

laser.display_data(time_data)
#SPD.display_data(time_data)
############################################################################
simulator.reset_data()

simulator_clock.set(t_unit * 10)

simulator.set((
    Connection(simulator_clock, current_driver),
    Connection(current_driver, laser),
    Connection(laser, SPDC),
))

simulator.reset(True)

simulator.simulate()
time_data = simulator.get_data()

#laser.display_data(time_data)
SPDC.display_data(time_data)

