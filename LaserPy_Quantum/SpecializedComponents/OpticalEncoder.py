from __future__ import annotations

from collections import namedtuple

from ..Components.Component import DataComponent, TimeComponent

class BasisEncoder(DataComponent, TimeComponent):
    def __init__(self,name: str = "default_basis_encoder"):
        super().__init__(name)