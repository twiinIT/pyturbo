import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.turbofan import Turbofan


class TestTurbofan:
    """Define tests for the turbofan assembly system."""

    sys = Turbofan("tf")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["fl_in"]
        data_output = []
        data_inward = ["fan_diameter", "pamb", "fuel_W"]
        data_outward = ["thrust", "bpr", "opr", "sfc"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_outward:
            assert data in sys.outwards

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 300.0
        sys.fuel_W = 1.0
        sys.fan_module.splitter_fluid.fluid_fractions[0] = 0.2

        sys.run_once()

        assert sys.core.fl_out.W == pytest.approx(61.0, 1e-3)

    @pytest.mark.skip("not relevant")
    def test_run_solver(self):
        sys = self.sys
        run = sys.add_driver(NonLinearSolver("run"))

        sys.pamb = 1e5

        sys.fan_diameter = 1.8
        run.add_unknown("fl_in.W")

        sys.run_drivers()

        assert sys.bpr == pytest.approx(4.95, 0.01)
