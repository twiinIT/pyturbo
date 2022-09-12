from cosapp.systems import System

from pyturbo.systems.generic import GenericSimpleGeom
from pyturbo.systems.structures.channel_aero import ChannelAero


class Channel(System):
    """
    Channel vane with aero

    Sub-systems
    -----------
    geom: GenericSimpleGeom
        channel envelop
    aero: ChannelAero
        compute aerodyanmic characteristics

    Inputs
    ------
    kp: KeypointPort
        geometrical envelop
    fl_in: FluidPort
        inlet fluid

    Outputs
    -------
    fl_out: FluidPort
        exit fluid

    """

    def setup(self, geom_class=GenericSimpleGeom, aero_class=ChannelAero):
        if geom_class is not None:
            geom = geom_class("geom")
        if aero_class is not None:
            aero = aero_class("aero")

        self.add_child(geom, pulling="kp")
        self.add_child(aero, pulling=["fl_in", "fl_out"])
