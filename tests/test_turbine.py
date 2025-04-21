# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import Turbine


class TestTurbine:
    """Define tests for the turbine assembly model."""

    def test_compute_HPT(self):
        sys = Turbine("tur", config="hpt")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 15000.").add_equation("aero.dhqt == 400.")

        sys.run_drivers()
        assert sys.aero.Ncqdes == pytest.approx(101.0, rel=1e-2)

    def test_compute_LPT(self):
        sys = Turbine("tur", config="lpt")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 5000.").add_equation("aero.dhqt == 400.")

        sys.run_drivers()
        assert sys.aero.Ncqdes == pytest.approx(105.0, rel=1e-2)
