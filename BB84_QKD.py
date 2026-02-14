from LaserPy_Quantum import Clock
from LaserPy_Quantum import Connection, Simulator
from LaserPy_Quantum import (
    StaticWave, ArbitaryWaveGenerator
)
from LaserPy_Quantum import ModulationFunction, CurrentDriver
from LaserPy_Quantum import Laser

from LaserPy_Quantum import RandomNumSource
from LaserPy_Quantum import VariableOpticalAttenuator

from LaserPy_Quantum import AsymmetricMachZehnderInterferometer
from LaserPy_Quantum import (
    display_class_instances_data, 
    get_time_delay_phase_correction
)

import numpy as np

# Control Constants (all in SI units)
modulation_bits = [0] * 10
dt = 1e-12
t_unit = 1e-11
t_final = t_unit * len(modulation_bits) / 2
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

current_driver1 = CurrentDriver(AWG)
current_driver1.set(mBase)

master_laser = Laser(name= "master_laser")

simulator_clock = Clock(dt, sampling_rate)
simulator_clock.set(t_final)

simulator = Simulator(simulator_clock)

VOA = VariableOpticalAttenuator(5)

simulator.set((
    Connection(simulator_clock, current_driver1),
    Connection(current_driver1, master_laser),
    Connection(master_laser, VOA),
))

simulator.reset(True)

simulator.simulate()
time_data = simulator.get_data()

#display_class_instances_data((master_laser,), time_data)
print(np.mod(master_laser._simulation_data['phase'], np.pi * 2) - np.pi)

exit(code= 0)