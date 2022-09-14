import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.mixers import MixerShaft


class TestShaft:
    """Define tests for the mixer shaft model."""

    s = MixerShaft("shaft", input_shafts=["in0", "in1"], output_shafts=["out0", "out1"])

    def test_system_setup(self):
        # default constructor
        s = self.s
        assert "in0" in s.inputs
        assert "out1" in s.outputs

    def test_run_once(self):
        s = self.s

        s.in0.N = 4000
        s.in1.N = 6000
        s.in0.power = 1e6
        s.in1.power = 3e6
        s.power_fractions = np.r_[0.75]

        s.run_once()

        assert s.power_fractions == [0.75]
        assert s.out1.N == 5000.0
        assert s.out0.power == 3e6
        assert s.out1.power == 1e6

    def test_run_solver(self):
        s = self.s
        run = s.add_driver(NonLinearSolver("run"))
        run.add_unknown("in0.N").add_equation("out0.power == 1e6")

        s.in0.N = 4000
        s.in1.N = 5000
        s.in0.power = 1e6
        s.in1.power = 2e6

        s.run_drivers()

        assert s.out1.N == pytest.approx(5000.0, abs=1.0)
        assert s.out0.power == pytest.approx(1e6, abs=1.0)
