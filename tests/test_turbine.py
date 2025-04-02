# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import pytest
from cosapp.drivers import NonLinearSolver

import pyturbo.systems.turbine.data as trb_data
from pyturbo.systems import Turbine


class TestTurbine:
    """Define tests for the turbine assembly model."""

    def setup_method(self):
        self.data_dir = Path(trb_data.__file__).parent

    def test_system_setup(self):
        # default constructor
        sys = Turbine("tur")

        data_input = ["fl_in", "kp"]
        data_inward = []
        data_output = ["fl_out", "sh_out"]
        data_outward = []

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute_HPT(self):
        sys = Turbine("tur", init_file=self.data_dir / "hpt.json")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 15000.").add_equation("aero.dhqt == 400.").add_unknown(
            "fl_in.W"
        )

        sys.run_drivers()
        assert sys.aero.Ncqdes == pytest.approx(101.0, rel=1e-2)

    def test_compute_LPT(self):
        sys = Turbine("tur", init_file=self.data_dir / "lpt.json")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 5000.").add_equation("aero.dhqt == 400.").add_unknown(
            "fl_in.W"
        )

        sys.run_drivers()
        assert sys.aero.Ncqdes == pytest.approx(105.0, rel=1e-2)
