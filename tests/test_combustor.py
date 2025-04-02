# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import Combustor


class TestCombustor:
    """Define tests for the combustor aero model."""

    sys = Combustor("comb")

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 100.0
        sys.run_drivers()

        assert sys.Tcomb == pytest.approx(743.7, rel=1e-2)

    def test_solver(self):
        sys = self.sys

        run = sys.add_driver(NonLinearSolver("run"))
        run.add_unknown("fuel_W")
        run.add_equation("Tcomb == 1000.")

        sys.run_drivers()

        assert sys.Tcomb == pytest.approx(1000.0, rel=1e-2)

    def test_view(self):
        sys = Combustor("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
