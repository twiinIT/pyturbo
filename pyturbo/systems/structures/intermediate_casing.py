# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.generic import GenericSimpleView
from pyturbo.systems.structures import ChannelAero


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
    view: GenericSimpleView
        compute visualisation

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
        # aero
        self.add_child(
            ChannelAero("primary_aero"), pulling={"fl_in": "fl_booster", "fl_out": "fl_core"}
        )
        self.add_child(
            ChannelAero("secondary_aero"), pulling={"fl_in": "fl_ogv", "fl_out": "fl_bypass"}
        )

        # view
        self.add_child(GenericSimpleView("view"), pulling=["kp", "occ_view"])
