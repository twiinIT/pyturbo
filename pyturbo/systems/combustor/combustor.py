# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.combustor.combustor_aero import CombustorAero
from pyturbo.systems.generic import GenericSimpleView


class Combustor(System):
    """Combustor assembly model.

    Sub-systems
    -----------
    aero: CombustorAero
        combustion is performed from fluid flow and fuel flow
    view: GenericSimpleView
        compute visualisation

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
    occ_view: ViewPort
        occ view of the combustor

    Tcomb[K]: float
        combustion temperature
    """

    def setup(self):
        # children
        self.add_child(CombustorAero("aero"), pulling=["fl_in", "fl_out", "fuel_W", "Tcomb"])
        self.add_child(GenericSimpleView("view"), pulling=["kp", "occ_view"])

        # design methods
        scaling = self.add_design_method("scaling")
        scaling.extend(self.aero.design_methods["scaling"])
