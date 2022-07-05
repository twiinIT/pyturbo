# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

import numpy as np
from OCC.Core.TopoDS import TopoDS_Shape
from pyoccad.create import CreateAxis, CreateBezier, CreateEdge, CreateRevolution, CreateTopology

from pyturbo.systems.generic import GenericSimpleGeom
from pyturbo.systems.structures.channel import Channel
from pyturbo.systems.structures.channel_aero import ChannelAero
from pyturbo.utils import rz_to_3d, slope_to_3d


class FanDuctGeom(GenericSimpleGeom):
    def setup(self):
        super().setup()

        self.add_inward("core_cowl_slope", -20.0, unit="deg", desc="core cowl slope")
        self.add_inward("exit_tip_slope", 15.0, unit="deg", desc="exit tip slope")

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        b1 = CreateBezier.g1_relative_tension(
            rz_to_3d(self.kp.inlet_hub),
            rz_to_3d(self.kp.exit_hub),
            (0.0, 0.0, 1.0),
            slope_to_3d(self.core_cowl_slope),
            1.0,
            1.0,
        )
        b2 = CreateBezier.g1_relative_tension(
            rz_to_3d(self.kp.inlet_tip),
            rz_to_3d(self.kp.exit_tip),
            (0.0, 0.0, 1.0),
            (-np.sin(np.radians(self.exit_tip_slope)), 0.0, 1.0),
            1.0,
            1.0,
        )

        e1 = CreateEdge.from_curve(b1)
        e2 = CreateEdge.from_curve(b2)

        inner_shell = CreateRevolution.surface_from_curve(e1, CreateAxis.oz())
        outer_shell = CreateRevolution.surface_from_curve(e2, CreateAxis.oz())

        return CreateTopology.make_compound(inner_shell, outer_shell)


class FanDuct(Channel):
    """
    Fan duct

    """

    def setup(self, geom_class=FanDuctGeom, aero_class=ChannelAero):
        if geom_class is not None:
            self.add_child(geom_class("geom"), pulling=["kp", "core_cowl_slope"])
        if aero_class is not None:
            self.add_child(aero_class("aero"), pulling=["fl_in", "fl_out"])
