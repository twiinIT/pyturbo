# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

import pyturbo.systems.turbofan.data as tf_data
from pyturbo.systems.turbofan import Turbofan
from pyturbo.thermo import init_environment
from pyturbo.utils import load_from_json


class TestTurbofan:
    """Define tests for the turbofan assembly system."""

    sys = Turbofan("tf")

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 300.0
        sys.fuel_W = 1.0
        sys.fan_module.splitter_fluid.fluid_fractions[0] = 0.8

        sys.run_once()

        assert sys.fan_module.fan.fl_out.W == pytest.approx(240.0, 1e-3)
        assert sys.fan_module.booster.fl_out.W == pytest.approx(60.0, 1e-3)

    def test_init_environment(self):
        sys = self.sys
        sys.pamb = 0.0

        init_environment(sys, mach=0.0, dtamb=0.0, alt=0.0)

        assert sys.pamb == 101325.0

    def test_run_CFM(self):
        sys = Turbofan("sys")
        load_from_json(sys, Path(tf_data.__file__).parent / "turbofan_default.json")
        init_environment(sys, mach=0.0, dtamb=15.0, alt=0.0)

        solver = sys.add_driver(NonLinearSolver("solver", tol=1e-6))

        # run solver
        sys.run_drivers()

        assert np.linalg.norm(solver.problem.residue_vector()) < 1e-6
        assert pytest.approx(sys.sfc, rel=0.1) == 0.4

    def test_run_design_method(self):
        sys = Turbofan("sys")
        load_from_json(sys, Path(tf_data.__file__).parent / "turbofan_default.json")
        init_environment(sys, mach=0.0, dtamb=15.0, alt=0.0)

        design = sys.add_driver(NonLinearSolver("solver", tol=1e-6))

        # pure scaling
        design.extend(sys.design_methods["scaling"])
        sys.run_drivers()
        assert np.linalg.norm(design.problem.residue_vector()) < 1e-6

    def test_calib(self):
        """Calibration of CMF56-7 turbofan."""
        # Create a new turbofan system
        sys = Turbofan("sys")
        solver = sys.add_driver(NonLinearSolver("nls", tol=1e-6))

        # cfm
        load_from_json(sys, Path(tf_data.__file__).parent / "turbofan_default.json")
        init_environment(sys, mach=0.0, dtamb=15.0, alt=0.0)

        # engine functional requirements
        solver.add_equation("thrust == 90e3")
        solver.add_equation("fan_module.fan.aero.pr == 1.6")
        solver.add_equation("bpr == 5.0")
        solver.add_equation("opr == 25.0")
        solver.add_equation("N2 == 15000.")
        solver.add_equation("N1 == 5000.")
        solver.add_equation("fan_module.booster.aero.pr == 1.8")
        solver.add_equation("turbine.fl_in.Tt == 1300.")

        # design
        solver.add_unknown("fuel_W")
        solver.add_unknown("geom.sec_nozzle_area_ratio")
        solver.add_unknown("geom.pri_nozzle_area_ratio")
        solver.add_unknown("core.turbine.geom.blade_height_ratio")
        solver.add_unknown("core.compressor.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("fan_module.fan.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("fan_module.booster.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("turbine.geom.blade_height_ratio")

        sys.run_drivers()

        assert np.linalg.norm(solver.problem.residue_vector()) < 1e-6

    def test_cfm56_init_env(self):
        """Calibration of CMF56-7 turbofan."""
        # Create a new turbofan system
        sys = Turbofan("sys")
        solver = sys.add_driver(NonLinearSolver("nls", tol=1e-6))
        init_environment(sys, mach=0.0, dtamb=15.0, alt=0.0)

        # cfm
        load_from_json(sys, Path(tf_data.__file__).parent / "turbofan_default.json")

        # engine functional requirements
        solver.add_equation("thrust == 90e3")
        solver.add_equation("fan_module.fan.aero.pr == 1.6")
        solver.add_equation("bpr == 5.0")
        solver.add_equation("opr == 25.0")
        solver.add_equation("N2 == 15000.")
        solver.add_equation("N1 == 5000.")
        solver.add_equation("fan_module.booster.aero.pr == 1.8")
        solver.add_equation("turbine.fl_in.Tt == 1300.")

        # design
        solver.add_unknown("fuel_W")
        solver.add_unknown("geom.sec_nozzle_area_ratio")
        solver.add_unknown("geom.pri_nozzle_area_ratio", max_rel_step=0.9)
        solver.add_unknown("core.turbine.geom.blade_height_ratio")
        solver.add_unknown("core.compressor.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("fan_module.fan.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("fan_module.booster.aero.phiP", max_rel_step=0.9)
        solver.add_unknown("turbine.geom.blade_height_ratio")

        sys.run_drivers()

        assert np.linalg.norm(solver.problem.residue_vector()) < 1e-6
