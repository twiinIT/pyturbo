import numpy as np

from pyturbo.ports import C1Keypoint


def rz_to_3d(rz):
    return np.r_[rz[0], 0.0, rz[1]]


def slope_to_drdz(slope: float) -> np.ndarray:
    slope_rad = np.radians(slope)
    return np.r_[np.sin(slope_rad), np.cos(slope_rad)]


def slope_to_3d(slope: float) -> np.ndarray:
    """Computes the slope from ..."""
    return rz_to_3d(slope_to_drdz(slope))


def derivative_slope(kp: C1Keypoint) -> float:
    return np.arctan(kp.dr / kp.dz)
