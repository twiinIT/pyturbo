# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

from cosapp.systems import System

from pyturbo.systems.turbine.turbine_aero import TurbineAero
from pyturbo.systems.turbine.turbine_geom import TurbineGeom
from pyturbo.utils import JupyterViewable, load_from_json


class Turbine(System, JupyterViewable):
    """Turbine simple assembly model.

    Sub-systems
    -----------
    geom: TurbineGeom
        geometry value from envelop
    aero: TurbineAero
        performance characteristics

    Inputs
    ------
    stage_count: integer
        number of stages

    kp: KeypointsPort
        geometrical envelop
    fl_in: FluidPort
        inlet gas

    Outputs
    -------
    fl_out: FluidPort
        exit gas
    sh_out: ShaftPort
        exit shaft
    fp_exit_hub_kp[m]: np.array(2), default=np.ones(2)
        exit hub flow position

    pr[-]: float
        total to total pressure ratio
    N[rpm]: float
        shaft speed rotation
    """

    def setup(self, init_file: Path = None):
        # children
        self.add_child(
            TurbineGeom("geom"),
            pulling=["stage_count", "kp", "fp_exit_hub_kp"],
        )
        self.add_child(TurbineAero("aero"), pulling=["fl_in", "fl_out", "sh_out", "stage_count"])

        # connections
        self.connect(
            self.geom.outwards,
            self.aero.inwards,
            ["area_in", "mean_radius"],
        )

        if init_file:
            load_from_json(self, init_file)

    def _to_occt(self):
        return dict(geom=self.geom._to_occt())
