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
        data_outwards = ["thrust", "Ps1", "M1", "speed"]

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

        # run.add_unknown("area", max_rel_step=0.1)
        run.add_unknown("area_exit", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        print("NOMBRE DE MACH À INLET : ", sys.M1)
        print(
            "VITESSE FLUIDE INLET",
            (sys.fl_in.W / (sys.rho_1 * sys.area_in)),
        )
        print(
            "VITESSE DU SON INLET",
            ((sys.gamma * 287 * sys.Ts1) ** 0.5),
        )
        print("TEMPÉRATURE STATIQUE ENTRÉE ISSUE DU SYSTÈME : ", sys.Ts1)
        print(
            "TEMPÉRATURE STATIQUE INLET RECALCULÉE",
            sys.fl_in.Tt
            + ((1 - sys.gamma) / (2 * sys.gamma * 287)) * (sys.fl_in.W / (sys.rho_1 * sys.area_in)),
        )
        print("NOMBRE DE MACH À LA SORTIE : ", sys.M2)
        print("POUSSÉE EN SORTIE DE TUYÈRE : ", sys.thrust)
        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        assert False
        # assert (sys.fl_in.W / (sys.rho_1 * sys.area_in)) / (
        #     (sys.gamma * 287 * sys.Ts1) ** 0.5
        # ) == pytest.approx(sys.M1)
        # assert sys.fl_out.Pt == sys.Ps2 - 0.5 * sys.rho_2 * (sys.v2**2)
        # assert (sys.Ts1 / sys.Ts2) ** (sys.gamma / (sys.gamma - 1)) == sys.Ps1 / sys.Ps2
        # assert sys.speed == (
        #     ((574 / 0.029) * (sys.gamma / (sys.gamma - 1))) * (sys.Ts1 - sys.Ts2)
        # ) ** (0.5)
