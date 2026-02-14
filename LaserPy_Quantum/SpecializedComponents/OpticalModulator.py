from __future__ import annotations

from ..Components.Component import Clock
from ..Components.Component import DataComponent, TimeComponent

class PhaseModulator(DataComponent, TimeComponent):
    def __init__(self, name: str = "default_phase_modulator"):
        super().__init__(name)