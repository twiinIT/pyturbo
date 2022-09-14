import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import Combustor


class TestCombustor:
    """Define tests for the combustor aero model."""

    sys = Combustor("comb")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["fl_in", "kp"]
        data_inward = ["fuel_W"]
        data_output = ["fl_out"]
        data_outward = ["Tcomb"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 100.0
        sys.run_drivers()

        assert sys.Tcomb == pytest.approx(743.7, rel=1e-2)

    def test_solver(self):
        sys = self.sys

        run = sys.add_driver(NonLinearSolver("run"))
        run.add_unknown("fuel_W")
        run.add_equation("Tcomb == 1000.")

        sys.run_drivers()

        assert sys.Tcomb == pytest.approx(1000.0, rel=1e-2)
