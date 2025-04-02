# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

from cosapp.systems import System

from pyturbo.systems.compressor.compressor_aero import CompressorAero
from pyturbo.systems.compressor.compressor_geom import CompressorGeom
from pyturbo.utils import JupyterViewable, load_from_json


class Compressor(System, JupyterViewable):
    """Compressor assembly model.

    Sub-systems
    -----------
    geom: CompressorGeom
        geometry value from envelop
    aero: CompressorAero
        performance characteristics

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

        # connections
        self.connect(
            self.geom.outwards,
            self.aero.inwards,
            ["tip_in_r", "tip_out_r", "inlet_area"],
        )

        # outwards
        # TODO check how to avoid this standard copy
        self.add_outward("N", 1.0, unit="rpm", desc="shaft speed rotation")

        if init_file:
            load_from_json(self, init_file)

    def compute(self):
        self.N = self.sh_in.N

    def _to_occt(self):
        return dict(geom=self.geom._to_occt())
