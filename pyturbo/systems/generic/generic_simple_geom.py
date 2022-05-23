# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape
from pyoccad.create import CreateAxis, CreateRevolution, CreateTopology, CreateWire

from pyturbo.ports import KeypointsPort
from pyturbo.utils import rz_to_3d


class GenericSimpleGeom(System):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):
        # inwards/outwards
        self.add_input(KeypointsPort, "kp")

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        w = CreateWire.from_points(
            (
                rz_to_3d(self.kp.inlet_hub),
                rz_to_3d(self.kp.exit_hub),
                rz_to_3d(self.kp.exit_tip),
                rz_to_3d(self.kp.inlet_tip),
            ),
            auto_close=True,
        )

        shell = CreateRevolution.surface_from_curve(w, CreateAxis.oz())
        return dict(geom=CreateTopology.make_compound(shell))
