from cosapp.systems import System

from pyturbo.systems.channel import ChannelAero
from pyturbo.systems.generic import GenericSimpleGeom


class IntermediateCasing(System):
    """Intermediate Casing with primary and secondary flow.

    Sub-systems
    -----------
    geom: GenericSimpleGeom
        compute geometrical data
    primary_aero: ChannelAero
        compute primary flow aero performances
    secondary_aero: ChannelAero
        compute secondary flow aero performances

    Inputs
    ------
    kp : KeypointsPort
        nozzle geometrical envelop
    fl_booster: FluidPort
        boosler outlet fluid
    fl_ogv: FluidPort
        ogv outlet fluid

    Outputs
    -------
    fl_core: FluidPort
        core fluid
    fl_bypass: FluidPort
        bypass fluid

    """

    def setup(self):
        # geom
        self.add_child(GenericSimpleGeom("geom"), pulling="kp")

        # aero
        self.add_child(
            ChannelAero("primary_aero"), pulling={"fl_in": "fl_booster", "fl_out": "fl_core"}
        )
        self.add_child(
            ChannelAero("secondary_aero"), pulling={"fl_in": "fl_ogv", "fl_out": "fl_bypass"}
        )
