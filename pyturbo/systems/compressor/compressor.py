# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.systems.compressor.compressor_aero import CompressorAero
from pyturbo.systems.compressor.compressor_geom import CompressorGeom
from pyturbo.utils.jupyter_view import JupyterViewable


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

    def setup(self):
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

    def compute(self):
        self.N = self.sh_in.N

    def _to_occt(self):
        return dict(geom=self.geom._to_occt())


class Fan(Compressor):
    """Instantiate a fan module."""

    def setup(self):
        super().setup()

        # init param
        self.stage_count = 1

        # init inputs
        self.fl_in.W = 350
        self.fl_in.Tt = 288.15
        self.fl_in.Pt = 101325.0

        self.sh_in.power = 18e6
        self.sh_in.N = 5500

        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.85, 0.0]
        self.kp.exit_hub = np.r_[0.2, 0.5]
        self.kp.exit_tip = np.r_[0.85, 0.5]

        # init geom
        self.geom.blade_hub_to_tip_ratio = 0.3

        # init aero
        self.aero.eff_poly = 0.92
        self.aero.phiP = 0.9


class HPC(Compressor):
    """Instantiate a high pressure compressor."""

    def setup(self):
        super().setup()

        # init param
        self.stage_count = 9

        # init inputs
        self.fl_in.W = 60
        self.fl_in.Tt = 330.0
        self.fl_in.Pt = 1.7e5

        self.sh_in.power = 20e6
        self.sh_in.N = 15000

        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.25, 0.0]
        self.kp.exit_hub = np.r_[0.0, 0.5]
        self.kp.exit_tip = np.r_[0.20, 0.5]

        # init geom
        self.geom.blade_hub_to_tip_ratio = 0.8

        # init aero
        self.aero.eff_poly = 0.9
        self.aero.phiP = 0.9


class Booster(Compressor):
    """Instantiate a booster module."""

    def setup(self):
        super().setup()

        # init param
        self.stage_count = 3

        # init inputs
        self.fl_in.W = 60
        self.fl_in.Tt = 310.0
        self.fl_in.Pt = 1.7e5

        self.sh_in.power = 2e6
        self.sh_in.N = 5000

        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.6, 0.0]
        self.kp.exit_hub = np.r_[0.0, 0.4]
        self.kp.exit_tip = np.r_[0.4, 0.4]

        # init geom
        self.geom.blade_hub_to_tip_ratio = 0.6

        # init aero
        self.aero.eff_poly = 0.9
        self.aero.phiP = 0.7
