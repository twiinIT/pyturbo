# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import EulerExplicit, NonLinearSolver

from pyturbo.systems.nozzle import NozzleAero


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

    def test_run_solver(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("area_exit", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        assert np.linalg.norm(run.problem.residue_vector()) < 1e-6
        assert sys.speed == pytest.approx(308.3, 0.01)
        assert sys.mach == pytest.approx(0.7, 0.01)
        assert sys.thrust == pytest.approx(9250.0, 0.01)
        assert sys.area_exit == pytest.approx(0.133, 0.01)

    def test_run_simulation(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.W = 30.0
        sys.area_exit = 0.133
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.run_drivers()

        assert sys.speed == pytest.approx(308.3, 0.01)
        assert sys.mach == pytest.approx(0.7, 0.01)
        assert sys.thrust == pytest.approx(9250.0, 0.01)
        assert sys.fl_in.W == pytest.approx(30.0, 0.01)

    def test_run_simulation_choked(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        sys.pamb = 1.01e2
        sys.fl_in.W = 30.0
        sys.area_exit = 0.133
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.run_drivers()

        sys2 = NozzleAero("noz2")
        run2 = sys2.add_driver(NonLinearSolver("run2"))

        run2.add_unknown("fl_in.W", max_rel_step=0.1)

        sys2.area = 0.133
        sys2.fl_in.Tt = 530.0
        sys2.fl_in.Pt = 1.405e5
        sys2.run_drivers()

        assert sys.mach == pytest.approx(1.0, 0.01)

    def test_run_transient(self):
        # basic run
        sys = NozzleAero("noz")
        time_driver = sys.add_driver(EulerExplicit("euler_explicit", dt=0.1, time_interval=(0, 10)))
        run = time_driver.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        time_driver.set_scenario(values={"pamb": "1.01e5 - 1e4 * time"})
        sys.area = 0.133
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.run_drivers()

        sys2 = NozzleAero("noz2")
        time_driver2 = sys2.add_driver(
            EulerExplicit("euler_explicit", dt=0.1, time_interval=(0, 10))
        )
        run2 = time_driver2.add_driver(NonLinearSolver("run2"))

        run2.add_unknown("fl_in.W", max_rel_step=0.1)

        time_driver2.set_scenario(values={"pamb": "1.01e5 - 1e4 * time"})
        sys2.area = 0.133
        sys2.fl_in.Tt = 530.0
        sys2.fl_in.Pt = 1.405e5
        sys2.run_drivers()

        assert sys.mach == pytest.approx(1.0, 0.01)
