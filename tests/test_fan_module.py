import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.fan_module import FanModule


class TestFanModule:
    sys = FanModule("fm")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        inputs = ["fl_in", "sh_in"]
        inwards = ["fan_diameter", "length"]
        outputs = ["fl_core", "fl_bypass"]
        outwards = ["N"]

        for name in inputs:
            assert name in sys.inputs
        for name in inwards:
            assert name in sys.inwards
        for name in outputs:
            assert name in sys.outputs
        for name in outwards:
            assert name in sys.outwards

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.run_once()

        assert sys.fl_bypass.W == pytest.approx(280.0, 0.1)
        assert sys.fl_core.W == pytest.approx(70.0, 0.1)

    @pytest.mark.skip("not relevant")
    def test_solver(self):
        # basic solver
        sys = self.sys

        sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()

        assert sys.bpr == pytest.approx(5.12, abs=0.1)
        assert sys.booster.pr == pytest.approx(1.44, abs=0.1)
        assert sys.fan.pr == pytest.approx(1.66, abs=0.1)
