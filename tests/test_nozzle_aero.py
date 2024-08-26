# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import EulerExplicit, NonLinearSolver
from cosapp.utils import swap_system

from pyturbo.systems.nozzle import Nozzle
from pyturbo.systems.nozzle.nozzle_aero_advanced import NozzleAeroAdvConverging
from pyturbo.systems.turbofan import Turbofan


class TestNozzleAero:
    """Define tests for the nozzle."""

    def test_swap(self):
        sys = NozzleAeroAdvConverging("noz")
        tf = Turbofan("tf")

        tf.add_driver(NonLinearSolver("solver"))
        tf.run_drivers()

        thrust1 = tf.thrust
        swap_system(tf.primary_nozzle.aero, sys)
        tf.run_drivers()
        assert thrust1 == pytest.approx(tf.thrust, 0.01)

    def test_system_setup(self):
        # default constructor
        sys = NozzleAeroAdvConverging("noz")

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

    def test_run_solver(self):
        # basic run
        sys = NozzleAeroAdvConverging("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("area_exit", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        assert sys.speed == pytest.approx(308.3, 0.01)
        assert sys.mach == pytest.approx(0.7, 0.01)
        assert sys.thrust == pytest.approx(9250.0, 0.01)
        assert sys.area_exit == pytest.approx(0.133, 0.01)

    def test_run_simulation(self):
        # basic run
        sys = NozzleAeroAdvConverging("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        sys.pamb = 1.01e5
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
        sys = NozzleAeroAdvConverging("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        sys.pamb = 1.01e2
        sys.area_exit = 0.133
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.run_drivers()

        assert sys.mach == pytest.approx(1.0, 0.01)

    def test_run_transient(self):
        # basic run
        sys = NozzleAeroAdvConverging("noz")
        time_driver = sys.add_driver(EulerExplicit("euler_explicit", dt=0.1, time_interval=(0, 10)))
        run = time_driver.add_driver(NonLinearSolver("run"))

        run.add_unknown("fl_in.W", max_rel_step=0.1)

        time_driver.set_scenario(values={"pamb": "1.01e5 - 1e4 * time"})
        sys.area = 0.133
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.run_drivers()

        assert sys.mach == pytest.approx(1.0, 0.01)
