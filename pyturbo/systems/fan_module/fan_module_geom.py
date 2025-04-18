# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class FanModuleGeom(System):
    """Fan module geometry.

    It computes the key points for the Fan Module Sub-systems:
    - spinner,
    - fan,
    - ogv,
    - booster,
    - ic (intermediate casing)

    Inputs
    ------
    kp: KeypointsPort
        fan module geometrical envelop

    fan_length_ratio[-]: float, default=0.3
        fan length relative to fan module length

    fan_hub_radius_ratio[-]: float, default=0.25
        fan hub radius ratio

    booster_length_ratio[-]: float, default=0.3
        booster length relative to fan module length

    booster_radius_ratio[-]: float, default=0.6
        booster tip radius relative to fan module radius

    shaft_radius_ratio[-]: float, default=0.1
        shaft radius relative to fan module tip radius

    spinner_angle[deg]: float, default=40.0
        fan spinner ang

    fan_to_splitter_axial_gap[-]: float, default=0.02
        fan to splitter axial gap as a ratio of fan diameter

    Outputs
    -------
    fan_kp: KeypointsPort
        fan geometrical envelop
    ogv_kp: KeypointsPort
        ogv geometrical envelop
    booster_kp: KeypointsPort
        booster geometrical envelop
    ic_kp: KeypointsPort
        ic geometrical envelop
    shaft_kp: KeypointsPort
        shaft geometrical envelop

    fan_hub_kp[m]: np.array(2), default=np.ones(2)
        fan inlet hub position
    fan_inlet_hub_kp[m]: np.array(2), default=np.ones(2)
        fan inlet hub position
    spinner_apex_kp[m]: np.array(2), default=np.ones(2)
        spinner inlet hub position
    """

    def setup(self):
        # inputs
        self.add_input(KeypointsPort, "kp")

        # inputs/outputs
        self.add_output(KeypointsPort, "spinner_kp")
        self.add_output(KeypointsPort, "fan_kp")
        self.add_output(KeypointsPort, "ogv_kp")
        self.add_output(KeypointsPort, "booster_kp")
        self.add_output(KeypointsPort, "ic_kp")
        self.add_output(KeypointsPort, "shaft_kp")

        # inwards/outwards
        self.add_inward(
            "fan_length_ratio", 0.3, unit="", desc="fan length relative to fan module length"
        )

        self.add_inward("fan_hub_radius_ratio", 0.25, unit="", desc="fan hub radius ratio")

        self.add_inward(
            "booster_length_ratio",
            0.3,
            unit="",
            desc="booster length relative to fan module length",
        )
        self.add_inward(
            "booster_radius_ratio",
            0.6,
            unit="",
            desc="booster tip radius relative to fan module radius",
        )
        self.add_inward(
            "shaft_radius_ratio",
            0.1,
            unit="",
            desc="shaft radius relative to fan module tip radius",
        )
        self.add_inward("spinner_angle", 40.0, unit="deg", desc="fan spinner angle")
        self.add_inward(
            "fan_to_splitter_axial_gap",
            0.02,
            unit="",
            desc="fan to splitter axial gap as a ratio of fan diameter",
        )

        self.add_outward("fan_hub_kp", np.ones(2), unit="m", desc="fan inlet hub position")
        self.add_outward("spinner_apex_kp", np.ones(2), unit="m", desc="spinner inlet hub position")
        self.add_outward("fan_inlet_hub_kp", np.ones(2), unit="m", desc="fan inlet hub position")

    def compute(self):
        # set keypoints to internal components
        length = self.kp.exit_hub[1] - self.kp.inlet_hub[1]
        radius = self.kp.inlet_tip[0]

        fan_exit_z = self.fan_length_ratio * length
        splitter_gap = self.fan_to_splitter_axial_gap * 2 * radius
        booster_inlet_z = fan_exit_z + splitter_gap
        booster_exit_z = booster_inlet_z + self.booster_length_ratio * length

        booster_r = radius * self.booster_radius_ratio
        shaft_r = radius * self.shaft_radius_ratio

        # fan
        self.fan_kp.inlet_hub = np.r_[0.0, 0.0]
        self.fan_kp.inlet_tip = np.r_[radius, 0.0]
        self.fan_kp.exit_hub = np.r_[0.0, booster_inlet_z]
        self.fan_kp.exit_tip = np.r_[radius, booster_inlet_z]

        # shaft
        self.shaft_kp.inlet_hub = self.fan_kp.exit_hub
        self.shaft_kp.inlet_tip = np.r_[shaft_r, self.fan_kp.exit_hub_z]

        self.shaft_kp.exit_hub = np.r_[0.0, length]
        self.shaft_kp.exit_tip = np.r_[shaft_r, length]

        # booster
        self.booster_kp.inlet_hub = self.shaft_kp.inlet_tip
        self.booster_kp.inlet_tip = np.r_[booster_r, booster_inlet_z]

        self.booster_kp.exit_hub = np.r_[shaft_r, booster_exit_z]
        self.booster_kp.exit_tip = np.r_[booster_r, booster_exit_z]

        # ogv
        self.ogv_kp.inlet_hub = self.booster_kp.inlet_tip
        self.ogv_kp.inlet_tip = self.fan_kp.exit_tip

        self.ogv_kp.exit_hub = self.booster_kp.exit_tip
        self.ogv_kp.exit_tip = np.r_[radius, booster_exit_z]

        # intermediate casing
        self.ic_kp.inlet_hub = self.booster_kp.exit_hub
        self.ic_kp.inlet_tip = self.ogv_kp.exit_tip

        self.ic_kp.exit_hub = self.shaft_kp.exit_tip
        self.ic_kp.exit_tip = np.r_[radius, length]

        # spinner
        r = radius * self.fan_hub_radius_ratio
        z = r / np.tan(np.radians(self.spinner_angle))

        self.spinner_kp.inlet_hub = np.r_[0.0, -z]
        self.spinner_kp.inlet_tip = np.r_[0.0, -z]

        self.spinner_kp.exit_hub = np.r_[0.0, 0.0]
        self.spinner_kp.exit_tip = np.r_[r, 0.0]
