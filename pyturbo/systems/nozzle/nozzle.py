from typing import Dict

from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape

from pyturbo.systems.nozzle.nozzle_aero import NozzleAero
from pyturbo.systems.nozzle.nozzle_geom import NozzleGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Nozzle(System, JupyterViewable):
    """
    Nozzle simple assembly model with geom and aero.

    Sub-systems
    -----------
    geom: NozzleGeom
        compute geometrical data
    aero: NozzleAero
        compute aero performances

    Inputs
    ------
    kp : KeypointPort
        nozzle geometrical envelop
    fl_in: FluidPort
        inlet gas 

    pamb[Pa]: float
        ambiant static pressure

    Outputs
    -------
    fl_out: FluidPort
        exit gas

    thrust[N]: float
        thrust in N computed at throat. If drag < 0, aspiration contribute to thrust

    """

    def setup(self):
        # children
        self.add_child(NozzleGeom("geom"), pulling="kp")
        self.add_child(NozzleAero("aero"), pulling=["fl_in", "pamb", "thrust"])

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, "area")

    def _to_occt(self) -> Dict[str, TopoDS_Shape]:
        return self.geom._to_occt()
