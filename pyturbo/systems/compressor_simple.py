import numpy as np

from cosapp.systems import System

from pyturbo.systems import CompressorSimpleAero, CompressorSimpleGeom


class CompressorSimple(System):
    """Compressor simple assembly model.

    It may contain aero and/or geometry sub-models.
    """

    def setup(self, stage_count: int = 1, geom: bool = True, aero: bool = True):
        # childrens
        if geom:
            self.add_child(
                CompressorSimpleGeom("geom", stage_count=stage_count),
                pulling=[
                    "stage_count",
                    "inlet_hub_radius",
                    "inlet_tip_radius",
                    "exit_hub_radius",
                    "exit_tip_radius",
                ],
            )
        if aero:
            self.add_child(CompressorSimpleAero("aero"), pulling=["fl_in", "fl_out", "shaft_in"])

        # connections
        if geom and aero:
            self.connect(
                self.geom.outwards,
                self.aero.inwards,
                ["inlet_tip_radius", "exit_tip_radius", "inlet_section"],
            )
            self.connect(self.geom.inwards, self.aero.inwards, ["stage_count"])

        # design methods
        self.add_design_method("sizing")
        if geom:
            self.design_methods["sizing"].extend(self.geom.design_methods["sizing"])
        if aero:
            self.design_methods["sizing"].extend(self.aero.design_methods["sizing"])

        # calib methods
        self.add_design_method("calib")
        if aero:
            self.design_methods["calib"].extend(self.aero.design_methods["calib"])
