# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateBezier, CreateRevolution, CreateWire

from pyturbo.utils import JupyterViewable


class InletGeom(System, JupyterViewable):
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

        self.add_inward(
            "fan_inlet_tip_kp", np.ones(2), unit="m", desc="Fan inlet tip (A1) keypoint"
        )
        self.add_inward("LqD", 0.3, unit="", desc="Length over fan diameter ratio")

        # aero
        self.add_outward("hilite_kp", np.r_[0.0, 0.0], unit="m", desc="hilite keypoint")
        self.add_outward("area", 1.0, unit="m**2", desc="throat area")

    def compute(self):
        fan_radius = self.fan_inlet_tip_kp[0]
        lip_length = self.LqD * fan_radius * 2.0
        hilite_radius = fan_radius

        self.hilite_kp = np.r_[hilite_radius, self.fan_inlet_tip_kp[1] - lip_length]
        self.area = np.pi * hilite_radius**2

    def _to_occt(self):
        def rz_to_3d(rz):
            return np.r_[rz[0], 0.0, rz[1]]

        inlet = CreateBezier.g1_relative_tension(
            rz_to_3d(self.fan_inlet_tip_kp),
            rz_to_3d(self.hilite_kp),
            (0.0, 0.0, -1),
            (1.0, 0.0, 0.0),
            1.0,
            1.0,
        )

        w = CreateWire.from_element((inlet))

        return CreateRevolution.solid_from_curve(w, CreateAxis.oz())
