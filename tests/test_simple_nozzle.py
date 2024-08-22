# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.nozzle.simple_nozzle_vin import SimpleNozzle


class TestNozzle:
    """Define tests for the nozzle."""

    def test_system_setup(self):
        # default constructor
        sys = SimpleNozzle("noz")

        data_input = ["F_in", "inwards"]
        data_inwards = ["S_inlet", "P_atm", "S_outlet", "gamma", "R"]
        data_output = ["F_out", "outwards"]
        data_outwards = [
            "rho_inlet",
            "rho_outlet",
            "speed_outlet",
            "Thrust",
            "Mach_inlet",
            "Mach_outlet",
        ]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_outwards:
            assert data in sys.outwards
        for data in data_inwards:
            assert data in sys.inwards

    # # @pytest.mark.skip("not relevant")
    def test_run_once(self):
        # basic run
        sys = SimpleNozzle("noz")

        sys.F_in.W = 400.0
        sys.P_atm = 1e5
        sys.run_once()

        print(sys.F_out.Tt)
        assert sys.Mach_in == pytest.approx(0.1375, 0.01)

    #     assert False

    #     assert sys.F_out.Tt == pytest.approx(287.06, 0.01)
    #     assert sys.F_out.Pt == pytest.approx(99995.07, 0.01)
    #     assert sys.rho_inlet == pytest.approx(1.225, 0.01)
    #     assert sys.rho_outlet == pytest.approx(1.213, 0.01)
    #     assert sys.speed_outlet == pytest.approx(46.7, 0.01)
    #     assert sys.F_out.W == pytest.approx(113.34, 0.01)
    #     # assert sys.Thrust == pytest.approx(6216.98, 0.01)

    # def test_run_solver(self):
    #     # basic run
    #     sys = SimpleNozzle("noz")
    #     run = sys.add_driver(NonLinearSolver("run"))

    #     run.add_unknown("S_outlet", max_rel_step=0.1)
    #     run.add_equation("Thrust == 20")  # Pratt and Whitney 156 kN de poussée

    #     sys.F_in.Tt = 530.0
    #     sys.F_in.Pt = 1.405e5
    #     sys.F_in.W = 30.0
    #     sys.P_atm = 1e5
    #     sys.run_drivers()

    #     print("SECTION DE SORTIE : ", sys.speed_outlet)
    #     # assert sys.S_outlet == pytest.approx(2, 0.01)
    #     assert False
    #     # assert sys.speed == pytest.approx(308.3, 0.01)
    #     # assert sys.mach == pytest.approx(0.7, 0.01)
    #     # assert sys.thrust == pytest.approx(9250.0, 0.01)
    #     # assert sys.area == pytest.approx(0.133, 0.01)
