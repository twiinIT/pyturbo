from numpy import pi

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class CombustorSimpleGeom(GenericSimpleGeom):
    """Combustor geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.
    """

    def setup(self, stage_count: int = 1):
        super().setup()

        # design method
        self.add_design_method("sizing").add_unknown("scale")

    def compute(self):
        self.axial_form_factor = 3.0
        self.compute_generic_geom()
