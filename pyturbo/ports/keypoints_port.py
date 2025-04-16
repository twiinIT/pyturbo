# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.ports import Port
from pyoccad.create import CreateAxis, CreateRevolution, CreateWire


class KeypointsPort(Port):
    """Keypoints of an annular geometry.

    The geometry is assumed to be revolution around x-axis and keypoints
    are defined in {r, z} coordinates.

    Variables
    ---------
    inlet_hub[m]: np.ndarray, default=np.r_[0.0, 0.0]
        inlet hub keypoint
    inlet_tip[m]: np.ndarray, default=np.r_[0.9, 0.0]
        inlet tip keypoint
    exit_hub[m]: np.ndarray, default=np.r_[0.0, 0.9]
        exit hub keypoint
    exit_tip[m]: np.ndarray, default=np.r_[0.9, 0.9]
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

    def view(self, shell=False):
        from pyturbo.utils import rz_to_3d

        if shell:
            inner = CreateWire.from_points((rz_to_3d(self.inlet_hub), rz_to_3d(self.exit_hub)))
            outer = CreateWire.from_points((rz_to_3d(self.inlet_tip), rz_to_3d(self.exit_tip)))
            w = (inner, outer)

            return CreateRevolution.surface_from_curve(inner, CreateAxis.oz())

        else:
            w = CreateWire.from_points(
                (
                    rz_to_3d(self.inlet_hub),
                    rz_to_3d(self.exit_hub),
                    rz_to_3d(self.exit_tip),
                    rz_to_3d(self.inlet_tip),
                ),
                auto_close=True,
            )

            return CreateRevolution.surface_from_curve(w, CreateAxis.oz())
