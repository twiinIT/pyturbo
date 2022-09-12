from cosapp.systems import System

from pyturbo.systems.combustor.combustor_aero import CombustorAero
from pyturbo.systems.generic import GenericSimpleGeom


class Combustor(System):
    """Combustor assembly model.

    Sub-systems
    -----------
    geom: GenericSimpleGeom
        geometry is generated from the keypoints
    aero: CombustorAero
        combustion is performed from fluid flow and fuel flow

    Inputs
    ------
    fl_in: FluidPort
        fluid going into the combustor
    kp: KeyPointPort
        the combustor geometrical envelop

    fuel_W: [kg/s]float
        fuel consumption

    Outputs
    -------
    fl_out: FluidPort
        fluid leaving the combustor

    Tcomb[K]: float
        combustion temperature
    """

    def setup(self):
        # children
        self.add_child(GenericSimpleGeom("geom"), pulling="kp")
        self.add_child(CombustorAero("aero"), pulling=["fl_in", "fl_out", "fuel_W", "Tcomb"])
