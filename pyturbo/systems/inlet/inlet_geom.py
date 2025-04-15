# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class InletGeom(System):
    """Inlet geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    Inputs
    ------
    kp: KeypointsPort
        inlet geometrical envelop

    fan_inlet_tip_kp[m]: np.array(2), default=np.ones(2)
        Fan inlet tip (A1) keypoint

    LqD[-]: float, default=0.3
        Length over fan diameter ratio

    Outputs
    -------
    area[m**2]: float
        throat area

    hilite_kp[m]: np.array(2), default=np.ones(2)
        hilite keypoint
    area[m**2]: float, default=1.0
        throat area
    """

    def setup(self):
        # inputs/outputs
        self.add_input(KeypointsPort, "kp")

        # aero
        self.add_outward("area", 1.0, unit="m**2", desc="throat area")

    def compute(self):
        radius = self.kp.exit_tip[0]
        self.area = np.pi * radius**2
