# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.base import System

from pyturbo.ports import KeypointsPort


class CompressorGeom(System):
    """Compressor geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.
    The geometry exposed to aero module is made of:
    - inlet area
    - inlet and exit tip radius

    Inputs
    ------
    kp: KeypointsPort
        compressor geometrical envelop

    stage_count[-]: integer, default=1
        number of stages

    blade_height_ratio[-]: float, default=0.2
        inlet blade height relative to compressor inlet tip radius

    Outputs
    -------
    tip_in_r[m]: float, default=1.0
        inlet tip radius
    tip_out_r[m]: float, default=1.0
        exit tip radius
    inlet_area[m**2]: float, default=1.0
        inlet area
    """

    def setup(self):
        # inputs
        self.add_input(KeypointsPort, "kp")

        self.add_inward("stage_count", 1, unit="", desc="number of stages")
        self.add_inward(
            "blade_hub_to_tip_ratio",
            0.2,
            unit="",
            desc="blade hub-to-tip radius ratio",
        )

        # blade geometric properties
        self.add_outward("inlet_area", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_outward("tip_out_r", 1.0, unit="m", desc="exit tip radius")

    def compute(self):
        # Compute blade hub radial position
        hub_in_r = self.kp.inlet_tip_r * self.blade_hub_to_tip_ratio

        self.inlet_area = np.pi * (self.kp.inlet_tip_r**2 - hub_in_r**2)
        self.tip_in_r = self.kp.inlet_tip_r
        self.tip_out_r = self.kp.exit_tip_r
