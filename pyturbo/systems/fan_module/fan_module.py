# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.systems.compressor import Compressor
from pyturbo.systems.fan_module import FanModuleGeom
from pyturbo.systems.generic import GenericSimpleView, GenericSystemView
from pyturbo.systems.mixers import MixerFluid, MixerShaft
from pyturbo.systems.structures import Channel, IntermediateCasing


class FanModule(System):
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

        splitter_shaft: MixerShaft
            split power from LP shaft toward booster and fan shaft
        splitter_fluid: MixerFluid
            split fluid flow from fan toward booster and ogv

        geom: FanModuleGeom
            sub systems key points generated from the fan module envelop
        view: FanModuleView
            compute visualisation

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
        # properties
        children_name = ["spinner", "fan", "ogv", "booster", "ic"]

        # component
        self.add_child(Compressor("fan", config="fan"), pulling={"N": "N", "pr": "fan_pr"})
        self.add_child(Compressor("booster", config="booster"), pulling={"pr": "booster_pr"})
        self.add_child(Channel("ogv"))
        self.add_child(IntermediateCasing("ic"), pulling=["fl_core", "fl_bypass"])
        self.add_child(GenericSimpleView("spinner"))

        # physics
        self.add_child(FanModuleGeom("geom"), pulling=["kp"])

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

        self.add_child(GenericSystemView("view", children_name=children_name), pulling=["occ_view"])

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
        # connection geom
        for name in children_name:
            self.connect(self.geom[f"{name}_kp"], self[name].kp)
            self.connect(self[name], self.view, {"occ_view": f"{name}_view"})

        # inwards/outwards
        self.add_outward("bpr", 1.0, unit="", desc="By pass ratio")

        # design methods
        scaling = self.add_design_method("scaling")

        scaling.extend(self.fan.design_methods["scaling"])
        scaling.extend(self.booster.design_methods["scaling"])

        # init
        self.sh_in.power = 20e6
        self.sh_in.N = 5100.0
        self.fl_in.W = 450.0

        self.splitter_shaft.power_fractions = np.r_[0.9]
        self.splitter_fluid.fluid_fractions = np.r_[0.8]

    def compute(self):
        self.bpr = self.splitter_fluid.fl_fan.W / self.splitter_fluid.fl_booster.W
