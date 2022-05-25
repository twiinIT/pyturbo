# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.ports import Port


class KeypointsPort(Port):
    """Keypoints of an annular geometry.

    The geometry is assumed to be revolution around x-axis and keypoints
    are defined in {r, z} coordinates.
    """

    def setup(self):
        self.add_variable("inlet_hub", np.r_[0.9, 0.0], desc="inlet hub")
        self.add_variable("inlet_tip", np.r_[0.9, 0.0], desc="inlet tip")
        self.add_variable("exit_hub", np.r_[0.9, 0.0], desc="exit hub")
        self.add_variable("exit_tip", np.r_[0.9, 0.0], desc="exit tip")

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
