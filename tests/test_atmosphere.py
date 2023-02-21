# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems import Atmosphere


class TestAtmosphere:
    """Tests for the Atmosphere model."""

    atm = Atmosphere("atm")

    def test_sea_level_static(self):
        atm = self.atm

        atm.altitude = 0.0
        atm.mach = 0.0
        atm.dtamb = 0.0
        atm.run_drivers()

        assert atm.Pt == 101325.0
        assert atm.Tt == 288.15
        assert atm.pamb == 101325.0
