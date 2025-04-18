# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.nozzle import Nozzle, NozzleAero


class TestNozzle:
    """Define tests for the nozzle."""

    def test_run_solver(self):
        # basic run
        sys = NozzleAero("noz")
        run = sys.add_driver(NonLinearSolver("run"))

        run.add_unknown("area_exit", max_rel_step=0.1)

        sys.pamb = 1.01e5
        sys.fl_in.Tt = 530.0
        sys.fl_in.Pt = 1.405e5
        sys.fl_in.W = 30.0
        sys.run_drivers()

        assert np.linalg.norm(run.problem.residue_vector()) < 1e-6
        assert sys.speed == pytest.approx(308.3, 0.01)
        assert sys.mach == pytest.approx(0.7, 0.01)
        assert sys.thrust == pytest.approx(9250.0, 0.01)
        assert sys.area_exit == pytest.approx(0.133, 0.01)

    def test_view(self):
        sys = Nozzle("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
