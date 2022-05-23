# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.combustor import Combustor
from pyturbo.systems.compressor import HPC
from pyturbo.systems.gas_generator import GasGeneratorGeom
from pyturbo.systems.turbine import HPT
from pyturbo.utils.jupyter_view import JupyterViewable


class GasGenerator(System, JupyterViewable):
    """
    A simple gas generator model.

    This model includes a compressor, a combustor and a turbine. The power transmission
    between the turbine and the compressor is direct without and intermediate shaft model.

    --------------------------------------
    |   hpc   |   combustor   |   hpt    |
    --------------------------------------

    Components
    ----------
    hpc : HPC
    combustor : Combustor
    hpt : HPT

    Physics
    -------
    geom : GasGeneratorGeom
        component kp from gg kp

    Inputs
    ------
    kp : KeypointPort
    fl_in : FluidPort

    Outputs
    -------
    fl_out : FluidPort

    Inwards
    -------
    fuel_W : float
        fuel mass flow

    Outwards:
    ---------
    opr : float
        compressor pressure ration
    N : float
        shaft speed rotation in rpm

    Good practice
    -------------
    1 - init compressor.aero.sh_in.power to the good order of magnitude
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
