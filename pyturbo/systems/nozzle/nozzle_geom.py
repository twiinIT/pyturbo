# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.base import System

from pyturbo.ports import KeypointsPort


class NozzleGeom(System):
    """Nozzle geometry model.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    Inputs
    ------
    kp : KeypointsPort
        nozzle geometrical envelop

    Outputs
    -------
    area[m**2] : float, default=1.0
        throat area, same as exit
    area_in[m**2]: float
        inlet area section
    area_exit[m**2]: float
        exit area section
    """

    def setup(self):
        # inputs
        self.add_input(KeypointsPort, "kp")

        # aero
        self.add_outward("area", 1.0, unit="m**2", desc="exit area")
        self.add_outward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("area_exit", 1.0, unit="m**2", desc="exit area")

    def compute(self):
        # throat
        r_tip = self.kp.exit_tip_r
        r_hub = self.kp.exit_hub_r
        self.area = np.pi * (r_tip**2 - r_hub**2)

        r_tip = self.kp.inlet_tip_r
        r_hub = self.kp.inlet_hub_r
        self.area_in = np.pi * (r_tip**2 - r_hub**2)

        r_tip = self.kp.exit_tip_r
        r_hub = self.kp.exit_hub_r
        self.area_exit = np.pi * (r_tip**2 - r_hub**2)
