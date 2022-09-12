# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.ports import Port


class KeypointsPort(Port):
    """Keypoints of an annular geometry.

    The geometry is assumed to be revolution around x-axis and keypoints
    are defined in {r, z} coordinates.

    Variables
    ---------
    inlet_hub [m] : np.ndarray
        inlet hub keypoint
    inlet_tip [m] : np.ndarray
        inlet tip keypoint
    exit_hub [m] : np.ndarray
        exit hub keypoint
    exit_tip [m] : np.ndarray
        exit tip keypoint
    """

    def setup(self):
        self.add_variable("inlet_hub", np.r_[0.0, 0.0], unit="m", desc="inlet hub")
        self.add_variable("inlet_tip", np.r_[0.9, 0.0], unit="m", desc="inlet tip")
        self.add_variable("exit_hub", np.r_[0.0, 0.9], unit="m", desc="exit hub")
        self.add_variable("exit_tip", np.r_[0.9, 0.9], unit="m", desc="exit tip")

    @property
    def inlet_hub_r(self):
        return self.inlet_hub[0]

    @property
    def inlet_hub_z(self):
        return self.inlet_hub[1]

    @property
    def inlet_tip_r(self):
        return self.inlet_tip[0]

    @property
    def inlet_tip_z(self):
        return self.inlet_tip[1]

    @property
    def exit_hub_r(self):
        return self.exit_hub[0]

    @property
    def exit_hub_z(self):
        return self.exit_hub[1]

    @property
    def exit_tip_r(self):
        return self.exit_tip[0]

    @property
    def exit_tip_z(self):
        return self.exit_tip[1]

    @property
    def mean_radius(self):
        return np.mean((self.inlet_hub, self.inlet_tip, self.exit_hub, self.exit_tip), axis=0)[0]


class C1Keypoint:
    """A keypoint class including C1-continuity info

    A C1 keypoint contains both position `pos` and first order derivate `der`.

    The geometry is assumed to be revolution around x-axis and keypoint
    is defined in {r, z} coordinates.
    """

    default_pos = np.ones(2)
    default_der = np.ones(2)

    def __init__(self, pos=default_pos, der=default_der):
        self.pos = pos
        self.der = der

    @property
    def rz(self):
        return self.pos

    @rz.setter
    def rz(self, rz: np.ndarray):
        self.pos = rz

    @property
    def r(self):
        return self.pos[0]

    @r.setter
    def r(self, val: float):
        self.pos[0] = val

    @property
    def z(self):
        return self.pos[1]

    @z.setter
    def z(self, val: float):
        self.pos[1] = val

    @property
    def drdz(self):
        return self.der

    @drdz.setter
    def drdz(self, drdz: np.ndarray):
        self.der = drdz

    @property
    def dr(self):
        return self.der[0]

    @dr.setter
    def dr(self, val: float):
        self.der[0] = val

    @property
    def dz(self):
        return self.der[1]

    @dz.setter
    def dz(self, val: float):
        self.der[1] = val
