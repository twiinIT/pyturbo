# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.base import System

from pyturbo.systems.channel import ChannelAero
from pyturbo.systems.duct.fan_duct_geom import FanDuctGeom


class FanDuct(System):
    """Fan duct assembly system."""

    def setup(self):
        self.add_child(FanDuctGeom("geom"), pulling=["kp", "core_cowl_slope"])
        self.add_child(ChannelAero("aero"), pulling=["fl_in", "fl_out"])
