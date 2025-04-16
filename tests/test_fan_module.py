# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

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

    @pytest.mark.skip("not relevant")
    def test_solver(self):
        # basic solver
        sys = self.sys

        sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()

        assert sys.bpr == pytest.approx(5.12, abs=0.1)
        assert sys.booster.pr == pytest.approx(1.44, abs=0.1)
        assert sys.fan.pr == pytest.approx(1.66, abs=0.1)

    def test_view(self):
        sys = FanModule("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
