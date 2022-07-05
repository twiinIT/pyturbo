from typing import Dict

from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape

from pyturbo.systems.nozzle import NozzleAero, NozzleGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Nozzle(System, JupyterViewable):
    """
    Nozzle simple assembly model with geom and aero.

    """

    def setup(self):
        # children
        self.add_child(NozzleGeom("geom"), pulling="kp")
        self.add_child(NozzleAero("aero"), pulling=["fl_in", "pamb", "thrust"])

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, "area")

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        return self.geom._to_occt()
