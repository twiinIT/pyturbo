# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import CompressorSimpleAero, CompressorSimpleGeom
from pyturbo.systems.compressor import CompressorSimple


class TestCompressorSimpleAero:
    def test_setup(self):
        # default constructor
        sys = CompressorSimpleAero("cmp")

        data_input = ["fl_in", "shaft_in"]
        data_inward = ["tip_in_r", "inlet_area", "eff_poly", "phiP"]
        data_output = ["fl_out"]
        data_outward = ["phi", "psi"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimpleAero("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("shaft_in.power")

        sys.tip_in_r = 0.8
        sys.tip_out_r = 0.8
        sys.inlet_area = np.pi * sys.tip_in_r**2 * (1 - 0.3**2)
        sys.shaft_in.N = 5500
        sys.shaft_in.power = 5e6

        sys.fl_in.W = 300.0
        sys.fl_in.pt = 1e5
        sys.fl_in.Tt = 288.15

        sys.phiP = 0.4
        sys.eff_poly = 0.8

        sys.run_drivers()

        assert sys.shaft_in.power == pytest.approx(16.8e6, rel=1e-2)


class TestCompressorSimpleGeom:
    def test_setup(self):
        # default constructor
        sys = CompressorSimpleGeom("sys")

        data_outward = ["tip_in_r", "tip_out_r", "inlet_area"]

        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimpleGeom("sys")

        sys.kp.inlet_hub = np.r_[0.5, 0.0]
        sys.kp.inlet_tip = np.r_[1.0, 0.0]
        sys.kp.exit_hub = np.r_[0.5, 1.0]
        sys.kp.exit_tip = np.r_[1.5, 1.0]

        sys.compute()
        assert sys.inlet_area == pytest.approx(np.pi * (1 - 0.5**2), abs=1e-6)
        assert sys.tip_in_r == 1.0
        assert sys.tip_out_r == 1.5


class TestCompressorSimple:
    def test_setup(self):
        # default constructor
        sys = CompressorSimple("cmp")

        data_input = ["fl_in", "shaft_in"]
        data_inward = []
        data_output = ["fl_out"]
        data_outward = []

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimple("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("shaft_in.power")

        # CFM56-3B
        sys.kp.inlet_hub = np.r_[0.8, 0.0] * 0.3
        sys.kp.inlet_tip = np.r_[0.8, 0.0]

        sys.kp.exit_hub = np.r_[0.8, 1.0] * 0.6  # no impact
        sys.kp.exit_tip = np.r_[0.8, 1.0]

        sys.shaft_in.N = 5500
        sys.shaft_in.power = 5e6

        sys.fl_in.W = 300.0
        sys.fl_in.pt = 1e5
        sys.fl_in.Tt = 288.15

        sys.aero.phiP = 0.4
        sys.aero.eff_poly = 0.8

        sys.run_drivers()

        assert sys.shaft_in.power == pytest.approx(16.8e6, rel=1e-2)
