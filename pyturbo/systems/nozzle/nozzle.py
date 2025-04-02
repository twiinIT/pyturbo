# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.generic import GenericSimpleView
from pyturbo.systems.nozzle.nozzle_aero import NozzleAero
from pyturbo.systems.nozzle.nozzle_geom import NozzleGeom


class Nozzle(System):
    """Nozzle simple assembly model with geom and aero.

    Sub-systems
    -----------
    geom: NozzleGeom
        compute geometrical data
    aero: NozzleAero
        compute aero performances
    view: GenericSimpleView
        compute visualisation

    Inputs
    ------
    kp : KeypointsPort
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
        self.add_child(NozzleGeom("geom"), pulling=["kp"])
        self.add_child(NozzleAero("aero"), pulling=["fl_in", "pamb", "thrust"])
        self.add_child(
            GenericSimpleView("view"),
            pulling=["kp", "occ_view"],
        )

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, ["area", "area_in", "area_exit"])
