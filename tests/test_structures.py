# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.structures import Channel, IntermediateCasing


class TestChannel:
    """Define tests for the structure model."""

    sys = Channel("ch")

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.fl_in.Pt = 100.0
        sys.aero.pressure_loss = 0.01

        sys.run_once()

        assert sys.fl_out.Pt == 99.0


class TestIntermediateCasing:
    """Define tests for the intermediate casing model."""

    sys = IntermediateCasing("ic")

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.kp.inlet_hub = np.r_[0.0, 2.0]
        sys.kp.inlet_tip = np.r_[1.0, 2.0]
        sys.kp.exit_hub = np.r_[0.0, 3.0]
        sys.kp.exit_tip = np.r_[1.0, 3.0]

        sys.primary_aero.pressure_loss = 0.01
        sys.secondary_aero.pressure_loss = 0.01

        sys.run_once()

    def test_solver(self):
        # basic solver
        sys = self.sys

        sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()
