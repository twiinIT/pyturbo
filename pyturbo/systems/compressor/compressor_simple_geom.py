from numpy import pi

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class CompressorSimpleGeom(GenericSimpleGeom):
    """Compressor geometry.

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
        self.add_outward("inlet_area", 1.0, unit="m**2", desc="inlet area")

        # design method
        self.add_design_method("sizing").add_unknown(("scale", "tip_in_r_ref"))

    def compute(self):
        # a stage is composed of 2 rows
        self.axial_form_factor = 2 * self.stage_count * self.h_over_cx

        self.compute_generic_geom()

        self.inlet_area = pi * (self.tip_in_r**2 - self.hub_in_r**2)
