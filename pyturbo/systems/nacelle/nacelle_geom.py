# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System
from OCC.Core.Geom import Geom_RectangularTrimmedSurface
from pyoccad.create import CreateAxis, CreateBezier, CreateRevolution, CreateWire
from pyoccad.transform import Scale

from pyturbo.utils import JupyterViewable, rz_to_3d


class NacelleGeom(System, JupyterViewable):
    """A nacelle simple geometrical model.

    It is a Short Duct Separated Flow (SDSF) configuration.
    All the cowl are represented from the inlet to the nozzle, using
    very simplistic Bezier curves between turbomachinery keypoints.

    Inputs
    ------
    kp: KeypointsPort
        nacelle geometrical envelop

    hilite_kp[m]: np.array(2), default=np.ones(2)
        inlet hilite keypoint
    ogv_exit_tip_kp[m]: np.array(2), default=np.ones(2)
        OGV exit tip keypoint
    sec_nozzle_exit_kp[m]: np.array(2), default=np.ones(2)
        Secondary nozzle exit keypoint

    fan_diameter[m]: float, default=1.0
        fan diameter
    dmax_over_dfan[-]: float, default=1.2
        max nacelle diameter over fan diameter

    Outputs
    -------
    external_max_diameter[m]: np.array, default=np.ones(2)
    """

    def setup(self):

        # inwards
        self.add_inward("hilite_kp", np.r_[0.0, 0.0], unit="m", desc="inlet hilite keypoint")
        self.add_inward("ogv_exit_tip_kp", np.r_[0.0, 0.0], unit="m", desc="OGV exit tip keypoint")
        self.add_inward(
            "sec_nozzle_exit_kp", np.r_[0.0, 0.0], unit="m", desc="Secondary nozzle exit keypoint"
        )

        self.add_inward("fan_diameter", 1.0, unit="m", desc="fan diameter")
        self.add_inward(
            "dmax_over_dfan", 1.2, unit="", desc="max nacelle diameter over fan diameter"
        )

        # outwards
        self.add_outward("external_max_diameter", np.r_[0.0, 0.0], unit="m")

    def compute(self):
        self.external_max_diameter = np.r_[
            self.fan_diameter / 2.0 * self.dmax_over_dfan,
            self.ogv_exit_tip_kp[0],
        ]

    def _to_occt(self):

        external_upstream = CreateBezier.g1_relative_tension(
            rz_to_3d(self.hilite_kp),
            rz_to_3d(self.external_max_diameter),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
            0.3,
            1.0,
        )
        external_downstream = CreateBezier.g1_relative_tension(
            rz_to_3d(self.external_max_diameter),
            rz_to_3d(self.sec_nozzle_exit_kp),
            (0.0, 0.0, 1.0),
            (-0.3, 0.0, 1.0),
            1.0,
            1.0,
        )

        w = CreateWire.from_elements(
            (
                external_upstream,
                external_downstream,
            )
        )
        r = CreateRevolution.surface_from_curve(w, CreateAxis.oz())

        brand = Geom_RectangularTrimmedSurface(
            CreateRevolution.surface_from_curve(external_upstream, CreateAxis.oz()),
            np.pi - 0.5,
            np.pi - 0.5 + 0.6 / self.fan_diameter,
            0.1,
            0.8,
        )
        Scale.from_factor(brand, 1.005, inplace=True)

        return r

    def _brand_shape(self):

        external_upstream = CreateBezier.g1_relative_tension(
            rz_to_3d(self.hilite_kp),
            rz_to_3d(self.external_max_diameter),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
            0.3,
            1.0,
        )

        brand = Geom_RectangularTrimmedSurface(
            CreateRevolution.surface_from_curve(external_upstream, CreateAxis.oz()),
            np.pi - 0.4,
            np.pi - 0.4 + 1.0 / self.fan_diameter,
            0.5,
            0.8,
        )
        Scale.from_factor(brand, 1.005, inplace=True)

        return brand
