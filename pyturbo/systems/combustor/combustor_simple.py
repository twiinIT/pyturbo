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
            self.add_child(CombustorSimpleGeom("geom"))
        if aero:
            self.add_child(CombustorSimpleAero("aero"), pulling=["fl_in", "fl_out", "fuel_in"])

        # design method
        self.add_design_method("sizing").extend(self.geom.design_methods["sizing"])
