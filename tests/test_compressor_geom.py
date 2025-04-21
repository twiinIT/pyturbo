# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest

from pyturbo.systems.compressor.physics.compressor_geom import CompressorGeom


class TestCompressorGeom:
    """Define tests for the compressor geometric model."""

    def test_compute(self):
        sys = CompressorGeom("sys")

        sys.kp.inlet_hub = np.r_[0.5, 0.0]
        sys.kp.inlet_tip = np.r_[1.0, 0.0]
        sys.kp.exit_hub = np.r_[0.5, 1.0]
        sys.kp.exit_tip = np.r_[1.5, 1.0]
        sys.blade_hub_to_tip_ratio = 0.5

        sys.compute()
        assert sys.inlet_area == pytest.approx(np.pi * 0.75, abs=1e-3)
        assert sys.tip_in_r == 1.0
        assert sys.tip_out_r == 1.5

    def test_compute_fan(self):
        sys = CompressorGeom("sys")

        sys.kp.inlet_hub = np.r_[0.5, 0.0]
        sys.kp.inlet_tip = np.r_[1.0, 0.0]
        sys.kp.exit_hub = np.r_[0.5, 1.0]
        sys.kp.exit_tip = np.r_[1.5, 1.0]
        sys.blade_hub_to_tip_ratio = 0.0

        sys.compute()
        assert sys.inlet_area == pytest.approx(np.pi, abs=1e-3)
        assert sys.tip_in_r == 1.0
        assert sys.tip_out_r == 1.5
