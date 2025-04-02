# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System
from OCC.Core.Geom import Geom_RectangularTrimmedSurface
from pyoccad.create import CreateAxis, CreateBezier, CreateRevolution, CreateWire
from pyoccad.transform import Scale

from pyturbo.ports import KeypointsPort
from pyturbo.ports.view_port import View, ViewPort


class NacelleView(System):
    """Class with visual representation of the Nacelle.

    Inputs
    ------
    kp : KeypointsPort
        The key points of the nacelle

    Outputs
    -------
    occ_view : ViewPort
        The visualisation.
    """

    def setup(self):
        # inputs/outputs
        self.add_input(KeypointsPort, "kp")
        self.add_output(ViewPort, "occ_view")

    def compute(self):
        r = self.kp.exit_tip[0] * 1.2
        z = 0.6 * self.kp.inlet_hub[1] + 0.4 * self.kp.exit_hub[1]

        outer_shell = {
            "shape": bezier(
                self.kp.inlet_tip,
                np.r_[r, z],
                self.kp.exit_tip,
                1.0,
                (0, 0, 1),
            ),
            "face_color": "black",
            "opacity": 0.2,
        }

        view = View({"outer_shell": outer_shell})

        self.occ_view.set_value(view)


def bezier(hilite_kp, external_max_diameter, secondary_nozzle_exit_tip, fan_diameter, vect):
    """Generate a Bezier surface for a nozzle using key points and specified axis direction.

    Parameters
    ----------
    hilite_kp : tuple
        Key point at the hilite (front) of the nozzle.
    external_max_diameter : tuple
        Key point at the external maximum diameter of the nozzle.
    secondary_nozzle_exit_tip : tuple
        Key point at the secondary nozzle exit.
    fan_diameter : float
        Diameter of the fan section, used to scale the surface.
    vect : tuple
        Axis direction vector for the revolution (must be (1,0,0), (0,1,0), or (0,0,1)).

    Returns
    -------
    r : pyoccad.Shape
        The pyoccad shape representing the Bezier surface of the nozzle after revolution.
    """

    axis = [rx_to_3d, ry_to_3d, rz_to_3d]
    for i, x in enumerate(vect):
        if x > 0:
            axis_index = i
            break

    external_upstream = CreateBezier.g1_relative_tension(
        axis[axis_index](hilite_kp),
        axis[axis_index](external_max_diameter),
        (0.0, 0.0, -1.0),
        (0.0, 0.0, 1.0),
        1.0,
        1.0,
    )
    external_downstream = CreateBezier.g1_relative_tension(
        axis[axis_index](external_max_diameter),
        axis[axis_index](secondary_nozzle_exit_tip),
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
    revolution_vector = [CreateAxis.ox(), CreateAxis.oy(), CreateAxis.oz()]
    r = CreateRevolution.surface_from_curve(w, revolution_vector[axis_index])

    brand = Geom_RectangularTrimmedSurface(
        CreateRevolution.surface_from_curve(external_upstream, revolution_vector[axis_index]),
        np.pi - 0.5,
        np.pi - 0.5 + 0.6 / fan_diameter,
        0.1,
        0.8,
    )
    Scale.from_factor(brand, 1.005, inplace=True)

    return r


def rz_to_3d(rz):
    """Compute the slope from ..."""
    return np.r_[rz[0], 0.0, rz[1]]


def rx_to_3d(rz):
    """Compute the slope from ..."""
    return np.r_[rz[1], rz[0], 0.0]


def ry_to_3d(rz):
    """Compute the slope from ..."""
    return np.r_[0.0, rz[1], rz[0]]
