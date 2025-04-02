# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import numpy as np
from cosapp.systems import System

import pyturbo.systems.compressor.data as cmp_data
from pyturbo.systems.channel import Channel
from pyturbo.systems.compressor import Compressor
from pyturbo.systems.fan_module.fan_module_geom import FanModuleGeom
from pyturbo.systems.fan_module.spinner_geom import SpinnerGeom
from pyturbo.systems.mixers import MixerFluid, MixerShaft
from pyturbo.systems.structures import IntermediateCasing
from pyturbo.utils import JupyterViewable, load_from_json


class FanModule(System, JupyterViewable):
    """Fan assembly model.

    The Fan assembly model is made of:
    - spinner,
    - fan,
    - ogv (outlet guided vanes),
    - booster,
    - ic (intermediate casing),

    Sub-systems
    -----------
    fan: Fan
        rotor
    ogv: Stator
        outlet guided vane in the secondary flow
    booster: Booster
        multi stage compressor link to the LP shaft
    ic: IntermediateCasing
        intermediate casing suports lp shaft front bearings, and forward mounts

    geom: FanModuleGeom
        component kp from fan module kp

    splitter_shaft: MixerShaft
        split power from LP shaft toward booster and fan shaft
    splitter_fluid: MixerFluid
        split fluid flow from fan toward booster and ogv

    Inputs
    ------
    kp: KeypointsPort
        fan module geometrical envelop
    fl_in: FluidPort
        fluid going into the fan madule
    sh_in: FluidShaft
        shaft driving the fan madule

    Outputs
    -------
    fl_booster: FluidPort
        fluid leaving the booster
    fl_ogv: FluidPort
        fluid leaving the ogv

    bpr[-]: float, default=1.0
        by pass ratio = secondary flow / primary flow
    pr[-]: float, default=1.0
        pressure ration = fan.pr * booster.pr

    Good practice
    -------------
    1:
        init mass flow split between booster and fan at the good level of magnitude
    2:
        init mass flow split between booster shaft and fan shaft at the good level of magnitude
    """

    def setup(self):
        # component
        self.add_child(Compressor("fan"), pulling=["N"])
        self.add_child(Compressor("booster"))
        self.add_child(Channel("ogv"))
        self.add_child(IntermediateCasing("ic"), pulling=["fl_core", "fl_bypass"])
        self.add_child(SpinnerGeom("spinner"))

        load_from_json(self.fan, Path(cmp_data.__file__).parent / "fan.json")
        load_from_json(self.booster, Path(cmp_data.__file__).parent / "booster.json")

        # physics
        self.add_child(FanModuleGeom("geom"), pulling=["fan_diameter", "length"])

        # numerics
        self.add_child(
            MixerShaft("splitter_shaft", output_shafts=["sh_fan", "sh_booster"]), pulling=["sh_in"]
        )
        self.add_child(
            MixerFluid("splitter_fluid", output_fluids=["fl_fan", "fl_booster"]), pulling=["fl_in"]
        )

        # exec order
        self.exec_order = [
            "geom",
            "splitter_shaft",
            "splitter_fluid",
            "fan",
            "booster",
            "ogv",
            "ic",
            "spinner",
        ]

        # Fluid ports connectors
        self.connect(self.splitter_fluid.fl_fan, self.fan.fl_in)
        self.connect(self.splitter_fluid.fl_booster, self.booster.fl_in)

        self.connect(self.booster.fl_out, self.ic.fl_booster)

        self.connect(self.fan.fl_out, self.ogv.fl_in)
        self.connect(self.ogv.fl_out, self.ic.fl_ogv)

        # Shaft ports connectors
        self.connect(self.splitter_shaft.sh_fan, self.fan.sh_in)
        self.connect(self.splitter_shaft.sh_booster, self.booster.sh_in)

        # geometry connectors
        self.connect(self.geom.fan_kp, self.fan.kp)
        self.connect(self.geom.booster_kp, self.booster.kp)
        self.connect(self.geom.ogv_kp, self.ogv.kp)
        self.connect(self.geom.ic_kp, self.ic.kp)
        self.connect(
            self.geom,
            self.spinner,
            {
                "fan_hub_kp": "fan_hub_kp",
                "spinner_apex_kp": "apex_kp",
                "spinner_angle": "mean_angle",
            },
        )

        # inwards/outwards
        self.add_outward("bpr", 1.0, unit="", desc="By pass ratio")
        self.add_outward("fan_pr", 1.0, unit="", desc="fan pressure ratio")
        self.add_outward("booster_pr", 1.0, unit="", desc="booster pressure ratio")

        # init
        self.sh_in.power = 20e6
        self.sh_in.N = 5100.0
        self.fl_in.W = 350.0

        self.splitter_shaft.power_fractions = np.r_[0.9]
        self.splitter_fluid.fluid_fractions = np.r_[0.8]

    def compute(self):
        self.bpr = self.splitter_fluid.fl_fan.W / self.splitter_fluid.fl_booster.W
        self.fan_pr = self.fan.pr
        self.booster_pr = self.booster.pr

    def _to_occt(self):
        return dict(
            spinner=self.spinner._to_occt(),
            fan=self.fan.geom._to_occt(),
            booster=self.booster.geom._to_occt(),
            ogv=self.ogv.geom._to_occt(),
            ic=self.ic.geom._to_occt(),
        )
