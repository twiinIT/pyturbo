from math import pi

import numpy as np
from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateRevolution, CreateWire
from pyoccad.transform import Scale, Translate


class GenericSimpleGeom(System):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):
        # inputs/outputs
        self.add_inward("inlet_mean_radius", 1.0, unit="m", desc="inlet arithmetic mean radius")
        self.add_inward("exit_mean_radius", 1.0, unit="m", desc="exit arithmetic mean radius")

        self.add_inward("inlet_area", 1.0, unit="m**2", desc="inlet area")
        self.add_inward("exit_area", 1.0, unit="m**2", desc="inlet area")

        self.add_inward("form_factor", 1.0, unit="", desc="length over mean height ratio")

        self.add_inward("scaling", 1.0, unit="", desc="homothetic scaling factor")
        self.add_inward("translation", [0.0, 0.0, 0.0], unit="", desc="3D translation")

        # outwards
        self.add_outward("shape", None, unit="", desc="geometry")

    def compute(self):
        def f(mean_r, area):
            c = area / (2 * pi)
            r_hub = mean_r - c / (2 * mean_r)
            r_tip = 1.0
            return r_hub, r_tip

        inlet_hub_r, inlet_tip_r = f(self.inlet_mean_radius, self.inlet_area)
        exit_hub_r, exit_tip_r = f(self.exit_mean_radius, self.exit_area)
        length = (
            np.mean((inlet_tip_r, exit_tip_r)) - np.mean((inlet_hub_r, exit_hub_r))
        ) * self.form_factor

        w = CreateWire.from_points(
            (
                (0.0, inlet_hub_r, 0.0),
                (0.0, inlet_tip_r, 0.0),
                (length, exit_tip_r, 0.0),
                (length, exit_hub_r, 0.0),
            ),
            auto_close=True,
        )
        revol = CreateRevolution.solid_from_curve(w, CreateAxis.ox())
        Scale.from_factor(revol, self.scaling)
        Translate.from_vector(revol, self.translation)

        self.shape = revol
