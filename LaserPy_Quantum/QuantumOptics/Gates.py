from __future__ import annotations

from numpy import (
    ndarray,
    array, 
)

from ..Photon import Photon

class Gates:
    @staticmethod
    def _Gate(matrix: ndarray, target: Photon, control: Photon|None = None):
        pass

    @staticmethod
    def I(target: Photon) -> None:
        pass

    @staticmethod
    def X(target: Photon) -> None:
        pass

    @staticmethod
    def Y(target: Photon) -> None:
        pass

    @staticmethod
    def Z(target: Photon) -> None:
        pass

    @staticmethod
    def H(target: Photon) -> None:
        pass

    @staticmethod
    def CNOT(target: Photon, control:Photon) -> None:
        pass