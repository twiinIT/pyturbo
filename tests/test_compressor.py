# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause


import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems.compressor import Compressor


class TestCompressor:
    """Define tests for the compressor assembly system."""

    def test_compute_fan(self):
        sys = Compressor("cmp", config="fan")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(5146.4, rel=1e-2)
        assert sys.pr == pytest.approx(1.69, rel=1e-2)

    def test_compute_hpc(self):
        sys = Compressor("cmp", config="hpc")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(28762.5, rel=1e-2)
        assert sys.pr == pytest.approx(8.95, rel=1e-2)

    def test_compute_booster(self):
        sys = Compressor("cmp", config="booster")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(3909.5, rel=1e-2)
        assert sys.pr == pytest.approx(1.37, rel=1e-2)
