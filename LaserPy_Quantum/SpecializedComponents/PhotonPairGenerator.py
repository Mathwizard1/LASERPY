from __future__ import annotations
from typing import Literal

from collections import namedtuple

from numpy import (
    random,
    array, ones,
    sinc,
    pi
)

from ..Components.Component import Component

from ..QuantumOptics.Entangler import QuantumEntangler, QuantumStateModel

from .Laser import Laser

from ..utils.RefractiveMaterials import POLARIZATION_AXIS, RefractiveMaterial

from ..Constants import UniversalConstants, LaserPyConstants

from ..Photon import Photon, Empty_Photon

SPDC_TYPE = Literal['0', 'I', 'II']

class PhotonPairGeneratorCrystal(Component):
    _deff = LaserPyConstants.get('deff')

    SPDC_POLARIZATIONS = namedtuple('SPDC_POLARIZATIONS', ('pump', 'signal', 'idler'))

    def __init__(self, refractive_material: RefractiveMaterial, SPDC_type: SPDC_TYPE= 'II', length: float|None = None, name: str = "default_photon_pair_generator_crystal"):
        super().__init__(name)

        self._refractive_material = refractive_material
        if(length is None):
            self._length = LaserPyConstants.get('Crystal_length')
        self._SPDC_type = SPDC_type

        # Polarization conventions based on SPDC type
        if(self._SPDC_type == '0'):
            self._polarizations = PhotonPairGeneratorCrystal.SPDC_POLARIZATIONS('H', 'H', 'H')
        elif(self._SPDC_type == 'I'):
            self._polarizations = PhotonPairGeneratorCrystal.SPDC_POLARIZATIONS('H', 'V', 'V')
        else:
            self._polarizations = PhotonPairGeneratorCrystal.SPDC_POLARIZATIONS('H', 'H', 'V')

        self._pump_bandwidth = 0.0

        self._photon: Photon = Empty_Photon
        self._photon_port2: Photon = Empty_Photon

    def set_laser(self, laser: Laser):
        #return super().set()
        self._pump_bandwidth = laser.get_pump_bandwidth()

    def _group_index(self, wavelength: float, polarization: POLARIZATION_AXIS):
        ng = self._refractive_material.n(wavelength, polarization) - wavelength * self._refractive_material.dn_dwavelength(wavelength, polarization)
        return ng

    def _gaussian_JSA(self, photon: Photon):
        # micron units
        pump_wavelength = photon.wavelength
        degenerate_wavelength = 2 * pump_wavelength

        ng_s = self._group_index(degenerate_wavelength, self._polarizations.signal)
        ng_i = self._group_index(degenerate_wavelength, self._polarizations.idler)

        sigma_wavelength = 0.88 * (degenerate_wavelength ** 2) / (2.355 * self._length * abs(ng_s - ng_i))
        sigma_omega_pm = (2 * pi * UniversalConstants.C.value / (degenerate_wavelength ** 2)) * sigma_wavelength

        sigma_s = (sigma_omega_pm ** 2 + self._pump_bandwidth ** 2) ** 0.5

        # Sample signal frequency
        omega_s = random.normal(loc= 0.5 * photon.frequency, scale= sigma_s)
        omega_i = photon.frequency - omega_s

        return omega_s, omega_i

    def _phase_mismatch(self, pump_wavelength: float, signal_wavelength: float, idler_wavelength: float):
        Kp = self._refractive_material.n(pump_wavelength, self._polarizations.pump) / pump_wavelength
        Ks = self._refractive_material.n(signal_wavelength, self._polarizations.signal) / signal_wavelength
        Ki = self._refractive_material.n(idler_wavelength, self._polarizations.idler) / idler_wavelength
        return 2 * pi * (Kp - Ks - Ki)

    def simulate(self, photon: Photon):
        #return super().simulate(args)
        omega_s, omega_i = self._gaussian_JSA(photon)

        signal_photon = Photon(frequency= omega_s)
        idler_photon = Photon(frequency= omega_i)

        # micron units
        delta_K = self._phase_mismatch(photon.wavelength, signal_photon.wavelength, idler_photon.wavelength)
        print(delta_K)

        # Phase dependent terms
        n_p = self._refractive_material.n(photon.wavelength, self._polarizations.pump)

        # SI units
        phase_term = sinc(delta_K * self._length / (2 * pi)) ** 2
        print(phase_term)
        gain = (self._deff * photon.amplitude * photon.frequency * self._length / (n_p * UniversalConstants.C.value)) ** 2
        print(gain)

        pair_probability = gain * phase_term
        print(pair_probability)
        if (random.rand() > pair_probability):
            self._photon = Empty_Photon
            self._photon_port2 = Empty_Photon
            return

        # Other Photon data
        mean_photon_numbers = pair_probability * photon.photon_number
        signal_photon.photon_number = mean_photon_numbers
        idler_photon.photon_number = mean_photon_numbers

        # Global state initialization
        QuantumEntangler((signal_photon, idler_photon))

        self._photon = signal_photon
        self._photon_port2 = idler_photon

    def input_port(self):
        #return super().input_port()
        kwargs = {'photon':None}
        return kwargs

    def output_port(self, kwargs: dict = {}):
        #return super().output_port(kwargs)
        kwargs['photon'] = self._photon
        kwargs['photon_port2'] = self._photon_port2
        return kwargs