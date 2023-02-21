# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

import numpy as np
from OCC.Core.TopoDS import TopoDS_Shape
from pyoccad.create import CreateAxis, CreateBezier, CreateRevolution, CreateTopology, CreateWire

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom
from pyturbo.utils import rz_to_3d


class TurbineGeom(GenericSimpleGeom):
    """Turbine geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.
    The geometry exposed to aero module is made of:
    - inlet area
    - inlet and exit tip radius

    Inputs
    ------
    kp: KeypointsPort
        geometrical envelop

    stage_count: integer
        number of stages

    blade_height_ratio[-]: float, default=0.2
        inlet blade height relative to compressor inlet tip radius
    exit_hubqtip[-]: float, default=0.8
        exit hub-to-tip radius ratio

    Outputs
    -------
    mean_radius[m]: float, default=1.0
        mean radius
    fp_exit_hub_kp[m]: np.array(2), default=np.ones(2)
        flowpath exit hub keypoint
    area_in[m**2]: float, default=1.0
        inlet area
    """

    def setup(self):
        super().setup()

        self.add_inward("stage_count", 1)
        self.add_inward(
            "blade_height_ratio",
            0.2,
            unit="",
            desc="blade height relative to tip radius",
        )
        self.add_inward(
            "exit_hubqtip",
            0.8,
            unit="",
            desc="exit hub-to-tip radius ratio",
        )

        # aero outputs
        self.add_outward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("mean_radius", 1.0, unit="m", desc="mean radius")
        self.add_outward("fp_exit_hub_kp", np.ones(2), unit="m", desc="flowpath exit hub keypoint")

    def compute(self):
        super().compute()

        hub_in_r = self.kp.inlet_tip_r * (1 - self.blade_height_ratio)
        hub_out_r = self.kp.exit_tip_r * (1 - self.blade_height_ratio)

        self.area_in = np.pi * (self.kp.inlet_tip_r**2 - hub_in_r**2)

        self.mean_radius = (self.kp.inlet_tip_r + hub_in_r + self.kp.exit_tip_r + hub_out_r) / 4.0

        self.fp_exit_hub_kp = self.kp.exit_tip * np.r_[self.exit_hubqtip, 1.0]

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        external_edge = CreateBezier.g1_relative_tension(
            rz_to_3d(self.kp.inlet_tip),
            rz_to_3d(self.kp.exit_tip),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            0.2,
            1.5,
        )
        other_edges = CreateWire.from_points(
            (
                rz_to_3d(self.kp.inlet_tip),
                rz_to_3d(self.kp.inlet_hub),
                rz_to_3d(self.kp.exit_hub),
                rz_to_3d(self.kp.exit_tip),
            )
        )

        w = CreateWire.from_elements(
            (external_edge, other_edges),
        )

        shell = CreateRevolution.surface_from_curve(w, CreateAxis.oz())
        return dict(geom=CreateTopology.make_compound(shell))
