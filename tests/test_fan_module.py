# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.fan_module import FanModule


class TestFanModule:
    """Define tests for the fan assembly module."""

    sys = FanModule("fm")

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.run_once()

        assert sys.fl_bypass.W == pytest.approx(280.0, 0.1)
        assert sys.fl_core.W == pytest.approx(70.0, 0.1)

    def test_solver(self):
        # basic solver
        sys = self.sys

        solver = sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()

        assert np.linalg.norm(solver.problem.residue_vector()) < 1e-6

    def test_view(self):
        sys = FanModule("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
