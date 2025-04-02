# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import pytest
from cosapp.drivers import NonLinearSolver

import pyturbo.systems.turbofan.data as tf_data
from pyturbo.systems.turbofan import Turbofan


class TestTurbofan:
    """Define tests for the turbofan assembly system."""

    sys = Turbofan("tf")

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 300.0
        sys.fuel_W = 1.0
        sys.fan_module.splitter_fluid.fluid_fractions[0] = 0.8

        sys.run_once()

        assert sys.fan_module.fan.fl_out.W == pytest.approx(240.0, 1e-3)
        assert sys.fan_module.booster.fl_out.W == pytest.approx(60.0, 1e-3)

    def test_run_CFM(self):
        assert Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

    @pytest.mark.skip("not relevant")
    def test_run_solver(self):
        sys = Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

        design = sys.add_driver(NonLinearSolver("solver", tol=1e-6, factor=0.2))
        sys.run_drivers()

        assert True

        design.add_unknown("fuel_W")
        design.add_target("thrust")
        design.design.extend(sys.design_methods["scaling"])

        sys.run_drivers()

        assert pytest.approx(sys.fan_diameter) == 1.549

        design = sys.add_driver(NonLinearSolver("solver", tol=1e-6))
        sys.run_drivers()

        design.add_unknown("fuel_W")
        design.add_target("thrust")
        sys.thrust = 85e3

        sys.run_drivers()

        assert pytest.approx(sys.sfc, rel=1e-2) == 0.37

    def test_run_design_method(self):
        sys = Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

        design = sys.add_driver(NonLinearSolver("solver", tol=1e-6, factor=0.2))
        sys.run_drivers()

        design.add_unknown("fuel_W")
        design.add_target("thrust")
        design.extend(sys.design_methods["scaling"])

        sys.thrust = 200e3

        sys.run_drivers()

        assert pytest.approx(sys.fan_diameter, rel=0.1) == 2.25

    def test_view(self):
        sys = Turbofan("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
