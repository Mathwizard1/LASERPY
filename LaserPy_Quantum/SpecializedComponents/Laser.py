from __future__ import annotations

from numpy import (
    sqrt, exp, cos, sin, mod,
    pi,
)

from ..Components.Component import Clock
from ..Components.Component import DataComponent, TimeComponent

from ..Components.Signal import NoNoise

from ..Constants import UniversalConstants
from ..Constants import LaserPyConstants

from ..Constants import ERR_TOLERANCE

from ..Photon import Photon

class Laser(DataComponent, TimeComponent):
    """
    Laser class
    """

    # Class variables for Laser
    _TAU_N = LaserPyConstants.get('Tau_N')
    _TAU_P = LaserPyConstants.get('Tau_P')

    _g = LaserPyConstants.get('g')
    _Epsilon = LaserPyConstants.get('Epsilon')
  
    _N_transparent = LaserPyConstants.get('N_transparent')

    _Beta = LaserPyConstants.get('Beta')
    _Alpha = LaserPyConstants.get('Alpha')
    _Eta = LaserPyConstants.get('Eta')

    _Laser_Vol = LaserPyConstants.get('Laser_Vol')
    _Laser_Beam_Area = LaserPyConstants.get('Laser_Beam_Area')

    _Gamma_cap = LaserPyConstants.get('Gamma_cap')
    _Kappa = LaserPyConstants.get('Kappa')

    def __init__(self, laser_wavelength:float|None = None, name: str = "default_laser"):
        super().__init__(name)
        self.photon_density: float = ERR_TOLERANCE
        """photon number data for Laser"""

        self.carrier: float = self._N_transparent
        """carrier data for Laser"""

        self.phase: float = ERR_TOLERANCE
        """phase data for Laser"""

        self.current: float = ERR_TOLERANCE
        """current data for Laser"""

        # Data storage
        self._simulation_data = {'current':[], 'photon_density':[], 'carrier':[], 'phase':[]}
        self._simulation_data_units = {'current':r" $(Amp)$", 'photon_density':r" $(m^{-3})$",
                                           'carrier':r" $(m^{-3})$", 'phase':r" $(rad)$"}

        # Laser class private data
        if(laser_wavelength is None):
            laser_wavelength = LaserPyConstants.get('Laser_wavelength')
        self._free_running_freq = 2 * pi * UniversalConstants.C.value / laser_wavelength
        """free running frequency data for Laser"""

        self.photon: Photon = Photon(ERR_TOLERANCE + 0j, self._free_running_freq)
        """Photon class data for Laser"""

        self._refractive_index = 3.4

        # Noise classes for simulations
        self._Fn_t = NoNoise('carrier_NoNoise')
        self._Fs_t = NoNoise('photon_NoNoise')
        self._Fphi_t = NoNoise('phase_NoNoise')

        # Optical Injection locking data
        self._slave_locked: bool = False

    def _dN_dt(self):
        """Delta number of carrier method"""
        dN_dt = self.current / (UniversalConstants.CHARGE.value * self._Laser_Vol) - self.carrier / self._TAU_N - self._g * ((self.carrier - self._N_transparent) / (1 + self._Epsilon * self.photon_density)) * self.photon_density + self._Fn_t()
        return dN_dt

    def _dS_dt(self):
        """Delta number of photon method"""
        dS_dt = self._Gamma_cap * self._g * ((self.carrier - self._N_transparent) / (1 + self._Epsilon * self.photon_density)) * self.photon_density - self.photon_density / self._TAU_P + self._Gamma_cap * self._Beta * self.carrier / self._TAU_N + self._Fs_t()
        return dS_dt

    def _dPhi_dt(self):
        """Delta phase method"""
        dPhi_dt = (self._Alpha / 2) * (self._Gamma_cap * self._g * (self.carrier - self._N_transparent) - 1 / self._TAU_P) + self._Fphi_t()
        return dPhi_dt

    def _power(self):
        """Laser _power method""" 
        return self.photon_density * self._Laser_Vol * self._Eta * UniversalConstants.H.value * self._free_running_freq / self._TAU_P

    def set_noise(self, Fn_t:NoNoise, Fs_t:NoNoise, Fphi_t:NoNoise):
        """Laser set noise method""" 
        self._Fn_t = Fn_t
        self._Fs_t = Fs_t
        self._Fphi_t = Fphi_t

    def set_slave_Laser(self, slave_locked: bool = True):
        """Laser set master laser method""" 
        self._slave_locked = slave_locked

    def simulate(self, clock: Clock, current: float, photon: Photon|tuple[Photon,...]|None = None):
        """Laser simulate method"""
        #return super().simulate(clock)

        # Save current in its variable
        self.current = current

        # Base Laser rate equations
        dN_dt = self._dN_dt()
        dS_dt = self._dS_dt()
        dPhi_dt = self._dPhi_dt()

        # injection photons equations
        if(self._slave_locked and photon):
            if(isinstance(photon, Photon)):
                photon = (photon,)

            # Multi Master laser lock
            for injection_photon in photon:
                delta_phase = self.phase - injection_photon.source_phase
                master_freq_detuning = (self._free_running_freq - injection_photon.frequency) * clock.t
                
                # Injection terms effects
                S_inj = injection_photon.photon_density(self._Laser_Vol)
                dS_dt += 2 * self._Kappa * sqrt(S_inj * self.photon_density) * cos(delta_phase - master_freq_detuning)
                dPhi_dt -= self._Kappa * sqrt(S_inj / self.photon_density) * sin(delta_phase - master_freq_detuning)

        # Time step update (Euler Integration)
        self.carrier += dN_dt * clock.dt
        self.photon_density += dS_dt * clock.dt
        self.phase += dPhi_dt * clock.dt

        # Value corrections
        self.carrier = max(self.carrier, ERR_TOLERANCE)
        self.photon_density = max(self.photon_density, ERR_TOLERANCE)

        # Optical field
        P = self._power()
        self.photon.field = sqrt(2 * P / (self._refractive_index * UniversalConstants.EPSILON_0.value * UniversalConstants.C.value * self._Laser_Beam_Area)) * exp(1j * self.phase)
        self.photon.photon_number = self.photon_density * self._Laser_Vol
        self.photon.source_phase = self.phase

    def input_port(self):
        """Laser input port method""" 
        #return super().input_port()
        kwargs = {'clock':None, 'current':None, 'photon':None}
        return kwargs
    
    def get_linewidth(self):
        Rsp = self._Beta * self.carrier / self._TAU_N
        delta_nu = self._Gamma_cap * Rsp * (1 + self._Alpha ** 2) / (4 * pi * self.photon_density)
        return delta_nu

    def get_pump_bandwidth(self):
        sigma_omega_p = 2 * pi * self.get_linewidth()
        return sigma_omega_p