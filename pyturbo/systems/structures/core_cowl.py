# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape
from pyoccad.create import CreateAxis, CreateBezier, CreateEdge, CreateRevolution

from pyturbo.ports import C1Keypoint
from pyturbo.utils import rz_to_3d


class CoreCowl(System):
    def setup(self):
        self.add_inward("inlet_kp", C1Keypoint(), desc="inlet keypoint")
        self.add_inward("exit_kp", C1Keypoint(), desc="exit keypoint")

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        b = CreateBezier.g1_relative_tension(
            rz_to_3d(self.inlet_kp.rz),
            rz_to_3d(self.exit_kp.rz),
            rz_to_3d(self.inlet_kp.drdz),
            rz_to_3d(self.exit_kp.drdz),
            1.0,
            1.0,
        )

        e = CreateEdge.from_curve(b)

        return CreateRevolution.surface_from_curve(e, CreateAxis.oz())
