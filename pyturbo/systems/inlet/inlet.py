from cosapp.systems import System

from pyturbo.systems.inlet import InletAero, InletGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Inlet(System, JupyterViewable):
    """
    Inlet simple assembly model.

    Physics
    -------
    geom : InletGeom
    aero : InletAero

    Inputs
    ------
    kp : KeypointPort
    fl_in : FluidPort

    Outputs
    -------
    fl_out : FluidPort

    Inwards
    -------
    pamb : float
        ambiant static pressure in Pa

    Outwards
    --------
    drag : float
        drag in N computed at throat. If drag < 0, aspiration contribute to thrust

    Good practice
    -------------
    1 - initiate sh_in.power with the good order of magnitude of shaft power
    """

    def setup(self):
        # children
        self.add_child(InletGeom("geom"), pulling=["fan_inlet_tip_kp", "hilite_kp"])
        self.add_child(InletAero("aero"), pulling=["fl_in", "pamb", "fl_out", "drag"])

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, "area")

    def _to_occt(self):
        return self.geom._to_occt()
