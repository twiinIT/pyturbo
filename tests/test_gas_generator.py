# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems import GasGenerator


class TestGasGenerator:
    """Define tests for the gas generator assembly system."""

    def test_run_once(self):
        sys = GasGenerator("cmp")

        sys.fl_in.W = 80
        sys.fuel_W = 0.1
        sys.run_once()

        assert sys.fl_out.W == 80.1
