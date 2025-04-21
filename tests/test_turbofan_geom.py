# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy.testing as npt

from pyturbo.systems.turbofan.physics import TurbofanGeom


class TestTurbofanGeom:
    """Define tests for the turbofan geometric model."""

    @classmethod
    def setup_class(cls):
        cls.geom = geom = TurbofanGeom("tf")

        geom.fan_diameter = 2.0
        geom.fan_module_length_ratio = 1.0
        geom.inlet_length_ratio = 0.4
        geom.inlet_radius_ratio = 0.9
        geom.core_inlet_radius_ratio = 0.25
        geom.core_exit_radius_ratio = 0.25
        geom.core_length_ratio = 4.0
        geom.shaft_radius_ratio = 0.1
        geom.turbine_radius_ratio = 0.5
        geom.turbine_length_ratio = 1.0
        geom.trf_length_ratio = 0.5
        geom.frd_mount_relative = 0.75
        geom.aft_mount_relative = 0.5
        geom.pri_nozzle_area_ratio = 0.9
        geom.sec_nozzle_area_ratio = 0.6

        geom.run_once()

    def test_run_once_inlet(self):
        geom = self.geom

        npt.assert_almost_equal(geom.inlet_kp.inlet_hub, [0.0, -0.4])
        npt.assert_almost_equal(geom.inlet_kp.inlet_tip, [0.9, -0.4])
        npt.assert_almost_equal(geom.inlet_kp.exit_hub, [0.0, 0.0])
        npt.assert_almost_equal(geom.inlet_kp.exit_tip, [1.0, 0.0])

    def test_run_once_trf(self):
        geom = self.geom

        hub_radius = geom.turbine_fp_exit_hqt * geom.turbine_kp.exit_tip_r
        inlet_z = geom.turbine_kp.exit_tip_z
        npt.assert_almost_equal(geom.trf_kp.inlet_hub, [hub_radius, inlet_z])
        npt.assert_almost_equal(geom.trf_kp.inlet_tip, [0.5, inlet_z])
        npt.assert_almost_equal(geom.trf_kp.exit_hub, [hub_radius, inlet_z + 0.25])
        npt.assert_almost_equal(geom.trf_kp.exit_tip, [0.5, inlet_z + 0.25])

    def test_run_once_turbine(self):
        geom = self.geom

        inlet_hub_z = geom.shaft_kp.exit_hub_z
        npt.assert_almost_equal(geom.turbine_kp.inlet_hub, [0.0, inlet_hub_z])
        npt.assert_almost_equal(geom.turbine_kp.inlet_tip, [0.3, inlet_hub_z])
        npt.assert_almost_equal(geom.turbine_kp.exit_hub, [0.0, inlet_hub_z + 0.5])
        npt.assert_almost_equal(geom.turbine_kp.exit_tip, [0.5, inlet_hub_z + 0.5])

    def test_run_once_shaft(self):
        geom = self.geom

        exit_z = geom.turbine_kp.inlet_hub_z
        npt.assert_almost_equal(geom.shaft_kp.inlet_hub, [0.0, 1.0])
        npt.assert_almost_equal(geom.shaft_kp.inlet_tip, [0.1, 1.0])
        npt.assert_almost_equal(geom.shaft_kp.exit_hub, [0.0, exit_z])
        npt.assert_almost_equal(geom.shaft_kp.exit_tip, [0.1, exit_z])

    def test_run_once_fan_module(self):
        geom = self.geom

        npt.assert_almost_equal(geom.fan_module_kp.inlet_hub, [0.0, 0.0])
        npt.assert_almost_equal(geom.fan_module_kp.inlet_tip, [1.0, 0.0])
        npt.assert_almost_equal(geom.fan_module_kp.exit_hub, [0.0, 1.0])
        npt.assert_almost_equal(geom.fan_module_kp.exit_tip, [1.0, 1.0])

    def test_run_once_gasgenerator(self):
        geom = self.geom

        npt.assert_almost_equal(geom.core_kp.inlet_hub, [0.1, 1.0])
        npt.assert_almost_equal(geom.core_kp.inlet_tip, [0.25, 1.0])
        npt.assert_almost_equal(geom.core_kp.exit_hub, [0.1, 2.0])
        npt.assert_almost_equal(geom.core_kp.exit_tip, [0.25, 2.0])

    def test_mount(self):
        geom = self.geom
        npt.assert_almost_equal(geom.frd_mount, [1.0, 0.75])
        npt.assert_almost_equal(geom.aft_mount, [0.5, 2.6625])
