# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class TurbofanGeom(System):
    """Turbofan geometry.

    Reference for all dimensions is fan diameter

    Turbofan module is made of components:
        - inlet
        - fan module
        - gas generator
        - turbine
        - trf (turbine rear frame)
        - primary nozzle
        - fan_duct
        - secondary nozzle
        - plug
        - nacelle
        - shaft

    Pylon attach points are also provided

    Inputs
    ------
    fan_diameter[m]: float, default=1.6
        fan diameter

    inlet_length_ratio[-]: float, default=0.4
        inlet length relative to fan radius
    inlet_radius_ratio[-]: float, default=0.9
        inlet radius relative to fan radius"

    fan_module_length_ratio[-]: float, default=1.0
        fan_module length relative to fan radius
    ogv_exit_hqt[-]: float, default=0.6
        fan OGV exit hub-to-tip ratio

    core_inlet_radius_ratio[-]: float, default=0.25
        high-pressure core inlet radius relative to fan radius
    core_exit_radius_ratio[-]: float, default=0.3
        high-pressure core exit radius relative to fan radius
    core_length_ratio[-]: float, default=3.0
        high-pressure core length relative to its radius

    shaft_radius_ratio[-]: float, default=0.1
        shaft radius relative to fan radius

    tcf_exit_radius_ratio[-]: float, default=1.4
        turbine center frame exit radius relative to inlet one
    tcf_length_ratio[-]: float, default=0.15
        turbine center frame length relative its inlet tip radius

    turbine_radius_ratio[-]: float, default=0.65
        turbine radius relative to fan radius
    turbine_length_ratio[-]: float, default=1.0
        turbine length relative to turbine radius
    turbine_fp_exit_hqt[-]: float, default=0.8
        LPT turbine flowpath exit hub-to-tip ratio
    trf_length_ratio[-]: float, default=0.15
        trf length relative to turbine radius

    core_cowl_slope[deg]: float, default=-20.0
        core cowl slope angle

    secondary_nozzle_length_ratio[-]: float, default=0.2
        secondary nozzle length relative to fan_radius

    pri_nozzle_area_ratio[-]: float, default=0.9
        primary nozzle area ratio
    sec_nozzle_area_ratio[-]: float, default=0.9
        secondary nozzle area ratio

    frd_mount_relative[-]: float, default=0.75
        forward engine mount position relative to tip fan module
    aft_mount_relative[-]: float, default=0.75
        aftward engine mount position relative to tip trf

    Outputs
    -------
    inlet_kp: KeypointsPort
        inlet geometrical envelop
    fan_module_kp: KeypointsPort
        fan module geometrical envelop
    core_kp: KeypointsPort
        core geometrical envelop
    shaft_kp: KeypointsPort
        shaft geometrical envelop
    tcf_kp: KeypointsPort
        turbine center frame geometrical envelop
    turbine_kp: KeypointsPort
        turbine geometrical envelop
    trf_kp: KeypointsPort
        turbine rear frame geometrical envelop
    primary_nozzle_kp: KeypointsPort
        primary nozzle geometrical envelop
    secondary_nozzle_kp: KeypointsPort
        secondary nozzle geometrical envelop

    ogv_exit_hub_kp[m]: np.array(2), default=np.ones(2)
        ogv exit hub position
    ogv_exit_tip_kp[m]: np.array(2), default=np.ones(2)
        ogv exit tip position

    frd_mount[m]: np.array(2), default=np.r_[0.9, 0.5]
        forward engine mount
    aft_mount[m]: np.array(2), default=np.r_[0.9, 0.5]
        aftward engine mount

    fan_module_length[m]: float, default=1.0
        fan module length from fan inlet to intermediate case exit",
    engine_length[m]: float, default=1.0
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
            "fan_module_length_ratio",
            1.0,
            unit="",
            desc="fan_module length relative to fan radius",
        )
        self.add_inward("ogv_exit_hqt", 0.6, unit="", desc="fan OGV exit hub-to-tip ratio")
        self.add_inward(
            "core_inlet_radius_ratio",
            0.25,
            unit="",
            desc="high-pressure core inlet radius relative to fan radius",
        )
        self.add_inward(
            "core_exit_radius_ratio",
            0.3,
            unit="",
            desc="high-pressure core exit radius relative to fan radius",
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
            "tcf_exit_radius_ratio",
            1.2,
            unit="",
            desc="turbine center frame exit radius relative to inlet one",
        )
        self.add_inward(
            "tcf_length_ratio",
            0.15,
            unit="",
            desc="turbine center frame length relative its inlet tip radius",
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

        self.add_inward(
            "core_cowl_slope",
            -10.0,
            unit="deg",
            desc="core_cowl_slope angle relative to horizontal",
        )

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

        self.add_inward(
            "pri_nozzle_area_ratio", 0.9, unit="", desc="primary nozzle exit area ratio"
        )
        self.add_inward(
            "sec_nozzle_area_ratio", 0.6, unit="", desc="secondary nozzle exit area ratio"
        )

        # outwards
        self.add_output(KeypointsPort, "inlet_kp")
        self.add_output(KeypointsPort, "fan_module_kp")
        self.add_output(KeypointsPort, "fan_duct_kp")
        self.add_output(KeypointsPort, "core_kp")
        self.add_output(KeypointsPort, "shaft_kp")
        self.add_output(KeypointsPort, "tcf_kp")
        self.add_output(KeypointsPort, "turbine_kp")
        self.add_output(KeypointsPort, "trf_kp")
        self.add_output(KeypointsPort, "primary_nozzle_kp")
        self.add_output(KeypointsPort, "secondary_nozzle_kp")
        self.add_output(KeypointsPort, "nacelle_kp")

        self.add_outward("ogv_exit_hub_kp", np.ones(2), unit="m")
        self.add_outward("ogv_exit_tip_kp", np.ones(2), unit="m")

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

        # design methods
        scaling = self.add_design_method("scaling")

        scaling.add_unknown("turbine_radius_ratio")
        scaling.add_unknown("core_exit_radius_ratio", max_rel_step=0.8)
        scaling.add_unknown("pri_nozzle_area_ratio", lower_bound=0.05)
        scaling.add_unknown("sec_nozzle_area_ratio", upper_bound=1.0)

    def compute(self):
        # compute radius and lengths
        fan_radius = self.fan_diameter / 2.0

        self.fan_module_length = fan_module_length = fan_radius * self.fan_module_length_ratio

        inlet_radius = fan_radius * self.inlet_radius_ratio
        inlet_length = fan_radius * self.inlet_length_ratio

        core_inlet_radius = fan_radius * self.core_inlet_radius_ratio
        core_exit_radius = fan_radius * self.core_exit_radius_ratio
        core_length = core_inlet_radius * self.core_length_ratio

        shaft_radius = fan_radius * self.shaft_radius_ratio

        turbine_radius = fan_radius * self.turbine_radius_ratio
        turbine_length = turbine_radius * self.turbine_length_ratio

        trf_length = turbine_radius * self.trf_length_ratio

        primary_nozzle_length = turbine_radius * self.primary_nozzle_length_ratio
        secondary_nozzle_length = fan_radius * self.secondary_nozzle_length_ratio

        self.engine_length = fan_module_length + core_length + turbine_length + trf_length

        # fan_module
        self.fan_module_kp.inlet_hub = np.r_[0.0, 0.0]
        self.fan_module_kp.inlet_tip = np.r_[fan_radius, 0.0]
        self.fan_module_kp.exit_hub = self.fan_module_kp.inlet_hub + np.r_[0.0, fan_module_length]
        self.fan_module_kp.exit_tip = self.fan_module_kp.inlet_tip + np.r_[0.0, fan_module_length]

        self.ogv_exit_hub_kp = self.fan_module_kp.exit_tip * np.r_[self.ogv_exit_hqt, 1.0]
        self.ogv_exit_tip_kp = self.fan_module_kp.exit_tip

        # inlet module
        self.inlet_kp.exit_hub = self.fan_module_kp.inlet_hub
        self.inlet_kp.exit_tip = self.fan_module_kp.inlet_tip

        self.inlet_kp.inlet_hub = self.inlet_kp.exit_hub - np.r_[0.0, inlet_length]
        self.inlet_kp.inlet_tip = (
            self.inlet_kp.exit_tip - np.r_[fan_radius - inlet_radius, inlet_length]
        )

        # shaft inlet
        self.shaft_kp.inlet_hub = self.fan_module_kp.exit_hub
        self.shaft_kp.inlet_tip = self.fan_module_kp.exit_hub + np.r_[shaft_radius, 0.0]

        # core
        self.core_kp.inlet_hub = self.shaft_kp.inlet_tip
        self.core_kp.inlet_tip = np.r_[core_inlet_radius, self.core_kp.inlet_hub_z]

        self.core_kp.exit_hub = self.core_kp.inlet_hub + np.r_[0.0, core_length]
        self.core_kp.exit_tip = np.r_[core_exit_radius, self.core_kp.exit_hub_z]

        # tcf
        self.tcf_kp.inlet_hub = self.core_kp.exit_hub
        self.tcf_kp.inlet_tip = self.core_kp.exit_tip

        tcf_length = self.tcf_kp.inlet_tip_r * self.tcf_length_ratio

        self.tcf_kp.exit_hub = self.tcf_kp.inlet_hub + np.r_[0.0, tcf_length]
        self.tcf_kp.exit_tip = (
            self.core_kp.exit_tip * np.r_[self.tcf_exit_radius_ratio, 1.0] + np.r_[0.0, tcf_length]
        )

        # shaft exit
        shaft_length = core_length + tcf_length
        self.shaft_kp.exit_hub = self.shaft_kp.inlet_hub + np.r_[0.0, shaft_length]
        self.shaft_kp.exit_tip = self.shaft_kp.inlet_tip + np.r_[0.0, shaft_length]

        # turbine
        self.turbine_kp.inlet_hub = self.shaft_kp.exit_hub
        self.turbine_kp.inlet_tip = self.tcf_kp.exit_tip

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

        # fan_duct
        z_exit = self.trf_kp.exit_tip[1]
        self.fan_duct_kp.inlet_hub = self.ogv_exit_hub_kp
        self.fan_duct_kp.inlet_tip = self.ogv_exit_tip_kp
        self.fan_duct_kp.exit_hub = np.r_[self.ogv_exit_hub_kp[0], z_exit]
        self.fan_duct_kp.exit_tip = np.r_[self.ogv_exit_tip_kp[0], z_exit]

        # primary nozzle
        z_exit = self.trf_kp.exit_tip[1] + primary_nozzle_length

        self.primary_nozzle_kp.inlet_hub = self.trf_kp.exit_hub
        self.primary_nozzle_kp.inlet_tip = self.trf_kp.exit_tip

        r_inlet_tip = self.primary_nozzle_kp.inlet_tip_r
        r_inlet_hub = self.primary_nozzle_kp.inlet_hub_r
        inlet_area = np.pi * (r_inlet_tip**2 - r_inlet_hub**2)
        exit_area = self.pri_nozzle_area_ratio * inlet_area

        r_exit_tip = r_inlet_tip * (1 + np.sin(np.radians(self.core_cowl_slope)))
        r_exit_hub = np.sqrt(r_exit_tip**2 - exit_area / np.pi)

        self.primary_nozzle_kp.exit_hub = np.r_[r_exit_hub, z_exit]
        self.primary_nozzle_kp.exit_tip = np.r_[r_exit_tip, z_exit]

        # secondary nozzle
        z_exit = self.trf_kp.exit_tip[1] + secondary_nozzle_length

        self.secondary_nozzle_kp.inlet_hub = self.fan_duct_kp.exit_hub
        self.secondary_nozzle_kp.inlet_tip = self.fan_duct_kp.exit_tip

        r_inlet_tip = self.secondary_nozzle_kp.inlet_tip_r
        r_inlet_hub = self.secondary_nozzle_kp.inlet_hub_r
        inlet_area = np.pi * (r_inlet_tip**2 - r_inlet_hub**2)
        exit_area = self.sec_nozzle_area_ratio * inlet_area

        r_exit_hub = r_exit_tip
        r_exit_tip = np.sqrt(r_exit_hub**2 + exit_area / np.pi)

        self.secondary_nozzle_kp.exit_hub = np.r_[r_exit_hub, z_exit]
        self.secondary_nozzle_kp.exit_tip = np.r_[r_exit_tip, z_exit]

        # nacelle
        self.nacelle_kp.inlet_hub = self.inlet_kp.inlet_hub
        self.nacelle_kp.inlet_tip = self.inlet_kp.inlet_tip
        self.nacelle_kp.exit_hub = np.r_[0.0, self.secondary_nozzle_kp.inlet_hub[1]]
        self.nacelle_kp.exit_tip = self.secondary_nozzle_kp.inlet_tip

        # mounts
        r = self.frd_mount_relative
        self.frd_mount = (1 - r) * self.fan_module_kp.inlet_tip + r * self.fan_module_kp.exit_tip
        r = self.aft_mount_relative
        self.aft_mount = (1 - r) * self.trf_kp.inlet_tip + r * self.trf_kp.exit_tip
