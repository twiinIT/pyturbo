# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems import Combustor


class TestCombustor:
    """Define tests for the combustor aero model."""

    sys = Combustor("comb")

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 100.0
        sys.run_drivers()

        assert sys.Tcomb == pytest.approx(743.7, rel=1e-2)
