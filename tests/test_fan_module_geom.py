# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import numpy.testing as npt

from pyturbo.systems.fan_module import FanModuleGeom


class TestFanModuleGeom:
    """Define tests for the fan geometric model."""

    sys = FanModuleGeom("fm")
    radius = 2 * 1.35
    length = 0.5

    sys.kp.inlet_tip[0] = radius
    sys.kp.exit_hub[1] = length
    sys.kp.exit_tip = np.r_[radius, length]

    sys.fan_length_ratio = 0.4
    sys.booster_length_ratio = 0.4
    sys.booster_radius_ratio = 0.5
    sys.shaft_radius_ratio = 0.1

    sys.run_once()

    def test_run_once_fan(self):
        sys = self.sys

        fan_r = self.radius

        splitter_gap = sys.fan_to_splitter_axial_gap * self.radius * 2
        length = self.length * sys.fan_length_ratio + splitter_gap

        npt.assert_almost_equal(sys.fan_kp.inlet_hub, [0.0, 0.0])
        npt.assert_almost_equal(sys.fan_kp.inlet_tip, [fan_r, 0.0])
        npt.assert_almost_equal(sys.fan_kp.exit_hub, [0.0, length])
        npt.assert_almost_equal(sys.fan_kp.exit_tip, [fan_r, length])

    def test_run_once_shaft(self):
        sys = self.sys
        inlet_z = sys.fan_kp.exit_hub_z
        shaft_r = self.radius * sys.shaft_radius_ratio
        length = self.length

        npt.assert_almost_equal(sys.shaft_kp.inlet_hub, [0.0, inlet_z])
        npt.assert_almost_equal(sys.shaft_kp.inlet_tip, [shaft_r, inlet_z])
        npt.assert_almost_equal(sys.shaft_kp.exit_hub, [0.0, length])
        npt.assert_almost_equal(sys.shaft_kp.exit_tip, [shaft_r, length])

    def test_run_once_booster(self):
        sys = self.sys
        npt.assert_almost_equal(sys.booster_kp.inlet_hub, sys.shaft_kp.inlet_tip)
        npt.assert_almost_equal(sys.booster_kp.inlet_tip, sys.ogv_kp.inlet_hub)
        npt.assert_almost_equal(sys.booster_kp.exit_hub, sys.ic_kp.inlet_hub)
        npt.assert_almost_equal(sys.booster_kp.exit_tip, sys.ogv_kp.exit_hub)

    def test_run_once_ogv(self):
        sys = self.sys

        npt.assert_almost_equal(sys.ogv_kp.inlet_hub, sys.booster_kp.inlet_tip)
        npt.assert_almost_equal(sys.ogv_kp.inlet_tip, sys.fan_kp.exit_tip)
        npt.assert_almost_equal(sys.ogv_kp.exit_hub, sys.booster_kp.exit_tip)
        npt.assert_almost_equal(
            sys.ogv_kp.exit_tip, [sys.fan_kp.inlet_tip_r, sys.booster_kp.exit_hub_z]
        )

    def test_run_once_ic(self):
        sys = self.sys
        npt.assert_almost_equal(sys.ic_kp.inlet_hub, sys.booster_kp.exit_hub)
        npt.assert_almost_equal(sys.ic_kp.inlet_tip, sys.ogv_kp.exit_tip)
        npt.assert_almost_equal(sys.ic_kp.exit_hub, sys.shaft_kp.exit_tip)
        npt.assert_almost_equal(
            sys.ic_kp.exit_tip, [sys.fan_kp.inlet_tip_r, sys.shaft_kp.exit_hub_z]
        )
