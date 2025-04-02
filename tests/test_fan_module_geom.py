# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy.testing as npt
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.fan_module import FanModuleGeom


class TestFanModuleGeom:
    """Define tests for the fan geometric model."""

    sys = FanModuleGeom("fm")

    def setup_method(self):
        sys = self.sys

        sys.length = 3.0
        sys.fan_diameter = 1.35
        sys.fan_length_ratio = 0.4
        sys.booster_length_ratio = 0.4
        sys.booster_radius_ratio = 0.5

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        inputs = []
        inwards = [
            "length",
            "fan_diameter",
            "fan_length_ratio",
            "fan_hub_radius_ratio",
            "booster_length_ratio",
            "booster_radius_ratio",
            "shaft_radius_ratio",
            "spinner_angle",
            "fan_to_splitter_axial_gap",
        ]
        outputs = ["fan_kp", "booster_kp", "ogv_kp", "ic_kp", "shaft_kp"]
        outwards = ["fan_hub_kp", "spinner_apex_kp", "fan_inlet_hub_kp"]

        for name in inputs:
            assert name in sys.inputs
        for name in inwards:
            assert name in sys.inwards
        for name in outputs:
            assert name in sys.outputs
        for name in outwards:
            assert name in sys.outwards

        sys.run_once()

    def test_run_once_fan(self):
        sys = self.sys
        fan_r = sys.fan_diameter / 2.0
        splitter_gap = sys.fan_to_splitter_axial_gap * sys.fan_diameter
        length = sys.length * sys.fan_length_ratio + splitter_gap

        npt.assert_almost_equal(sys.fan_kp.inlet_hub, [0.0, 0.0])
        npt.assert_almost_equal(sys.fan_kp.inlet_tip, [fan_r, 0.0])
        npt.assert_almost_equal(sys.fan_kp.exit_hub, [0.0, length])
        npt.assert_almost_equal(sys.fan_kp.exit_tip, [fan_r, length])

    def test_run_once_shaft(self):
        sys = self.sys
        inlet_z = sys.fan_kp.exit_hub_z
        shaft_r = sys.fan_diameter / 2.0 * sys.shaft_radius_ratio

        npt.assert_almost_equal(sys.shaft_kp.inlet_hub, [0.0, inlet_z])
        npt.assert_almost_equal(sys.shaft_kp.inlet_tip, [shaft_r, inlet_z])
        npt.assert_almost_equal(sys.shaft_kp.exit_hub, [0.0, 3.0])
        npt.assert_almost_equal(sys.shaft_kp.exit_tip, [shaft_r, 3.0])

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

    def test_solver(self):
        sys = self.sys
        sys.add_driver(NonLinearSolver("run"))
        sys.run_drivers()
