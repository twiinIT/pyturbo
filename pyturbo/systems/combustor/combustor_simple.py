import numpy as np
from cosapp.systems import System

from pyturbo.systems.combustor import CombustorSimpleAero, CombustorSimpleGeom


class CombustorSimple(System):
    """Combustor simple assembly model.

    It may contain aero and/or geometry sub-models.
    """

    def setup(self, geom: bool = True, aero: bool = True):
        # childrens
        if geom:
            self.add_child(CombustorSimpleGeom("geom"), pulling="kp")
        if aero:
            self.add_child(CombustorSimpleAero("aero"), pulling=["fl_in", "fl_out", "fuel_in"])

        # design method
        sizing = self.add_design_method("sizing")
        if geom:
            axial_length_des = self.geom.design_methods["axial_length"]
            sizing.extend(axial_length_des)
