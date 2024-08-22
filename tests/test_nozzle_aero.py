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
        data_inwards = ["pamb", "area_in", "area_exit", "area"]
        data_output = ["fl_out"]
        data_outwards = ["thrust", "ps", "mach", "speed"]

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

        run.add_unknown("area", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        ps_out = max(
            sys.fl_in.Pt * ((2 / (sys.gamma + 1)) ** (sys.gamma / (sys.gamma - 1))), sys.pamb
        )
        ps_in = sys.fl_in.Pt - 0.5 * (sys.fl_in.W**2) / (sys.density * (sys.area_in**2))

        ts_in = sys.fl_in.Tt / (1 + (((sys.gamma - 1) / 2) * (sys.mach**2)))

        ts_out = sys.fl_out.Tt / (1 + (((sys.gamma - 1) / 2) * (sys.mach**2)))

        assert sys.fl_out.Pt == ps_out - 0.5 * sys.density * (sys.speed**2)
        assert (ts_in / ts_out) ** (sys.gamma / (sys.gamma - 1)) == ps_in / ps_out
        assert sys.speed == (
            ((574 / 0.029) * (sys.gamma / (sys.gamma - 1))) * (ts_in - ts_out)
        ) ** (0.5)
