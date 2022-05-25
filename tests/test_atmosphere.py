# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems.atmosphere import Atmosphere


class TestAtmosphere:
    def test_compute(self):
        atm = Atmosphere("atm")

        atm.altitude = 0.0
        atm.mach = 0.0

        atm.run_once()
        assert atm.fl_out.Tt == 288.15
        assert atm.fl_out.pt == 101325.0
        assert atm.ps == 101325.0

        atm.altitude = 11000.0
        atm.mach = 0.0

        atm.run_once()
        assert atm.fl_out.pt == pytest.approx(20556.0, abs=1.0)
        assert atm.ps == pytest.approx(20556.0, abs=1.0)
        assert atm.fl_out.Tt == pytest.approx(216.6, abs=0.1)

        atm.altitude = 11000.0
        atm.mach = 0.8

        atm.run_once()
        assert atm.ps == pytest.approx(20556.0, abs=1.0)
        assert atm.fl_out.pt == pytest.approx(31338.0, abs=1.0)
        assert atm.fl_out.Tt == pytest.approx(244.4, abs=0.1)
