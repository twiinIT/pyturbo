from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateRevolution, CreateWire
from pyoccad.transform import Scale, Translate
import numpy as np


class GenericSimpleGeom(System):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):
        # inwards
        self.add_inward("inlet_hub_radius_ref", 0.5, unit="m", desc="reference inlet hub radius")
        self.add_inward("inlet_tip_radius_ref", 1.0, unit="m", desc="reference inlet tip radius")
        self.add_inward("exit_hub_radius_ref", 0.5, unit="m", desc="reference exit hub radius")
        self.add_inward("exit_tip_radius_ref", 1.0, unit="m", desc="reference exit tip radius")
        self.add_inward("axial_form_factor", 1.0, unit="", desc="length-over-radius form factor")

        self.add_inward("scale", 1.0, unit="", desc="scale factor")
        self.add_inward("translation", np.zeros(3), unit="m", desc="translation vector")

        self.add_outward("inlet_hub_radius", 0.5, unit="m", desc="inlet hub radius")
        self.add_outward("inlet_tip_radius", 1.0, unit="m", desc="inlet tip radius")
        self.add_outward("exit_hub_radius", 0.5, unit="m", desc="exit hub radius")
        self.add_outward("exit_tip_radius", 1.0, unit="m", desc="exit tip radius")
        self.add_outward("shape", None, unit="", desc="view")

    def compute(self):
        axial_length = np.mean(
            (
                self.inlet_hub_radius_ref,
                self.inlet_tip_radius_ref,
                self.exit_hub_radius_ref,
                self.exit_tip_radius_ref,
            )
        )
        w = CreateWire.from_points(
            (
                (0.0, self.inlet_hub_radius_ref, 0.0),
                (0.0, self.inlet_tip_radius_ref, 0.0),
                (axial_length, self.exit_tip_radius_ref, 0.0),
                (axial_length, self.exit_hub_radius_ref, 0.0),
            ),
            auto_close=True,
        )

        self.inlet_hub_radius = self.inlet_hub_radius_ref * self.scale
        self.inlet_tip_radius = self.inlet_tip_radius_ref * self.scale
        self.exit_hub_radius = self.exit_hub_radius_ref * self.scale
        self.exit_tip_radius = self.exit_tip_radius_ref * self.scale

        revol = CreateRevolution.solid_from_curve(w, CreateAxis.ox())
        Scale.from_factor(revol, self.scale)
        Translate.from_vector(revol, self.translation)
        self.shape = revol
