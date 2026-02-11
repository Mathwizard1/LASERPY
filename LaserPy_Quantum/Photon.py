from __future__ import annotations

from dataclasses import dataclass, field as datafield

from numpy import (
    dtype, object_,
    angle, abs
)

from itertools import count

from .Constants import ERR_TOLERANCE

_Photon_counter = count()
def _next_photon_id():
    """Global Monotonic Photon counter as uid"""
    return next(_Photon_counter)

""" Photon dtype for Photon class"""
Photon_dtype = dtype([
    ('field', complex),
    ('frequency', float),
    ('photon_number', float),
    ('source_phase', float),
    ('photon_id', int),
    ('qubit_index', int),
    ('quantum_entangler', object_) # For simplicity, store the Python object
])

@dataclass(slots= True)
class Photon:
    """
    Photon class.
    """
    # Microscopic parameters 
    field: complex = ERR_TOLERANCE + 0j
    frequency: float = ERR_TOLERANCE

    # Macroscopic parameters
    photon_number: float = ERR_TOLERANCE
    source_phase: float = ERR_TOLERANCE

    # Uid
    photon_id: int = datafield(default_factory= _next_photon_id)

    # Quantum parameters
    qubit_index: int = -1
    quantum_entangler: QuantumEntangler|None = None

    # Allowing Uid based-hashing
    def __hash__(self):
        return self.photon_id

    def __eq__(self, other: Photon):
        return self.photon_id == other.photon_id

    def __str__(self) -> str:
        return (f"Photon(ω={self.frequency:.4e}rad/s, |E|={self.amplitude:.4e}V/m, φ={self.phase:.2f}rad, id={self.photon_id})")

    def __repr__(self) -> str:
        return (f"Photon(id={self.photon_id}, qubit_idx={self.qubit_index})")

    @classmethod
    def from_photon(cls, other: Photon) -> Photon:
        """Photon classmethod from photon deepcopy method"""
        photon = cls.__new__(cls)                           # Bypasses __init__
        photon.field = other.field
        photon.frequency = other.frequency

        photon.photon_number = other.photon_number
        photon.source_phase = other.source_phase

        photon.photon_id = other.photon_id
        
        photon.qubit_index = other.qubit_index
        photon.quantum_entangler = other.quantum_entangler
        return photon

    @property
    def amplitude(self) -> float:
        """amplitude (V/m) of the field"""
        return abs(self.field)

    @property
    def phase(self) -> float:
        """phase (rad) of the field"""
        return float(angle(self.field))

    def qubit(self):        
        QE = self.quantum_entangler
        if(QE is None):
            QE = QuantumEntangler((self,))
        return QE
    
Empty_Photon = Photon()

from .QuantumOptics.Entangler import QuantumEntangler