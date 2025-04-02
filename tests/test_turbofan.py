# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import pytest
from cosapp.drivers import NonLinearSolver

import pyturbo.systems.turbofan.data as tf_data
from pyturbo.systems.turbofan import Turbofan
from pyturbo.utils import load_from_json


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
        sys = Turbofan("sys")
        load_from_json(sys, Path(tf_data.__file__).parent / "CFM56_7_geom.json")
        load_from_json(sys, Path(tf_data.__file__).parent / "CFM56_7_design_data.json")

        sys.add_driver(NonLinearSolver("solver", tol=1e-6))

        # run solver
        sys.run_drivers()

        assert pytest.approx(sys.sfc, rel=0.1) == 0.4

    def test_run_design_method(self):
        sys = Turbofan("sys")

        design = sys.add_driver(NonLinearSolver("solver", tol=1e-6))

        # run solver
        sys.run_drivers()

        # pure scaling
        design.extend(sys.design_methods["scaling"])
        sys.run_drivers()

        # tuning bpr
        design.extend(sys.design_methods["tuning_bpr"])

        sys.bpr = bpr = 5.0

        sys.run_drivers()

        assert pytest.approx(sys.bpr) == bpr

        # tuning thrust
        design.extend(sys.design_methods["tuning_thrust"])

        sys.thrust = thrust = 100e3

        sys.run_drivers()

        assert pytest.approx(sys.thrust) == thrust
        assert pytest.approx(sys.bpr) == bpr
        assert pytest.approx(sys.fan_diameter, rel=0.1) == 1.65

    def test_view(self):
        sys = Turbofan("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
