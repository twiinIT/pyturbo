from cosapp.systems import System

from pyturbo.systems.combustor import CombustorAero
from pyturbo.systems.generic import GenericSimpleGeom


class Combustor(System):
    """Combustor assembly model.

    Components
    ----------

    Physics
    -------
    geom : GenericSimpleGeom
        geometry is generated from the keypoints
    aero : CombustorAero
        combustion is performed from fluid flow and fuel flow

    Parameters
    ----------

    Inputs
    ------
    fl_in : FluidPort
    kp : KeyPointPort

    Outputs
    -------
    fl_out : FluidPort

    Inwards
    -------
    fuel_W : float
        fuel consumption in kg/s

    Outwards
    --------
    Tcomb : float
        combustion temperature

    Off design methods
    ------------------

    Good practice
    -------------

    """

    def setup(self):
        # children
        self.add_child(GenericSimpleGeom("geom"), pulling="kp")
        self.add_child(CombustorAero("aero"), pulling=["fl_in", "fl_out", "fuel_W", "Tcomb"])
