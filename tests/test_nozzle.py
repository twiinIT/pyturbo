# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
import numpy as np
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.nozzle import Nozzle, NozzleAero


class TestNozzle:
    """Define tests for the nozzle."""

    def test_system_setup(self):
        # default constructor
        sys = Nozzle("noz")

        data_input = ["kp", "fl_in"]
        data_inwards = []
        data_output = []
        data_outwards = ["thrust"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_outwards:
            assert data in sys.outwards
        for data in data_inwards:
            assert data in sys.inwards

    @pytest.mark.skip("not relevant")
    def test_run_once(self):
        # basic run
        sys = Nozzle("noz")

        sys.fl_in.W = 400.0
        sys.pamb = 1e5
        sys.run_once()

        assert sys.thrust == pytest.approx(30093.0, 0.1)

    def test_run_solver(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("m2", max_rel_step=0.1)
        run.add_unknown("mach", max_rel_step=0.1)

        sys.area_exit = 0.0225 * np.pi
        sys.area = sys.area_exit  # if throat area = exit area, converging nozzle
        sys.area_in = 0.0625 * np.pi
        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        # assert sys.speed == pytest.approx(308.3, 0.01)  # Initial way for Nozzle calculation
        assert sys.speed == pytest.approx(407.5, 0.01)  # New way for Nozzle calculation
        # assert sys.mach == pytest.approx(0.7, 0.01)  # Initial way for Nozzle calculation
        assert sys.mach == pytest.approx(0.97, 0.01)  # New way for Nozzle calculation
        # assert sys.thrust == pytest.approx(9250.0, 0.01)  # Initial way for Nozzle calculation
        assert sys.thrust == pytest.approx(10669.9, 0.01)  # New way for Nozzle calculation
        # assert sys.area == pytest.approx(0.133, 0.01)  # Initial way for Nozzle calculation
        # assert sys.area_exit == pytest.approx(0.07, 0.01)  # New way for Nozzle calculation
