# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems.inlet import Inlet


class TestInlet:
    """Define tests for the inlet assembly model."""

    sys = Inlet("inlet")

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.pamb = 1e5
        sys.fl_in.W = 400.0
        sys.fl_in.Pt = 101325.0
        sys.fl_in.Tt = 300.0

        sys.run_once()

        assert sys.drag == pytest.approx(32000, 0.1)
