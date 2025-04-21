# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.compressor.physics import CompressorAero


class TestCompressorAero:
    """Define tests for the compressor aero model."""

    def test_fan(self):
        sys = CompressorAero("cmp")
        sys.add_driver(NonLinearSolver("run"))

        sys.tip_in_r = 0.8
        sys.tip_out_r = 0.8
        sys.inlet_area = np.pi * sys.tip_in_r**2 * (1 - 0.3**2)

        sys.eff_poly = 0.85
        sys.sh_in.N = 5500
        sys.sh_in.power = 17e6

        sys.fl_in.W = 308.3
        sys.fl_in.Pt = 101325.0
        sys.fl_in.Tt = 288.15

        sys.run_drivers()

        assert sys.pr == pytest.approx(1.68, rel=1e-2)
        assert sys.fl_out.Tt == pytest.approx(343.0, rel=1e-2)
