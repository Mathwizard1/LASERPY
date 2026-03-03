from __future__ import annotations
from typing import Any, Literal

from dataclasses import dataclass

from numpy import (
    cos, sin
)

POLARIZATION_AXIS = Literal['H', 'V']

@dataclass(frozen= True, slots= True)
class SellmeierFormula:
    """
    SellmeierFormula class.
    It uses coefficients of wavelength in microns.
    """
    _coeffs: tuple[float, ...]

    def _func(self, wavelength: float) -> float:
        A, B, C, D = self._coeffs

        # micron units
        wavelength2 = (wavelength * 1e6) ** 2
        n2 = A + B / (wavelength2 - C) - D * wavelength2
        return (n2 ** 0.5)
    
    def _dfunc(self, wavelength: float) -> float:
        A, B, C, D = self._coeffs

        # micron units
        wavelength = wavelength * 1e6
        dn = - (B + D) * wavelength / (self._func(wavelength) * (wavelength ** 2 - C) ** 2)
        return dn

########################################################

class RefractiveMaterial:
    def __init__(self, name: str="default_refractive_material") -> None:
        self.name = name

    def n(self, wavelength: float, material_axis= None) -> Any: pass

    def dn_dwavelength(self, wavelength: float, material_axis= None) -> Any: pass

class Isotropic(RefractiveMaterial):
    def __init__(self, refractive: SellmeierFormula, name="default_isotropic_material"):
        super().__init__(name)

        self._refractive = refractive

    def n(self, wavelength: float, material_axis=None):
        #return super().n(wavelength, material_axis)
        return self._refractive._func(wavelength)

    def dn_dwavelength(self, wavelength: float, material_axis=None):
        #return super().dn_dwavelength(wavelength, material_axis)
        return self._refractive._dfunc(wavelength)

class Birefringent(RefractiveMaterial):
    def __init__(self, ordinary: SellmeierFormula, extraordinary: SellmeierFormula, crystal_angle=0.0, name="default_birefringent_material"):
        super().__init__(name)

        self._ordinary = ordinary
        self._extraordinary = extraordinary

        self._crystal_angle_sin2 = sin(crystal_angle) ** 2
        self._crystal_angle_cos2 = cos(crystal_angle) ** 2

    def set(self, crystal_angle:float):
        self._crystal_angle_sin2 = sin(crystal_angle) ** 2
        self._crystal_angle_cos2 = cos(crystal_angle) ** 2

    def n(self, wavelength: float, material_axis: POLARIZATION_AXIS|None= None):
        #return super().n(wavelength, material_axis)
        if(material_axis == 'H'):
            return self._ordinary._func(wavelength)
        elif(material_axis == 'V'):
            no = self._ordinary._func(wavelength)
            ne = self._extraordinary._func(wavelength)
            neff = (ne * no) / ((no * self._crystal_angle_cos2) ** 2 + (ne * self._crystal_angle_sin2) ** 2) ** 0.5
            return neff
        return (self._ordinary._func(wavelength), self._extraordinary._func(wavelength))
    
    def dn_dwavelength(self, wavelength: float, material_axis: POLARIZATION_AXIS|None= None):
        #return super().dn_dwavelength(wavelength, material_axis)
        if(material_axis == 'H'):
            return self._ordinary._dfunc(wavelength)
        elif(material_axis == 'V'):
            no = self._ordinary._func(wavelength)
            ne = self._extraordinary._func(wavelength)

            dno = self._ordinary._dfunc(wavelength)
            dne = self._extraordinary._dfunc(wavelength)
            dneff = ((self._crystal_angle_cos2 * dne) * (no ** 3) + (self._crystal_angle_sin2 * dno) ** (ne ** 3)) / ((no * self._crystal_angle_cos2) ** 2 + (ne * self._crystal_angle_sin2) ** 2) ** (1.5) 
            return dneff
        return (self._ordinary._dfunc(wavelength), self._extraordinary._dfunc(wavelength))