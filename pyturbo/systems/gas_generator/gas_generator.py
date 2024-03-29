# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.combustor import Combustor
from pyturbo.systems.compressor import HPC
from pyturbo.systems.gas_generator.gas_generator_geom import GasGeneratorGeom
from pyturbo.systems.turbine import HPT
from pyturbo.utils.jupyter_view import JupyterViewable


class GasGenerator(System, JupyterViewable):
    """A simple gas generator model.

    This model includes a compressor, a combustor and a turbine. The power transmission
    between the turbine and the compressor is direct without an intermediate shaft model.

    Sub-systems
    -----------
    hpc: HPC
        high pressure compressor
    combustor: Combustor
        combustor
    hpt: HPT
        high pressure turbine

    geom: GasGeneratorGeom
        provide the sub-elemnts geometrical envelops

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

    opr[-]: float
        compressor pressure ration
    N[rpm]: float
        shaft speed rotation

    Good practice
    -------------
    1:
        init compressor.aero.sh_in.power to the good order of magnitude
    """

    def setup(self):
        # children
        geom = self.add_child(GasGeneratorGeom("geom"), pulling=["kp"])

        cmp = self.add_child(HPC("compressor"), pulling={"fl_in": "fl_in", "pr": "opr", "N": "N"})
        cmb = self.add_child(Combustor("combustor"), pulling=["fuel_W"])
        trb = self.add_child(HPT("turbine"), pulling=["fl_out"])

        # connection geom
        self.connect(geom.compressor_kp, cmp.kp)
        self.connect(geom.combustor_kp, cmb.kp)
        self.connect(geom.turbine_kp, trb.kp)

        # connection shaft
        self.connect(self.turbine.sh_out, self.compressor.sh_in)

        # connection fluid
        self.connect(self.compressor.fl_out, self.combustor.fl_in)
        self.connect(self.combustor.fl_out, self.turbine.fl_in)

    def _to_occt(self):
        return dict(
            compressor=self.compressor.geom._to_occt(),
            combustor=self.combustor.geom._to_occt(),
            turbine=self.turbine.geom._to_occt(),
        )
