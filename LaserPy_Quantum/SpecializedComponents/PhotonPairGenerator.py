from __future__ import annotations
from typing import Literal

from dataclasses import dataclass

from numpy import (
    array,
    sinc,
    pi
)

from ..Components.Component import DataComponent

from ..QuantumOptics.Entangler import QuantumEntangler, QuantumStateModel

from .Laser import Laser

from ..utils.RefractiveMaterials import POLARIZATION_AXIS, RefractiveMaterial

from ..Constants import UniversalConstants, LaserPyConstants, ERR_TOLERANCE, RND_GEN

from ..Photon import Photon, Empty_Photon

SPDC_TYPE = Literal['0', 'I', 'II']

@dataclass(slots= True)
class ParametricTriple:
    pump: POLARIZATION_AXIS
    signal: POLARIZATION_AXIS
    idler: POLARIZATION_AXIS

class PhotonPairGeneratorCrystal(DataComponent):
    _deff = LaserPyConstants.get('deff')

    def __init__(self, refractive_material: RefractiveMaterial, SPDC_type: SPDC_TYPE= 'II', length: float|None = None, poling_period: float|None = None, name: str = "default_photon_pair_generator_crystal"):
        super().__init__(name)
        self.omega_s = ERR_TOLERANCE
        self.omega_i = ERR_TOLERANCE

        self.delta_K = ERR_TOLERANCE

        self.pair_rate = ERR_TOLERANCE

        self.photon: Photon = Empty_Photon
        self.signal: Photon = Empty_Photon
        self.idler: Photon = Empty_Photon

        # Data storage
        self._simulation_data = {'omega_s':[], 'omega_i':[], 'delta_K':[], 'pair_rate':[]}
        self._simulation_data_units = {'omega_s':r" $(Hz)$", 'omega_i':r" $(Hz)$", 'delta_K':r" $(rad/m)$", 'pair_rate':r" $(per photon)$"}

        self._refractive_material = refractive_material
        if(length is None):
            length = LaserPyConstants.get('Crystal_length')
        self._length = length 
        self._poling_period = poling_period        
        
        # Polarization conventions based on SPDC type
        self._SPDC_type = SPDC_type

        if(self._SPDC_type == '0'):
            self._polarizations = ParametricTriple('V', 'V', 'V')
        elif(self._SPDC_type == 'I'):
            self._polarizations = ParametricTriple('V', 'H', 'H')
        else:
            self._polarizations = ParametricTriple('V', 'V', 'H')

        self._pump_bandwidth = 0.0

    def set_laser(self, laser: Laser):
        #return super().set()
        self._pump_bandwidth = laser.get_pump_bandwidth()

    def _QS(self):
        state = array([0, 0, 0, 0], dtype= complex)
        if(self._SPDC_type == '0'):
            state[3] = 1.0
        elif(self._SPDC_type == 'I'):
            state[0] = 1.0
        else:
            state[1] = state[2] = (0.5) ** 0.5
        return QuantumStateModel(2, state)

    def _group_index(self, wavelength: float, polarization: POLARIZATION_AXIS):
        ng = self._refractive_material.n(wavelength, polarization) - wavelength * self._refractive_material.dn_dwavelength(wavelength, polarization)
        return ng

    def _gaussian_JSA(self, photon: Photon):
        pump_wavelength = photon.wavelength
        degenerate_wavelength = 2 * pump_wavelength

        ng_s = self._group_index(degenerate_wavelength, self._polarizations.signal)
        ng_i = self._group_index(degenerate_wavelength, self._polarizations.idler)

        sigma_wavelength = 0.88 * (degenerate_wavelength ** 2) / (2.355 * self._length * abs(ng_s - ng_i))
        
        sigma_omega_pm = (2 * pi * UniversalConstants.C.value / (degenerate_wavelength ** 2)) * sigma_wavelength

        sigma_omega_s = (sigma_omega_pm ** 2 + self._pump_bandwidth ** 2) ** 0.5

        # Sample signal frequency
        omega_s = RND_GEN.normal(loc= 0.5 * photon.frequency, scale= sigma_omega_s)
        omega_i = photon.frequency - omega_s
        return omega_s, omega_i

    def simulate(self, photon: Photon):
        #return super().simulate(args)
        if self._SPDC_type == 'II':
            if (RND_GEN.random() < 0.5):
                self._polarizations.signal, self._polarizations.idler = 'V', 'H'
            else:
                self._polarizations.signal, self._polarizations.idler = 'H', 'V'

        self.omega_s, self.omega_i = self._gaussian_JSA(photon)

        self.photon = Photon.from_photon(photon)
        signal_photon = Photon(frequency= self.omega_s)
        idler_photon = Photon(frequency= self.omega_i)

        # Phase dependent terms
        np = self._refractive_material.n(photon.wavelength, self._polarizations.pump)
        ns = self._refractive_material.n(signal_photon.wavelength, self._polarizations.signal)
        ni = self._refractive_material.n(idler_photon.wavelength, self._polarizations.idler)
        
        self.delta_K = (np * photon.frequency - ns * signal_photon.frequency - ni * idler_photon.frequency) / UniversalConstants.C.value
        if(self._poling_period): self.delta_K -= 2 * pi / self._poling_period

        # np.sinc(x) = sin(pi * x) / (pi * x)
        phase_term = sinc(self.delta_K * self._length / (2 * pi)) ** 2

        gain = (self._deff * photon.frequency * photon.amplitude * self._length / (np * ns * ni * UniversalConstants.C.value)) ** 2
        self.pair_rate = gain * phase_term

        # Actual Pair generation
        N_pairs = RND_GEN.poisson(self.pair_rate * photon.photon_number)
        if (N_pairs < 1):
            self.omega_s = ERR_TOLERANCE
            self.omega_i = ERR_TOLERANCE
            self.signal = Photon.from_photon(Empty_Photon)
            self.idler = Photon.from_photon(Empty_Photon)
            return

        # Other Photon data
        signal_photon.photon_number = N_pairs
        idler_photon.photon_number = N_pairs

        # Global state initialization
        QuantumEntangler((signal_photon, idler_photon), self._QS())

        self.signal = signal_photon
        self.idler = idler_photon

    def input_port(self):
        #return super().input_port()
        kwargs = {'photon': None}
        return kwargs