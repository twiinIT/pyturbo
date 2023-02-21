# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import GasGenerator


class TestGasGenerator:
    """Define tests for the gas generator assembly system."""

    def test_system_setup(self):
        # default constructor
        sys = GasGenerator("core")

        data_input = ["fl_in", "kp"]
        data_inward = ["fuel_W"]
        data_output = ["fl_out"]
        data_outward = ["opr"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_run_once(self):
        sys = GasGenerator("cmp")

        sys.fl_in.W = 80
        sys.fuel_W = 0.1
        sys.run_once()

        assert sys.fl_out.W == 80.1

    @pytest.mark.skip("not relevant")
    def test_solver(self):
        sys = GasGenerator("core")
        sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()

        assert sys.opr == pytest.approx(16.4, rel=1e-2)
        assert sys.compressor.aero.sh_in.power == pytest.approx(28.5e6, rel=1e-2)
        assert sys.compressor.aero.sh_in.N == pytest.approx(5940, rel=1e-2)
