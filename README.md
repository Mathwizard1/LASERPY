# LaserPy_Quantum

![LaserPy_Quantum](https://raw.githubusercontent.com/Mathwizard1/LaserPy_Quantum/refs/heads/main/LaserPy_Quantum/LaserPy_Quantum.png)

**LaserPy_Quantum** provides an intuitive interface for simulating complex laser interactions, current drivers, and interferometer setups, with plans to offload performance-critical components to Rust for high-speed numerical computations. A *high-level, open-source Python library designed for the theoretical simulation of laser systems* in quantum communication and cryptographic protocols.

### 🚀 Features

- High-Level API for constructing laser-based quantum system simulations.
- Support for arbitrary waveform generation (AWG) and current drivers.
- Simulation of master–slave laser - configurations with injection locking.
- Built-in support for asymmetric Mach–Zehnder interferometers (AMZI) and photon detectors.
- Clock-driven simulation engine for precise time-step control.
- Extensible architecture for future modules and Rust acceleration.

### 📖 Documentation

LaserPy_Quantum documentation on *[Read the docs](https://mathwizard1.github.io/LaserPy_Quantum/)*.

### 📦 Installation

- LaserPy_Quantum is now on *[pypi](https://pypi.org/project/LaserPy-Quantum/)*.
```bash
pip install LaserPy_Quantum
```

- Also, LaserPy_Quantum is under active development and welcomes opensource developers. Clone the repository locally:
```bash
git clone https://github.com/Mathwizard1/LaserPy_Quantum.git
cd LaserPy_Quantum
pip install -e .
```

Ensure you’re using Python 3.9+.

### 📝 Example Usage

Below is an example of using LaserPy_Quantum component and connection system with simulator:

```python
############################################################################
from LaserPy_Quantum import Clock
from LaserPy_Quantum import Connection, Simulator
from LaserPy_Quantum import StaticWave, ArbitaryWaveGenerator
from LaserPy_Quantum import CurrentDriver
from LaserPy_Quantum import Laser

############################################################################
dt = 1e-12
t_unit = 1e-9
t_final = 100 * t_unit
#sampling_rate = 2 * dt

# Current Constants
I_th = 0.0178
MASTER_BASE_DC = 1.4 * I_th

mBase = StaticWave("mBase", MASTER_BASE_DC)

AWG = ArbitaryWaveGenerator()
AWG.set(mBase)

############################################################################

current_driver1 = CurrentDriver(AWG)
current_driver1.set(mBase)

master_laser = Laser(name= "master_laser")

simulator_clock = Clock(dt)
simulator_clock.set(t_final)

simulator = Simulator(simulator_clock)

simulator.set((
    Connection(simulator_clock, current_driver1),
    Connection(current_driver1, master_laser),
))

simulator.reset(True)
```

### 🧠 Use Case: Laser simulations

LaserPy_Quantum’s current use case is simulating quantum key distribution (QKD) protocols using master–slave lasers with injection locking and interferometer-based detection.<br>
It allows researchers and engineers to prototype and test theoretical setups before implementing them in hardware.

### 🔧 Planned Features

- Rust-based backend for high-performance simulation.
- Expanded library of optical components (modulators, detectors, etc.).

#### TODO list

0) Do a _setup method specific to loading constants
1) global config singleton

2) Quantum gates (WIP)

1) Rust based critical parts off-loading
2) Component behaviour refinement
3) More components

4) GUI

### 🤝 Contributing

We welcome contributions!<br>
Feel free to fork the repo, open issues, or submit pull requests.

### 📜 License

LaserPy_Quantum is distributed under a dual-license model to support both the open-source community and commercial applications.

-   **Open Source:** For academic, personal, and open-source projects, LaserPy_Quantum is licensed under the **GNU General Public License v3.0 (GPLv3)**. *Note: Modifications or Derived works on Components system requires maintainer's permission.*

-   **Commercial:** For use in proprietary or commercial software where the terms of *GPLv3 are not suitable*, a separate **commercial license is available**. Please contact the maintainer to discuss licensing options.

### 📬 Contact

Maintained by Anshurup Gupta.<br>
For questions or collaborations, open an issue or [email](mailto:anshurup.gupta@gmail.com).