# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import GasGenerator


class TestGasGenerator:
    """Define tests for the gas generator assembly system."""

    def test_run_once(self):
        sys = GasGenerator("cmp")

        sys.fl_in.W = 80
        sys.fuel_W = 0.1
        sys.run_once()

        assert sys.fl_out.W == 80.1

    def test_solver(self):
        sys = GasGenerator("core")
        solver = sys.add_driver(NonLinearSolver("run"))

        sys.run_drivers()

        assert np.linalg.norm(solver.problem.residue_vector()) < 1e-6

    def test_view(self):
        sys = GasGenerator("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
