# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

from cosapp.systems import System

from pyturbo.systems.compressor import CompressorAero, CompressorGeom
from pyturbo.systems.generic import GenericSimpleView
from pyturbo.utils import load_from_json


class Compressor(System):
    """Compressor assembly model.

    Sub-systems
    -----------
    geom: CompressorGeom
        geometry value from envelop
    aero: CompressorAero
        performance characteristics
    view: GenericSimpleView
        compute visualisation

    Inputs
    ------
    stage_count: integer
        number of stages

    kp: KeypointsPort
        compressor geometrical envelop
    fl_in: FluidPort
        fluid going into the compressor
    sh_in: ShaftPort
        shaft driving the compressor

    Outputs
    -------
    fl_out: FluidPort
        fluid leaving the compressor
    pr[-]: float
        total to total pressure ratio
    N[rpm]: float
        shaft speed rotation

    Design methods
    --------------
    off design:
        psi computed from enthalpy conservation equal psi computed from characteristics

    Good practice
    -------------
    1:
        initiate sh_in.power with the good order of magnitude of shaft power
    """

    def setup(self, init_file: Path = None):
        # children
        self.add_child(
            CompressorGeom("geom"),
            pulling=["stage_count", "kp"],
        )
        self.add_child(
            CompressorAero("aero"), pulling=["fl_in", "fl_out", "sh_in", "pr", "stage_count"]
        )
        self.add_child(
            GenericSimpleView("view"),
            pulling=["occ_view", "kp"],
        )

        # outwards
        # TODO check how to avoid this standard copy
        self.add_outward("N", 1.0, unit="rpm", desc="shaft speed rotation")

        # connections
        self.connect(
            self.geom.outwards,
            self.aero.inwards,
            ["tip_in_r", "tip_out_r", "inlet_area"],
        )
        self.connect(self.aero.inwards, self.view.inwards, {"stage_count": "n"})

        # design methods
        # scaling fan
        scaling = self.add_design_method("scaling_fan")
        scaling.extend(self.aero.design_methods["scaling"])

        # scaling booster
        scaling = self.add_design_method("scaling_booster")
        scaling.extend(self.aero.design_methods["scaling_booster"])

        scaling.add_unknown("geom.blade_hub_to_tip_ratio", lower_bound=1e-5, upper_bound=1.0)

        # scaling hpc
        scaling = self.add_design_method("scaling_hpc")
        scaling.extend(self.aero.design_methods["scaling_hpc"])

        # init
        if init_file:
            load_from_json(self, init_file)

    def compute(self):
        self.N = self.sh_in.N
