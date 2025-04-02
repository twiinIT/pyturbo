# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems.turbofan import TurbofanWeight


class TestTurbofanWeight:
    """Define tests for the turbofan weight model."""

    tfw = TurbofanWeight("tfw")

    def test_ref(self):

        tfw = self.tfw

        tfw.fan_diameter = 1.98
        tfw.eis = 2015
        tfw.length = 3.328

        tfw.run_once()

        assert pytest.approx(tfw.weight, rel=5e-2) == 2990.0
