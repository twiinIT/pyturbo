# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.combustor import Combustor
from pyturbo.systems.compressor import Compressor
from pyturbo.systems.gas_generator import GasGeneratorGeom
from pyturbo.systems.generic import GenericSystemView
from pyturbo.systems.turbine import Turbine


class GasGenerator(System):
    """A simple gas generator model.

    This model includes a compressor, a combustor and a turbine. The power transmission
    between the turbine and the compressor is direct without an intermediate shaft model.

    Sub-systems
    -----------
    hpc: Compressor(HPC)
        high pressure compressor
    combustor: Combustor
        combustor
    hpt: Turbine(HPT)
        high pressure turbine

    geom: GasGeneratorGeom
        sub systems key points generated from the core envelop
    view: GenericSystemView
        compute visualisation

    Inputs
    ------
    kp: KeypointsPort
        gas generator geometrical envelop
    fl_in: FluidPort
        fluid going into the gas generator

    fuel_W[kg/s]: float
        fuel mass flow

    Outputs
    -------
    fl_out: FluidPort
        gas leaving the gas generator

    pr[-]: float
        compressor pressure ration
    N[rpm]: float
        shaft speed rotation

    Good practice
    -------------
    1:
        init compressor.aero.sh_in.power to the good order of magnitude
    """

    def setup(self):
        # properties
        children_name = ["compressor", "combustor", "turbine"]

        # children
        self.add_child(GasGeneratorGeom("geom"), pulling=["kp"])

        self.add_child(Compressor("compressor", config="hpc"), pulling=["fl_in", "pr", "N"])
        self.add_child(Combustor("combustor"), pulling=["fuel_W"])
        self.add_child(Turbine("turbine", config="hpt"), pulling=["fl_out"])

        self.add_child(GenericSystemView("view", children_name=children_name), pulling=["occ_view"])

        # connection geom
        for name in children_name:
            self.connect(self.geom[f"{name}_kp"], self[name].kp)
            self.connect(self[name], self.view, {"occ_view": f"{name}_view"})

        # connection shaft
        self.connect(self.turbine.sh_out, self.compressor.sh_in)

        # connection fluid
        self.connect(self.compressor.fl_out, self.combustor.fl_in)
        self.connect(self.combustor.fl_out, self.turbine.fl_in)

        # design methods
        scaling = self.add_design_method("scaling")

        scaling.extend(self.compressor.design_methods["scaling"])
        scaling.extend(self.combustor.design_methods["scaling"])
        scaling.extend(self.turbine.design_methods["scaling"])
