# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.channel import ChannelAero, ChannelGeom


class Channel(System):
    """Channel vane with aero.

    Sub-systems
    -----------
    geom: GenericSimpleGeom
        channel envelop
    aero: ChannelAero
        compute aerodyanmic characteristics

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
        self.add_child(ChannelGeom("geom"), pulling="kp")
        self.add_child(ChannelAero("aero"), pulling=["fl_in", "fl_out"])

        self.connect(self.geom.outwards, self.aero.inwards, ["area_in", "area_exit"])
