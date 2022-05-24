from cosapp.systems import System

from pyturbo.systems.turbine import TurbineSimpleAero, TurbineSimpleGeom


class TurbineSimple(System):
    """Turbine simple assembly model.

    It may contain aero and/or geometry sub-models.
    """

    def setup(self, stage_count: int = 1, geom: bool = True, aero: bool = True):
        # childrens
        if geom:
            self.add_child(
                TurbineSimpleGeom("geom", stage_count=stage_count),
                pulling=[
                    "stage_count",
                    "kp",
                ],
            )
        if aero:
            self.add_child(TurbineSimpleAero("aero"), pulling=["fl_in", "fl_out", "shaft_out"])

        # connections
        if geom and aero:
            self.connect(
                self.geom.outwards,
                self.aero.inwards,
                ["area_in", "mean_radius"],
            )
            self.connect(self.geom.inwards, self.aero.inwards, ["stage_count"])

        # design method
        temp_des = self.aero.design_methods["temperature"]
        speed_des = self.aero.design_methods["speed"]
        axial_length_des = self.geom.design_methods["axial_length"]
        self.add_design_method("sizing").extend(temp_des).extend(speed_des).extend(axial_length_des)
