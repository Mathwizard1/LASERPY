from __future__ import annotations

from numpy import (
    mod, exp, sqrt,
    pi
)

from ..Components.Component import Component

from ..Photon import Photon, Empty_Photon

class PhaseCell(Component):
    """
    PhaseCell class
    """
    def __init__(self, phase_delay: float = 0.0, name: str = "default_phase_cell"):
        super().__init__(name)

        self._phase_interval = 2 * pi
        """phase interval for PhaseCell"""

        phase_delay = mod(phase_delay, self._phase_interval)
        self._phase_change = exp(1j * phase_delay)
        """phase change for PhaseCell"""

        self._photon: Photon = Empty_Photon
        """photon data for PhaseCell"""

    def set(self, phase_delay: float, phase_interval: float|None= None):
        """PhaseCell set method"""
        #return super().set()
        if(phase_interval):
            self._phase_interval = phase_interval
        phase_delay = mod(phase_delay, self._phase_interval)
        self._phase_change = exp(1j * phase_delay)

    def simulate(self, photon: Photon):
        """PhaseCell simulate method"""
        #return super().simulate(args)
        self._photon = Photon.from_photon(photon)

        # Add phase change
        self._photon.field = self._photon.field * self._phase_change
        return self._photon

    def input_port(self):
        """PhaseCell input port method"""
        #return super().input_port()
        kwargs = {'photon':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """PhaseCell output port method"""
        #return super().output_port(kwargs)
        kwargs['photon'] = self._photon
        return kwargs
    
class Mirror(PhaseCell):
    """
    Mirror class
    """
    def __init__(self, name: str = "default_mirror"):
        super().__init__(pi, name)

    def set(self):
        """Mirror set method"""
        #return super().set(phase_delay, phase_interval)
        print("Mirror phase is fixed at pi")

class BeamSplitter(Component):
    """
    BeamSplitter class
    """
    def __init__(self, splitting_ratio_t: float = 0.5, name: str = "default_beam_splitter"):
        super().__init__(name)

        # Field coefficients
        self._t = sqrt(splitting_ratio_t)
        self._r = exp(0.5j * pi) * sqrt(1 - splitting_ratio_t)

        # Photon variables
        self._photon_transmitted: Photon = Empty_Photon
        self._photon_reflected: Photon = Empty_Photon

    def set(self, splitting_ratio_t: float):
        """BeamSplitter set method"""
        #return super().set()
        self._t: complex = sqrt(splitting_ratio_t)
        self._r: complex = exp(0.5j * pi) * sqrt(1 - splitting_ratio_t)

    def simulate(self, photon: Photon, photon_port2: Photon|None = None):
        """BeamSplitter simulate method"""
        #return super().simulate(args)
        self._photon_transmitted = Photon.from_photon(photon)
        net_photons = photon.photon_number

        if(photon_port2):
            self._photon_reflected = Photon.from_photon(photon_port2)
            net_photons += photon_port2.photon_number
        else:
            self._photon_reflected = Photon.from_photon(Empty_Photon)

        # Mixing of fields
        E_T = self._t * self._photon_transmitted.field + self._r * self._photon_reflected.field
        E_R = self._r * self._photon_transmitted.field + self._t * self._photon_reflected.field

        field_T = abs(E_T) ** 2 
        field_R = abs(E_R) ** 2 
        net_field = field_T + field_R

        # Final photons
        self._photon_transmitted.field = E_T
        self._photon_transmitted.photon_number = net_photons * field_T / net_field

        self._photon_reflected.field = E_R
        self._photon_reflected.photon_number = net_photons * field_R / net_field
        return self._photon_transmitted, self._photon_reflected

    def input_port(self):
        """BeamSplitter input port method"""
        #return super().input_port()
        
        # Default port2 electric field
        kwargs = {'photon':None, 'photon_port2':None}
        return kwargs
    
    def output_port(self, kwargs: dict = {}):
        """BeamSplitter output port method"""
        #return super().output_port(kwargs)
        kwargs['photon'] = self._photon_transmitted
        kwargs['photon_port2'] = self._photon_reflected
        return kwargs