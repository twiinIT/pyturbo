import numpy as np
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.structures import IntermediateCasing
from pyturbo.systems.structures.channel import Channel


class TestChannel:
    """Define tests for the structure model."""

    sys = Channel("ch")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["kp", "fl_in"]
        data_output = ["fl_out"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.fl_in.Pt = 100.0
        sys.aero.pressure_loss = 0.01

        sys.run_once()

        assert sys.fl_out.Pt == 99.0


class TestIntermediateCasing:
    """Define tests for the intermediate casing model."""

    sys = IntermediateCasing("ic")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["kp", "fl_ogv", "fl_booster"]
        data_output = ["fl_bypass", "fl_core"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.kp.inlet_hub = np.r_[0.0, 2.0]
        sys.kp.inlet_tip = np.r_[1.0, 2.0]
        sys.kp.exit_hub = np.r_[0.0, 3.0]
        sys.kp.exit_tip = np.r_[1.0, 3.0]

        sys.primary_aero.pressure_loss = 0.01
        sys.secondary_aero.pressure_loss = 0.01

        sys.run_once()

    def test_solver(self):
        # basic solver
        sys = self.sys

        sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()
