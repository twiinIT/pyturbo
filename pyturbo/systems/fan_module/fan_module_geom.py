import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class FanModuleGeom(System):
    """
    Fan module geometry

    Components
    ----------
    fan : Compressor
        rotor
    ogv : Stator
        outlet guided vane in the secondary flow
    booster : Compressor
        multi stage compressor link to the LP shaft
    ic : IntermediateCasing
        intermediate casing suports lp shaft front bearings, and forward mounts

                   --------------------------------
                   |         |         |          |
                   |   fan   |         |   ic     |
                   |         |   ogv   |          |
                   |         |         |          |
                   |         |---------|          |
                   |         | booster |          |
        spinner  _/|         |---------|----------|
               _/  |         |    shaft funnel    |
             _/____|_________|____________________|


    Physics
    -------

    Parameters
    ----------

    Inputs
    ------
    kp : KeypointPort

    Outputs
    -------
    fan_kp : KeypointPort
    ogv_kp : KeypointPort
    booster_kp : KeypointPort
    ic_kp : KeypointPort
    shaft_kp : KeypointPort

    Inwards
    -------
    fan_length_ratio : float
        fan length relative to fan module length

    fan_hub_radius_ratio : float
        fan hub radius ratio

    booster_length_ratio : float
        booster length relative to fan module length

    booster_radius_ratio : float
        booster tip radius relative to fan module radius

    shaft_radius_ratio : float
        shaft radius relative to fan module tip radius

    Good practice
    -------------
    """

    def setup(self):
        self.add_inward("length", 0.8, unit="m", desc="fan module length")
        self.add_inward("fan_diameter", 1.0, unit="m", desc="fan module diameter")
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
        self.add_inward(
            "spinner_angle",
            40.0,
            unit="deg",
            desc="fan spinner angle",
        )
        self.add_inward(
            "fan_to_splitter_axial_gap",
            0.02,
            unit="",
            desc="fan to splitter axial gap as a ratio of fan diameter",
        )

        self.add_output(KeypointsPort, "fan_kp")
        self.add_output(KeypointsPort, "ogv_kp")
        self.add_output(KeypointsPort, "booster_kp")
        self.add_output(KeypointsPort, "ic_kp")
        self.add_output(KeypointsPort, "shaft_kp")
        self.add_outward("fan_hub_kp", np.ones(2))
        self.add_outward("spinner_apex_kp", np.ones(2))
        self.add_outward("fan_inlet_hub_kp", np.ones(2))

    def compute(self):
        # set keypoints to internal components
        length = self.length
        radius = self.fan_diameter / 2.0

        fan_exit_z = self.fan_length_ratio * length
        splitter_gap = self.fan_to_splitter_axial_gap * self.fan_diameter
        booster_inlet_z = fan_exit_z + splitter_gap
        booster_exit_z = booster_inlet_z + self.booster_length_ratio * length

        booster_r = radius * self.booster_radius_ratio
        shaft_r = radius * self.shaft_radius_ratio

        # fan
        self.fan_kp.inlet_hub = np.r_[0.0, 0.0]
        self.fan_kp.inlet_tip = np.r_[radius, 0.0]
        self.fan_kp.exit_hub = np.r_[0.0, booster_inlet_z]
        self.fan_kp.exit_tip = np.r_[radius, booster_inlet_z]
        self.fan_inlet_hub_kp = np.r_[radius * self.fan_hub_radius_ratio, 0.0]

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
        self.fan_hub_kp = self.fan_inlet_hub_kp
        fan_hub_r, fan_hub_z = self.fan_inlet_hub_kp
        self.spinner_apex_kp = np.r_[
            0.0, fan_hub_z - fan_hub_r / np.tan(np.radians(self.spinner_angle))
        ]
