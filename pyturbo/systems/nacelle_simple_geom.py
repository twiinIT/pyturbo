import numpy as np
from cosapp.systems import System
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GCE2d import GCE2d_MakeEllipse
from OCC.Core.Geom import Geom_Circle, Geom_Ellipse, Geom_RectangularTrimmedSurface
from OCC.Core.gp import gp_Ax2d, gp_Dir2d, gp_GTrsf2d, gp_Pnt, gp_Pnt2d
from OCC.Core.ShapeFix import ShapeFix_Shape
from pyoccad.create import (
    CreateArray1,
    CreateAxis,
    CreateBezier,
    CreateCircle,
    CreateDirection,
    CreateEllipse,
    CreateFace,
    CreatePoint,
    CreateRevolution,
    CreateTopology,
    CreateWire,
)
from pyoccad.transform import Scale


class NacelleSimpleGeom(System):
    """A nacelle simple geometrical model.

    It is a Short Duct Separated Flow (SDSF) configuration.
    All the cowl are represented from the inlet to the nozzle, using
    very simplistic Bezier curves between turbomachinery keypoints.
    """

    def setup(self):

        self.add_inward("fan_diameter", 1.0, unit="m", desc="fan diameter")
        self.add_inward(
            "fan_duct_length_over_radius",
            2.5,
            unit="",
            desc="fan duct length over fan diameter ratio",
        )
        self.add_inward(
            "inlet_length_over_diameter", 0.3, unit="", desc="inlet length over fan diameter ratio"
        )
        self.add_inward(
            "dmax_over_dfan", 1.3, unit="", desc="max nacelle diameter over fan diameter ratio"
        )
        self.add_inward(
            "inlet_throat_ratio", 0.97, unit="", desc="inlet throat over fan diameter ratio"
        )

        self.add_inward(
            "fan_inlet_tip",
            gp_Pnt(self.fan_diameter / 2.0, 0.0, 0.0),
            desc="fan inlet tip keypoint",
        )
        self.add_inward(
            "ogv_exit_tip", gp_Pnt(self.fan_diameter / 2.0, 0.0, 0.4), desc="OGV exit tip keypoint"
        )
        self.add_inward(
            "ogv_exit_hub",
            gp_Pnt(0.3 * self.fan_diameter / 2.0, 0.0, 0.4),
            desc="OGV exit hub keypoint",
        )
        self.add_inward(
            "turbine_exit_tip",
            gp_Pnt(0.3, 0.0, self.fan_diameter / 2.0 * self.fan_duct_length_over_radius),
            desc="LPT exit tip keypoint",
        )
        self.add_inward(
            "turbine_exit_hub",
            gp_Pnt(0.25, 0.0, self.fan_diameter / 2.0 * self.fan_duct_length_over_radius),
            desc="LPT exit hub keypoint",
        )

        self.add_outward("shape", None)

    def compute(self):
        fan_r = self.fan_diameter / 2.0

        self.fan_inlet_tip.SetX(fan_r)
        self.ogv_exit_tip.SetX(fan_r)
        self.ogv_exit_hub.SetX(fan_r)
        self.turbine_exit_tip.SetZ(fan_r * self.fan_duct_length_over_radius)
        self.turbine_exit_hub.SetZ(fan_r * self.fan_duct_length_over_radius)

        inlet_length = self.inlet_length_over_diameter * 2 / self.fan_diameter
        throat = (
            self.fan_inlet_tip.Coord()
            - np.r_[fan_r * (1.0 - self.inlet_throat_ratio), 0.0, 0.5 * inlet_length]
        )
        hilite = self.fan_inlet_tip.Coord() - np.r_[0.0, 0.0, inlet_length]
        max_radius = np.r_[self.ogv_exit_tip.X() * self.dmax_over_dfan, 0.0, self.fan_inlet_tip.Z()]
        sec_nozzle_exit = np.r_[
            self.ogv_exit_tip.X() * 1.0,
            0.0,
            self.ogv_exit_tip.Z() + 0.8 * (self.turbine_exit_tip.Z() - self.ogv_exit_tip.Z()),
        ]

        diffuser = CreateBezier.g1_relative_tension(
            self.fan_inlet_tip.Coord(), throat, (0.0, 0.0, -1), (0.0, 0.0, -1.0), 1.0, 1.0
        )
        inlet = CreateBezier.g1_relative_tension(
            throat, hilite, (0.0, 0.0, -1), (1.0, 0.0, 0.0), 1.0, 1.0
        )
        external = CreateBezier.g1_relative_tension(
            hilite, max_radius, (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), 0.3, 1.0
        )
        external_sec_duct = CreateBezier.g1_relative_tension(
            max_radius, sec_nozzle_exit, (0.0, 0.0, 1.0), (-0.3, 0.0, 1.0), 1.0, 1.0
        )
        internal_sec_duct = CreateBezier.g1_relative_tension(
            sec_nozzle_exit, self.ogv_exit_tip.Coord(), (0.3, 0.0, -1.0), (0.0, 0.0, -1.0), 1.0, 1.0
        )

        w = CreateWire.from_elements(
            (
                diffuser,
                inlet,
                external,
                external_sec_duct,
                internal_sec_duct,
            )
        )
        nacelle = CreateRevolution.solid_from_curve(w, CreateAxis.oz())
        self.shape = nacelle
