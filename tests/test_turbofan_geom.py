import numpy as np
import numpy.testing as npt
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.turbofan import TurbofanGeom


class TestTurbofanGeom:
    """Define tests for the turbofan geometric model."""

    @classmethod
    def setup_class(cls):
        cls.geom = geom = TurbofanGeom("tf")

        geom.fan_diameter = 2.0
        geom.fanmodule_length_ratio = 1.0
        geom.inlet_length_ratio = 0.4
        geom.inlet_radius_ratio = 0.9
        geom.core_radius_ratio = 0.25
        geom.core_length_ratio = 4.0
        geom.shaft_radius_ratio = 0.1
        geom.turbine_radius_ratio = 0.5
        geom.turbine_length_ratio = 1.0
        geom.trf_length_ratio = 0.5
        geom.frd_mount_relative = 0.75
        geom.aft_mount_relative = 0.5
        geom.pri_nozzle_area = 1.0
        geom.sec_nozzle_area = 1.0

        geom.run_once()

    def test_system_setup(self):
        data_output = ["fanmodule_kp", "core_kp", "shaft_kp", "turbine_kp", "trf_kp"]

        for data in data_output:
            assert data in self.geom.outputs

    def test_run_once_inlet(self):
        geom = self.geom

        npt.assert_almost_equal(geom.inlet_kp.inlet_hub, [0.0, -0.4])
        npt.assert_almost_equal(geom.inlet_kp.inlet_tip, [0.9, -0.4])
        npt.assert_almost_equal(geom.inlet_kp.exit_hub, [0.0, 0.0])
        npt.assert_almost_equal(geom.inlet_kp.exit_tip, [1.0, 0.0])

    def test_run_once_trf(self):
        geom = self.geom

        hub_radius = geom.turbine_fp_exit_hqt * geom.turbine_kp.exit_tip_r
        npt.assert_almost_equal(geom.trf_kp.inlet_hub, [hub_radius, 2.5])
        npt.assert_almost_equal(geom.trf_kp.inlet_tip, [0.5, 2.5])
        npt.assert_almost_equal(geom.trf_kp.exit_hub, [hub_radius, 2.75])
        npt.assert_almost_equal(geom.trf_kp.exit_tip, [0.5, 2.75])

    def test_run_once_turbine(self):
        geom = self.geom

        npt.assert_almost_equal(geom.turbine_kp.inlet_hub, [0.0, 2.0])
        npt.assert_almost_equal(geom.turbine_kp.inlet_tip, [0.25, 2.0])
        npt.assert_almost_equal(geom.turbine_kp.exit_hub, [0.0, 2.5])
        npt.assert_almost_equal(geom.turbine_kp.exit_tip, [0.5, 2.5])

    def test_run_once_shaft(self):
        geom = self.geom

        npt.assert_almost_equal(geom.shaft_kp.inlet_hub, [0.0, 1.0])
        npt.assert_almost_equal(geom.shaft_kp.inlet_tip, [0.1, 1.0])
        npt.assert_almost_equal(geom.shaft_kp.exit_hub, [0.0, 2.0])
        npt.assert_almost_equal(geom.shaft_kp.exit_tip, [0.1, 2.0])

    def test_run_once_fanmodule(self):
        geom = self.geom

        npt.assert_almost_equal(geom.fanmodule_kp.inlet_hub, [0.0, 0.0])
        npt.assert_almost_equal(geom.fanmodule_kp.inlet_tip, [1.0, 0.0])
        npt.assert_almost_equal(geom.fanmodule_kp.exit_hub, [0.0, 1.0])
        npt.assert_almost_equal(geom.fanmodule_kp.exit_tip, [1.0, 1.0])

    def test_run_once_gasgenerator(self):
        geom = self.geom

        npt.assert_almost_equal(geom.core_kp.inlet_hub, [0.1, 1.0])
        npt.assert_almost_equal(geom.core_kp.inlet_tip, [0.25, 1.0])
        npt.assert_almost_equal(geom.core_kp.exit_hub, [0.1, 2.0])
        npt.assert_almost_equal(geom.core_kp.exit_tip, [0.25, 2.0])

    @pytest.mark.skip("update test")
    def test_run_once_primary_nozzle(self):
        geom = self.geom

        npt.assert_almost_equal(geom.primary_nozzle_kp.exit_hub, [0.4, 3.0])
        npt.assert_almost_equal(
            geom.primary_nozzle_kp.exit_tip,
            [np.sqrt(1.0 / np.pi + geom.trf_kp.exit_hub_r**2), 2.75],
        )

    # TODO: update test
    @pytest.mark.skip("update test")
    def test_run_once_secondary_nozzle(self):
        pass

    def test_mount(self):
        geom = self.geom
        npt.assert_almost_equal(geom.frd_mount, [1.0, 0.75])
        npt.assert_almost_equal(geom.aft_mount, [0.5, 2.625])

    def test_solver(self):
        geom = self.geom

        geom.add_driver(NonLinearSolver("run"))
        geom.run_drivers()
