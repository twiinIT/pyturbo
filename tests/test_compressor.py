# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import HPC, Booster, Fan
from pyturbo.systems.compressor.compressor import Compressor


class TestCompressor:
    """Define tests for the compressor assembly system."""

    def test_system_setup(self):
        # default constructor
        sys = Compressor("cmp")

        data_input = ["fl_in", "sh_in"]
        data_inward = []
        data_output = ["fl_out"]
        data_outward = []

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    @pytest.mark.skip("not relevant")
    def test_compute_fan(self):
        sys = Fan("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(4517.0, rel=1e-2)
        assert sys.pr == pytest.approx(1.69, rel=1e-2)

    @pytest.mark.skip("not relevant")
    def test_compute_hpc(self):
        sys = HPC("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(16972.0, rel=1e-2)
        assert sys.pr == pytest.approx(8.95, rel=1e-2)

    @pytest.mark.skip("not relevant")
    def test_compute_booster(self):
        sys = Booster("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("sh_in.N")

        sys.run_drivers()

        assert sys.sh_in.N == pytest.approx(4890.0, rel=1e-2)
        assert sys.pr == pytest.approx(1.37, rel=1e-2)
