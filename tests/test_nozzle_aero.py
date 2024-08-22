# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.nozzle import NozzleAero


class TestNozzleAero:
    """Define tests for the nozzle."""

    def test_system_setup(self):
        # default constructor
        sys = NozzleAero("noz")

        data_input = ["fl_in"]
        data_inwards = ["pamb", "area_in", "area_exit"]
        data_output = ["fl_out"]
        data_outwards = ["thrust", "Ps1", "M1", "v2"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_outwards:
            assert data in sys.outwards
        for data in data_inwards:
            assert data in sys.inwards

    # @pytest.mark.skip("not relevant")
    # def test_run_once(self):
    #     # basic run
    #     sys = Nozzle("noz")

    #     sys.fl_in.W = 400.0
    #     sys.pamb = 1e5
    #     sys.run_once()

    #     assert sys.thrust == pytest.approx(30093.0, 0.1)

    def test_run_solver(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        # run.add_unknown("area", max_rel_step=0.1)S

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        assert sys.fl_out.Pt == sys.Ps2 - 0.5 * sys.rho_2 * (sys.v2**2)
        assert (sys.Ts1 / sys.Ts2) ** (sys.gamma / (sys.gamma - 1)) == sys.Ps1 / sys.Ps2
        assert sys.speed == (
            ((574 / 0.029) * (sys.gamma / (sys.gamma - 1))) * (sys.Ts1 - sys.Ts2)
        ) ** (0.5)
