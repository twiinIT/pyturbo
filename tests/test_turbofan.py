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

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["fl_in"]
        data_output = []
        data_inward = ["fan_diameter", "fuel_W", "pamb"]
        data_outward = ["thrust", "bpr", "opr", "sfc"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_outward:
            assert data in sys.outwards

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
        sys = self.sys
        run = sys.add_driver(NonLinearSolver("run"))

        sys.pamb = 1e5

        sys.fan_diameter = 1.8
        run.add_unknown("inlet.fl_in.W")

        sys.run_drivers()

        assert sys.bpr == pytest.approx(4.95, 0.01)
