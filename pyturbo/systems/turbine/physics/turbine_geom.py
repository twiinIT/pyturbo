# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.base import System

from pyturbo.ports import KeypointsPort


class TurbineGeom(System):
    """Turbine geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.
    The geometry exposed to aero module is made of:
    - inlet area
    - inlet and exit tip radius

    Inputs
    ------
    kp: KeypointsPort
        geometrical envelop

    stage_count: integer
        number of stages

    blade_height_ratio[-]: float, default=0.2
        inlet blade height relative to compressor inlet tip radius
    exit_hubqtip[-]: float, default=0.8
        exit hub-to-tip radius ratio

    Outputs
    -------
    mean_radius[m]: float, default=1.0
        mean radius
    fp_exit_hub_kp[m]: np.array(2), default=np.ones(2)
        flowpath exit hub keypoint
    area_in[m**2]: float, default=1.0
        inlet area
    """

    def setup(self):
        # inputs
        self.add_input(KeypointsPort, "kp")

        # inwards
        self.add_inward("stage_count", 1)
        self.add_inward(
            "blade_height_ratio",
            0.2,
            unit="",
            desc="blade height relative to tip radius",
        )
        self.add_inward(
            "exit_hubqtip",
            0.8,
            unit="",
            desc="exit hub-to-tip radius ratio",
        )

        # aero outputs
        self.add_outward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("mean_radius", 1.0, unit="m", desc="mean radius")
        self.add_outward("fp_exit_hub_kp", np.ones(2), unit="m", desc="flowpath exit hub keypoint")

        self.add_outward("hub_in_r", 1.0, unit="m", desc="inlet radius")
        self.add_outward("hub_out_r", 1.0, unit="m", desc="outlet radius")

    def compute(self):

        self.hub_in_r = self.kp.inlet_tip_r * (1 - self.blade_height_ratio)
        self.hub_out_r = self.kp.exit_tip_r * (1 - self.blade_height_ratio)

        self.area_in = np.pi * (self.kp.inlet_tip_r**2 - self.hub_in_r**2)

        self.mean_radius = (
            self.kp.inlet_tip_r + self.hub_in_r + self.kp.exit_tip_r + self.hub_out_r
        ) / 4.0

        self.fp_exit_hub_kp = self.kp.exit_tip * np.r_[self.exit_hubqtip, 1.0]
