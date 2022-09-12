import numpy as np
from cosapp.systems import System

from pyturbo.ports import C1Keypoint, KeypointsPort
from pyturbo.utils import slope_to_drdz


class TurbofanGeom(System):
    r"""
    Turbofan geometry

    Reference for all dimensions is fan diameter

    Turbofan module is made of components:
        - inlet
        - fan module
        - gas generator
        - turbine
        - trf (turbine rear frame)
        - primary nozzle
        - secondary nozzle
        - plug
        - nacelle
        - shaft

    Pylon attach points are also provided

    Inputs
    ------
    fan_diameter[m]: float
        fan diameter

    inlet_length_ratio[-]: float
        inlet length relative to fan radius
    inlet_radius_ratio[-]: float
        inlet radius relative to fan radius"

    fanmodule_length_ratio[-]:
        fanmodule length relative to fan radius
    ogv_exit_hqt[-]: float
        fan OGV exit hub-to-tip ratio

    core_radius_ratio[-]: float
        high-pressure core radius relative to fan radius
    core_length_ratio[-]:
        high-pressure core length relative to its radius

    shaft_radius_ratio[-]: float
        shaft radius relative to fan radius

    turbine_radius_ratio[-]: float
        turbine radius relative to fan radius
    turbine_length_ratio[-]: float
        turbine length relative to turbine radius
    turbine_fp_exit_hqt[-]: float
        LPT turbine flowpath exit hub-to-tip ratio
    trf_length_ratio[-]: float
        trf length relative to turbine radius

    core_cowl_slope[deg]: float
        core cowl slope angle

    primary_nozzle_length_ratio[-]: float
        primary nozzle length relative to TRF radius

    secondary_nozzle_length_ratio[-]: float
        secondary nozzle length relative to fan_radius

    pri_nozzle_area[-]: float
        primary nozzle exit area
    sec_nozzle_area[-]: float
        secondary nozzle exit area

    frd_mount_relative[-]: float
        forward engine mount position relative to tip fan module
    aft_mount_relative[-]: float
        aftward engine mount position relative to tip trf

    Outputs
    -------
    inlet_kp: KeypointsPort
        inlet geometrical envelop
    fanmodule_kp: KeypointsPort
        fan module geometrical envelop
    core_kp: KeypointsPort
        core geometrical envelop
    shaft_kp: KeypointsPort
        shaft geometrical envelop
    turbine_kp: KeypointsPort
        turbine geometrical envelop
    trf_kp: KeypointsPort
        trf geometrical envelop
    primary_nozzle_kp: KeypointsPort
        primary nozzle geometrical envelop
    secondary_nozzle_kp: KeypointsPort
        secondary nozzle geometrical envelop

    fan_inlet_tip_kp[m]: np.array(2)
        fan inlet tip position
    ogv_exit_hub_kp[m]: np.array(2)
        ogv exit hub position
    ogv_exit_tip_kp[m]: np.array(2)
        ogv exit tip position
    turbine_exit_tip_kp[m]: np.array(2)
        turbine exit tip position
    pri_nozzle_exit_kp: C1Keypoint
        primary nozzle exit position
    sec_nozzle_exit_kp[m]: np.array(2)
        secondary nozzle exit tip position
    sec_nozzle_exit_hub_kp: C1Keypoint
        secondary nozzle exit hub position
 
    frd_mount[m]: np.array(2)
        forward engine mount
    aft_mount[m]: np.array(2)
        aftward engine mount

    fan_module_length[m]: float
        fan module length from fan inlet to intermediate case exit",
    engine_length[m]: float
        engine length from fan module to trf
    """

    def setup(self):
        # inwards
        self.add_inward("fan_diameter", 1.6, unit="m", desc="fan diameter")

        self.add_inward(
            "inlet_length_ratio",
            0.4,
            unit="",
            desc="inlet length relative to fan radius",
        )
        self.add_inward(
            "inlet_radius_ratio",
            0.9,
            unit="",
            desc="inlet radius relative to fan radius",
        )

        self.add_inward(
            "fanmodule_length_ratio",
            1.0,
            unit="",
            desc="fanmodule length relative to fan radius",
        )
        self.add_inward("ogv_exit_hqt", 0.6, unit="", desc="fan OGV exit hub-to-tip ratio")
        self.add_inward(
            "core_radius_ratio",
            0.25,
            unit="",
            desc="high-pressure core radius relative to fan radius",
        )
        self.add_inward(
            "core_length_ratio",
            3.0,
            unit="",
            desc="high-pressure core length relative to its radius",
        )

        self.add_inward(
            "shaft_radius_ratio",
            0.1,
            unit="",
            desc="shaft radius relative to fan radius",
        )
        self.add_inward(
            "turbine_radius_ratio",
            0.65,
            unit="",
            desc="turbine radius relative to fan radius",
        )
        self.add_inward(
            "turbine_length_ratio",
            1.0,
            unit="",
            desc="turbine length relative to turbine radius",
        )
        self.add_inward(
            "turbine_fp_exit_hqt", 0.8, unit="", desc="LPT turbine flowpath exit hub-to-tip ratio"
        )
        self.add_inward(
            "trf_length_ratio",
            0.15,
            unit="",
            desc="trf length relative to turbine radius",
        )
        self.add_inward("core_cowl_slope", -20.0, unit="deg", desc="core cowl slope angle")

        self.add_inward(
            "primary_nozzle_length_ratio",
            0.5,
            unit="",
            desc="primary nozzle length relative to TRF radius",
        )

        self.add_inward(
            "secondary_nozzle_length_ratio",
            0.2,
            unit="",
            desc="secondary nozzle length relative to fan_radius",
        )

        self.add_inward(
            "frd_mount_relative",
            0.75,
            desc="forward engine mount position relative to tip fan module",
        )
        self.add_inward(
            "aft_mount_relative", 0.75, desc="aftward engine mount position relative to tip trf"
        )

        self.add_inward("pri_nozzle_area", 0.3, desc="primary nozzle exit area")

        self.add_inward("sec_nozzle_area", 1.0, desc="secondary nozzle exit area")

        # outwards
        self.add_output(KeypointsPort, "inlet_kp")
        self.add_output(KeypointsPort, "fanmodule_kp")
        self.add_output(KeypointsPort, "core_kp")
        self.add_output(KeypointsPort, "shaft_kp")
        self.add_output(KeypointsPort, "turbine_kp")
        self.add_output(KeypointsPort, "trf_kp")
        self.add_output(KeypointsPort, "primary_nozzle_kp")
        self.add_output(KeypointsPort, "secondary_nozzle_kp")

        self.add_outward("fan_inlet_tip_kp", np.ones(2), unit="m")
        self.add_outward("ogv_exit_hub_kp", np.ones(2), unit="m")
        self.add_outward("ogv_exit_tip_kp", np.ones(2), unit="m")
        self.add_outward("turbine_exit_tip_kp", np.ones(2), unit="m")
        self.add_outward("pri_nozzle_exit_kp", C1Keypoint())
        self.add_outward("sec_nozzle_exit_kp", np.ones(2), unit="m")

        self.add_outward("sec_nozzle_exit_hub_kp", C1Keypoint())

        self.add_outward("frd_mount", np.r_[0.9, 0.5], desc="forward engine mount")
        self.add_outward("aft_mount", np.r_[0.5, 3.0], desc="aftward engine mount")
        self.add_outward(
            "fan_module_length",
            1.0,
            unit="m",
            desc="fan module length from fan inlet to intermediate case exit",
        )
        self.add_outward(
            "engine_length", 1.0, unit="m", desc="engine length from fan module to trf"
        )

    def compute(self):
        # set keypoints to internal components
        fan_radius = self.fan_diameter / 2.0

        self.fan_module_length = fanmodule_length = fan_radius * self.fanmodule_length_ratio

        inlet_radius = fan_radius * self.inlet_radius_ratio
        inlet_length = fan_radius * self.inlet_length_ratio

        core_radius = fan_radius * self.core_radius_ratio
        core_length = core_radius * self.core_length_ratio

        shaft_radius = fan_radius * self.shaft_radius_ratio

        turbine_radius = fan_radius * self.turbine_radius_ratio
        turbine_length = turbine_radius * self.turbine_length_ratio

        trf_length = turbine_radius * self.trf_length_ratio

        primary_nozzle_length = turbine_radius * self.primary_nozzle_length_ratio

        self.engine_length = fanmodule_length + core_length + turbine_length + trf_length

        # fanmodule
        self.fanmodule_kp.inlet_hub = np.r_[0.0, 0.0]
        self.fanmodule_kp.inlet_tip = np.r_[fan_radius, 0.0]
        self.fanmodule_kp.exit_hub = self.fanmodule_kp.inlet_hub + np.r_[0.0, fanmodule_length]
        self.fanmodule_kp.exit_tip = self.fanmodule_kp.inlet_tip + np.r_[0.0, fanmodule_length]

        self.fan_inlet_tip_kp = self.fanmodule_kp.inlet_tip
        self.ogv_exit_hub_kp = self.fanmodule_kp.exit_tip * np.r_[self.ogv_exit_hqt, 1.0]
        self.ogv_exit_tip_kp = self.fanmodule_kp.exit_tip

        # inlet module
        self.inlet_kp.exit_hub = self.fanmodule_kp.inlet_hub
        self.inlet_kp.exit_tip = self.fanmodule_kp.inlet_tip

        self.inlet_kp.inlet_hub = np.r_[0.0, self.fanmodule_kp.inlet_hub_z - inlet_length]
        self.inlet_kp.inlet_tip = np.r_[inlet_radius, self.fanmodule_kp.inlet_hub_z - inlet_length]

        # shaft
        self.shaft_kp.inlet_hub = self.fanmodule_kp.exit_hub
        self.shaft_kp.inlet_tip = self.fanmodule_kp.exit_hub + np.r_[shaft_radius, 0.0]

        self.shaft_kp.exit_hub = self.shaft_kp.inlet_hub + np.r_[0.0, core_length]
        self.shaft_kp.exit_tip = self.shaft_kp.inlet_tip + np.r_[0.0, core_length]

        # core
        self.core_kp.inlet_hub = self.shaft_kp.inlet_tip
        self.core_kp.inlet_tip = self.shaft_kp.inlet_hub + np.r_[core_radius, 0.0]

        self.core_kp.exit_hub = self.core_kp.inlet_hub + np.r_[0.0, core_length]
        self.core_kp.exit_tip = self.core_kp.inlet_tip + np.r_[0.0, core_length]

        # turbine
        self.turbine_kp.inlet_hub = self.shaft_kp.exit_hub
        self.turbine_kp.inlet_tip = self.core_kp.exit_tip

        trb_exit_z = self.turbine_kp.inlet_hub_z + turbine_length
        self.turbine_kp.exit_hub = np.r_[self.turbine_kp.inlet_hub_r, trb_exit_z]
        self.turbine_kp.exit_tip = np.r_[turbine_radius, trb_exit_z]

        # trf
        lpt_fp_exit_hub_r = self.turbine_fp_exit_hqt * self.turbine_kp.exit_tip_r
        self.trf_kp.inlet_hub = np.r_[lpt_fp_exit_hub_r, self.turbine_kp.exit_hub_z]
        self.trf_kp.inlet_tip = self.turbine_kp.exit_tip

        trf_exit_z = self.trf_kp.inlet_hub_z + trf_length
        self.trf_kp.exit_hub = np.r_[self.trf_kp.inlet_hub_r, trf_exit_z]
        self.trf_kp.exit_tip = np.r_[self.trf_kp.inlet_tip_r, trf_exit_z]

        # primary nozzle
        self.primary_nozzle_kp.inlet_hub = self.trf_kp.exit_hub
        self.primary_nozzle_kp.inlet_tip = self.trf_kp.exit_tip

        self.primary_nozzle_kp.exit_hub = (
            self.primary_nozzle_kp.inlet_hub + np.r_[0.0, primary_nozzle_length]
        )
        self.primary_nozzle_kp.exit_tip = np.r_[
            np.sqrt(self.pri_nozzle_area / np.pi + self.primary_nozzle_kp.inlet_hub_r**2),
            self.trf_kp.exit_tip_z,
        ]

        min_dz = (self.primary_nozzle_kp.exit_tip_r - self.trf_kp.exit_tip_r) / np.tan(
            np.radians(self.core_cowl_slope)
        )
        dz = max(min_dz, primary_nozzle_length)
        dr = dz * np.tan(np.radians(self.core_cowl_slope))

        self.pri_nozzle_exit_kp.rz = self.trf_kp.exit_tip + np.r_[dr, dz]
        self.pri_nozzle_exit_kp.drdz = slope_to_drdz(self.core_cowl_slope)

        # secondary nozzle
        self.secondary_nozzle_kp.inlet_hub = self.ogv_exit_hub_kp
        self.secondary_nozzle_kp.inlet_tip = self.ogv_exit_tip_kp

        sec_noz_tip_z = (
            self.turbine_kp.exit_tip_z - self.fanmodule_kp.exit_tip_z
        ) * 0.85 + self.fanmodule_kp.exit_tip_z
        dz = self.trf_kp.exit_tip_z - sec_noz_tip_z
        dr = -dz * np.tan(np.radians(self.core_cowl_slope))
        sec_noz_hub_r = self.trf_kp.exit_tip_r + dr
        self.secondary_nozzle_kp.exit_hub = np.r_[sec_noz_hub_r, sec_noz_tip_z]

        sec_noz_tip_r = np.sqrt(self.sec_nozzle_area / np.pi + sec_noz_hub_r**2)
        self.secondary_nozzle_kp.exit_tip = np.r_[sec_noz_tip_r, sec_noz_tip_z]

        self.sec_nozzle_exit_hub_kp.rz = self.secondary_nozzle_kp.exit_hub
        self.sec_nozzle_exit_hub_kp.drdz = slope_to_drdz(self.core_cowl_slope)

        # nacelle
        self.turbine_exit_tip_kp = self.turbine_kp.exit_tip
        self.sec_nozzle_exit_kp = self.secondary_nozzle_kp.exit_tip

        # mounts
        r = self.frd_mount_relative
        self.frd_mount = (1 - r) * self.fanmodule_kp.inlet_tip + r * self.fanmodule_kp.exit_tip
        r = self.aft_mount_relative
        self.aft_mount = (1 - r) * self.trf_kp.inlet_tip + r * self.trf_kp.exit_tip
