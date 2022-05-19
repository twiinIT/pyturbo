from numpy import pi
from pyturbo.systems.generic_simple_geom import GenericSimpleGeom


class CompressorSimpleGeom(GenericSimpleGeom):
    """Compressor geometry.

    - The geometrical envelop is a cylinder with inlet and outlet assumed fully radial
    - The geometry exposed to aero module is made of:
            inlet section
            inlet and outlet tip radius
    """

    def setup(self, stage_count: int = 1):
        super().setup()

        self.add_inward("stage_count", 1)
        # aero outputs
        self.add_outward("inlet_section", 1.0, unit="m**2", desc="inlet section")

        # design method
        self.add_design_method("sizing").add_unknown("scale")

    def compute(self):
        super().compute()

        self.inlet_section = pi * (self.exit_tip_radius**2 - self.exit_hub_radius**2)
