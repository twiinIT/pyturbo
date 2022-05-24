from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class CombustorSimpleGeom(GenericSimpleGeom):
    """Combustor geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.
    """

    def setup(self):
        super().setup()

        # design method
        self.add_design_method("axial_length").add_equation("axial_form_factor == 0.25")
