# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.inlet.inlet_aero import InletAero
from pyturbo.systems.inlet.inlet_geom import InletGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Inlet(System, JupyterViewable):
    """Inlet simple assembly model.

    Sub-systems
    -----------
    geom: InletGeom
        compute the geometrical data
    aero: InletAero
        compute aerodynamics performances

    Inputs
    ------
    kp: KeypointsPort
        inlet geometrical envelop
    fl_in: FluidPort
        inlet gas

    pamb[Pa]: float
        ambiant static pressure

    Outputs
    -------
    fl_out: FluidPort
        exit gas

    drag[N]: float
        drag computed at throat. If drag < 0, aspiration contribute to thrust

    Good practice
    -------------
    1:
        initiate sh_in.power with the good order of magnitude of shaft power
    """

    def setup(self):
        # children
        self.add_child(InletGeom("geom"), pulling=["fan_inlet_tip_kp", "hilite_kp"])
        self.add_child(InletAero("aero"), pulling=["fl_in", "pamb", "fl_out", "drag"])

        # connections
        self.connect(self.geom.outwards, self.aero.inwards, "area")

    def _to_occt(self):
        return self.geom._to_occt()
