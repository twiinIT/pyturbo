# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
import numpy as np
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.nozzle import NozzleAero, Nozzle


class TestNozzleAero:
    """Define tests for the nozzle."""

    def test_system_setup(self):
        # default constructor
        sys = NozzleAero("noz")

        data_input = ["fl_in"]
        data_inwards = ["pamb", "area_in", "area_exit"]
        data_output = ["fl_out"]
        data_outwards = ["thrust", "speed"]

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

    def test_run_solver_converging_nozzle(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run", max_iter=2000, tol=1e-6))

        run.add_unknown("m2", max_rel_step=0.1)
        run.add_unknown("mach", max_rel_step=0.1)

        sys.area_exit = 0.0225 * np.pi
        sys.area = sys.area_exit  # if throat area = exit area, converging nozzle
        sys.area_in = 0.0625 * np.pi
        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 45.0
        sys.run_drivers()

        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        assert sys.fl_out.Tt == sys.fl_in.Tt
        assert sys.fl_out.Pt == sys.fl_in.Pt
        assert sys.mach <= 1.0
        assert sys.mach > sys.m1

    def test_run_solver_De_Laval_nozzle(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run", max_iter=2000, tol=1e-6))

        run.add_unknown("m2", max_rel_step=0.1)
        run.add_unknown("mach", max_rel_step=0.1)

        sys.area_exit = 0.16 * np.pi
        sys.area = 0.0225 * np.pi
        sys.area_in = 0.0625 * np.pi
        sys.pamb = 1.01e5
        sys.fl_in.Tt = 400.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 28.19342899746329

        sys.run_drivers()

        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        assert sys.fl_out.Tt == sys.fl_in.Tt
        assert sys.fl_out.Pt == sys.fl_in.Pt

        if sys.mach == pytest.approx(1, 0.05):
            assert sys.m2 > 1.0
            assert sys.m1 < sys.mach

        elif sys.mach < 1:
            assert sys.m2 < 1.0
            assert sys.m2 < sys.mach

        else:
            assert False

    def test_run_solver_De_Laval_nozzle_start(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run", max_iter=2000, tol=1e-6))

        run.add_unknown("m2", max_rel_step=0.1)
        run.add_unknown("mach", max_rel_step=0.1)

        sys.area_exit = 0.16 * np.pi
        sys.area = 0.0225 * np.pi
        sys.area_in = 0.0625 * np.pi
        sys.pamb = 1.01e5
        sys.fl_in.Tt = 400.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 10

        sys.run_drivers()

        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        assert sys.fl_out.Tt == sys.fl_in.Tt
        assert sys.fl_out.Pt == sys.fl_in.Pt

        if sys.mach == pytest.approx(1, 0.05):
            assert sys.m2 > 1.0
            assert sys.m1 < sys.mach

        elif sys.mach < 1:
            assert sys.m2 < 1.0
            assert sys.m2 < sys.mach

        else:
            assert False

    def test_run_solver_De_Laval_nozzle_stop(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run", max_iter=2000, tol=1e-6))

        run.add_unknown("m2", max_rel_step=0.1)
        run.add_unknown("mach", max_rel_step=0.1)

        sys.area_exit = 0.16 * np.pi
        sys.area = 0.0225 * np.pi
        sys.area_in = 0.0625 * np.pi
        sys.pamb = 1.01e5
        sys.fl_in.Tt = 400.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 50

        sys.run_drivers()

        assert sys.fl_in.W == pytest.approx(sys.fl_out.W)
        assert sys.fl_out.Tt == sys.fl_in.Tt
        assert sys.fl_out.Pt == sys.fl_in.Pt

        if sys.mach == pytest.approx(1, 0.1):
            assert sys.m2 > 1.0
            assert sys.m1 < sys.mach

        elif sys.mach < 1:
            assert sys.m2 < 1.0
            assert sys.m2 < sys.mach

        else:
            assert False
