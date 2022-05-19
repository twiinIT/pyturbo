from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateRevolution, CreateWire
from pyoccad.transform import Scale, Translate
import numpy as np


class GenericSimpleGeom(System):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):
        # inwards
        self.add_inward("hub_in_r_ref", 0.5, unit="m", desc="reference inlet hub radius")
        self.add_inward("tip_in_r_ref", 1.0, unit="m", desc="reference inlet tip radius")
        self.add_inward("hub_out_r_ref", 0.5, unit="m", desc="reference exit hub radius")
        self.add_inward("tip_out_r_ref", 1.0, unit="m", desc="reference exit tip radius")
        self.add_inward("axial_form_factor", 1.0, unit="", desc="length-over-radius form factor")

        self.add_inward("scale", 1.0, unit="", desc="scale factor")
        self.add_inward("translation", np.zeros(3), unit="m", desc="translation vector")

        self.add_outward("hub_in_r", 0.5, unit="m", desc="inlet hub radius")
        self.add_outward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_outward("hub_out_r", 0.5, unit="m", desc="exit hub radius")
        self.add_outward("tip_out_r", 1.0, unit="m", desc="exit tip radius")
        self.add_outward("shape", None, unit="", desc="view")

    def compute_generic_geom(self):
        axial_length = (
            np.mean(
                (
                    self.tip_in_r_ref - self.hub_in_r_ref,
                    self.tip_out_r_ref - self.hub_out_r_ref,
                )
            )
            * self.axial_form_factor
        )

        w = CreateWire.from_points(
            (
                (0.0, self.hub_in_r_ref, 0.0),
                (0.0, self.tip_in_r_ref, 0.0),
                (axial_length, self.tip_out_r_ref, 0.0),
                (axial_length, self.hub_out_r_ref, 0.0),
            ),
            auto_close=True,
        )

        self.hub_in_r = self.hub_in_r_ref * self.scale
        self.tip_in_r = self.tip_in_r_ref * self.scale
        self.hub_out_r = self.hub_out_r_ref * self.scale
        self.tip_out_r = self.tip_out_r_ref * self.scale

        revol = CreateRevolution.solid_from_curve(w, CreateAxis.ox())
        Scale.from_factor(revol, self.scale)
        Translate.from_vector(revol, self.translation)
        self.shape = revol
