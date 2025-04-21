# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems.fan_module import FanModule


class TestFanModule:
    """Define tests for the fan assembly module."""

    sys = FanModule("fm")

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.run_once()

        assert sys.fl_bypass.W == pytest.approx(280.0, 0.1)
        assert sys.fl_core.W == pytest.approx(70.0, 0.1)
