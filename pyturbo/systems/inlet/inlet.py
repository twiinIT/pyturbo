# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.generic import GenericSimpleView
from pyturbo.systems.inlet import InletAero, InletGeom


class Inlet(System):
    """Inlet simple assembly model.

    Sub-systems
    -----------
    geom: InletGeom
        compute the geometrical data
    aero: InletAero
        compute aerodynamics performances
    view: GenericSimpleView
        compute visualisation

    Inputs
    ------
    kp: KeypointsPort
        inlet geometrical envelop
    fl_in: FluidPort
        inlet gas

    pamb[Pa]: float
        ambiant static pressure

    Outputs
    -------
    fl_out: FluidPort
        exit gas

    drag[N]: float
        drag computed at throat. If drag < 0, aspiration contribute to thrust
    """

    def setup(self):
        # children
        self.add_child(InletGeom("geom"), pulling=["kp"])
        self.add_child(InletAero("aero"), pulling=["fl_in", "pamb", "fl_out", "drag"])
        self.add_child(GenericSimpleView("view"), pulling=["kp", "occ_view"])

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, "area")
