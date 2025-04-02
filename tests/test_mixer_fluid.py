# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.mixers import MixerFluid


class TestMixerFluid:
    """Define tests for the mixer aero model."""

    s = MixerFluid("aero", input_fluids=["in0", "in1"], output_fluids=["out0", "out1"])

    def test_run_once(self):
        s = self.s

        s.in0.Pt = 4000.0
        s.in1.Pt = 6000.0
        s.in0.W = 3.0
        s.in1.W = 1.0
        s.fluid_fractions = np.r_[0.25]

        s.run_once()

        assert s.fluid_fractions == [0.25]
        assert s.W == 4.0
        assert s.Pt == pytest.approx(5000.0, rel=0.01)
        assert s.out0.W == 1.0
        assert s.out1.W == 3.0
        assert s.out1.Pt == 5000.0

    def test_run_solver(self):
        s = self.s
        run = s.add_driver(NonLinearSolver("run"))
        run.add_unknown("in0.Pt").add_equation("out0.W == 1.")

        s.in0.Pt = 4000.0
        s.in1.Pt = 6000.0
        s.in0.W = 3.0
        s.in1.W = 1.0

        s.run_drivers()

        assert s.out1.Pt == pytest.approx(6000.0, abs=1.0)
        assert s.out0.W == pytest.approx(1.0, abs=0.01)
