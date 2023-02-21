# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.nacelle.plug_geom import PlugGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Plug(System, JupyterViewable):
    """Plug assembly model.

    Sub-systems
    -----------
    geom: PlugGeom
        geometrical data

    Inputs
    ------
    trf_exit_hub_kp: KeypointsPort
        position of the plug
    """

    def setup(self):
        # children
        self.add_child(
            PlugGeom("geom"),
            pulling=["trf_exit_hub_kp"],
        )

    def _to_occt(self):
        return self.geom._to_occt()
