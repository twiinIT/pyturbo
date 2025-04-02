# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.generic import GenericSimpleView
from pyturbo.systems.structures import ChannelAero, ChannelGeom


class Channel(System):
    """Channel vane with aero.

    Sub-systems
    -----------
    geom: GenericSimpleGeom
        channel envelop
    aero: ChannelAero
        compute aerodyanmic characteristics
    view: GenericSimpleView
        compute visualisation

    Inputs
    ------
    kp: KeypointsPort
        geometrical envelop
    fl_in: FluidPort
        inlet fluid

    Outputs
    -------
    fl_out: FluidPort
        exit fluid

    """

    def setup(self):
        self.add_child(ChannelGeom("geom"), pulling=["kp"])
        self.add_child(ChannelAero("aero"), pulling=["fl_in", "fl_out"])
        self.add_child(GenericSimpleView("view"), pulling=["kp", "occ_view"])

        self.connect(self.geom.outwards, self.aero.inwards, ["area_in", "area_exit"])
