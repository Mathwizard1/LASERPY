"""Constants for LaserPy_Quantum"""

from enum import Enum

from pathlib import Path
import json

from numpy.random import (
    default_rng
)

#import rust_optimizer

# fixed Scientific Constants
class UniversalConstants(float, Enum):
    """
    Universal Constants for LaserPy_Quantum
    """

    CHARGE = 1.602 * (1.0e-19)
    """
    single unit of Charge of elctron / proton (magnitude)
    """

    H = 6.626 * (1.0e-34)
    """
    Plank's Constant 
    """

    HBAR = 1.054 * (1.0e-34)
    """
    reduced Plank's Constant 
    """

    C = 2.997 * (1.0e+8)
    """
    Speed of light in vacuum 
    """

    EPSILON_0 = 8.8541878128e-12
    """
    Permittivity of free space
    """

class LaserPyConstants:
    """
    Simulation Constants for LaserPy_Quantum
    """
    _Constants: dict[str, float] = {}

    @classmethod
    def load_from_json(cls, filepath=r'Constants.json'):
        # Check the Local Directory (Project root/Running folder)
        local_file = Path.cwd() / filepath
        
        # Check the Library Internal Directory
        internal_file = Path(__file__).parent / filepath

        # Search Priority logic
        target_path = None
        if local_file.exists(): target_path = local_file
        elif internal_file.exists(): target_path = internal_file

        if target_path:
            with target_path.open('r') as f:
                cls._Constants = json.load(f)
        else:
            raise FileNotFoundError(f"Warning: {filepath} not found in {Path.cwd()} or {Path(__file__).parent}")

    @classmethod
    def get(cls, key, default=1.0):
        """Retrieves a constant value by key."""
        return cls._Constants.get(key, default)

    @classmethod
    def set(cls, key, value):
        """Allows for runtime modification of a constant."""
        cls._Constants[key] = value

# Load the constants at the runtime
LaserPyConstants.load_from_json()

ERR_TOLERANCE = 1.0e-12

FIG_WIDTH = 12
FIG_HEIGHT = 6

RND_GEN = default_rng()

# if __name__ == "__main__":
#     constants = rust_optimizer.UniversalConstant
#     print(constants.SpeedOfLight.value())        # 299792458.0