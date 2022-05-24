import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class TurbineSimpleGeom(GenericSimpleGeom):
    """Turbine geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    The geometry exposed to aero module is made of:
      - inlet area
      - inlet and exit tip radius
    """

    def setup(self, stage_count: int = 1):
        super().setup()

        self.add_inward("stage_count", 1)
        self.add_inward("h_over_cx", 1.0, unit="", desc="height over axial chord ratio of a row")

        # aero outputs
        self.add_outward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("mean_radius", 1.0, unit="m", desc="mean radius")

        # design method
        self.add_design_method("axial_length").add_equation(
            "axial_form_factor == h_over_cx / (2. * stage_count)"
        )

    def compute(self):
        super().compute()

        self.area_in = np.pi * (self.kp.inlet_tip_r**2 - self.kp.inlet_hub_r**2)
        self.mean_radius = self.kp.mean_radius
