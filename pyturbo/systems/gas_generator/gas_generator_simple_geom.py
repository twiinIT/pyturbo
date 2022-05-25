# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class GasGeneratorSimpleGeom(System):
    """A simple gas generator geometrical model.

    This model defines the gas generator keypoints {r, z} coordinates.
    """

    def setup(self):
        # inwards/outwards
        self.add_inward("scale", 1.0, desc="gas generator scale")
        self.add_input(KeypointsPort, "kp")

        self.add_inward("compressor_length_ratio", 0.5, desc="")
        self.add_inward(
            "compressor_exit_radius_ratio", 0.9, desc="compressor exit hub over tip radius ratio"
        )
        self.add_inward("turbine_length_ratio", 0.2, desc="")

        for subsystem in ["compressor", "combustor", "turbine"]:
            self.add_output(KeypointsPort, f"{subsystem}_kp")

        lenght_des = self.add_design_method("length").add_unknown("kp.exit_tip[1]")
        cmp_lenght_des = self.add_design_method("compressor_length").add_unknown(
            "compressor_length_ratio"
        )
        trb_length_des = self.add_design_method("turbine_length").add_unknown(
            "turbine_length_ratio"
        )

        self.add_design_method("sizing").extend(lenght_des).extend(cmp_lenght_des).extend(
            trb_length_des
        ).add_unknown("scale")

    def compute(self):
        # external keypoints/interfaces
        # ensure axial positions are equal
        self.kp.inlet_hub[1] = self.kp.inlet_tip_z
        self.kp.exit_hub[1] = self.kp.exit_tip_z
        # set keypoints to internal components
        self.compressor_kp.inlet_hub = self.kp.inlet_hub * self.scale
        self.compressor_kp.inlet_tip = self.kp.inlet_tip * self.scale
        self.turbine_kp.exit_hub = self.kp.exit_hub * self.scale
        self.turbine_kp.exit_tip = self.kp.exit_tip * self.scale

        # compute lengths
        length = self.turbine_kp.exit_hub_z - self.compressor_kp.inlet_hub_z
        cmp_length = self.compressor_kp.inlet_hub_z + length * self.compressor_length_ratio
        trb_length = self.turbine_kp.exit_hub_z - length * self.turbine_length_ratio

        # compressor/combustor interface
        # constant compressor internal and external radii
        self.compressor_kp.exit_hub = np.r_[
            self.compressor_kp.inlet_tip_r * self.compressor_exit_radius_ratio, cmp_length
        ]
        self.compressor_kp.exit_tip = np.r_[self.compressor_kp.inlet_tip_r, cmp_length]
        # combustor inlet
        self.combustor_kp.inlet_hub = self.compressor_kp.exit_hub
        self.combustor_kp.inlet_tip = self.compressor_kp.exit_tip

        # combustor/turbine interface
        # constant turbine internal and external radii
        self.turbine_kp.inlet_hub = np.r_[self.turbine_kp.exit_hub_r, trb_length]
        self.turbine_kp.inlet_tip = np.r_[self.turbine_kp.exit_tip_r, trb_length]
        # combustor exit
        self.combustor_kp.exit_hub = self.turbine_kp.inlet_hub
        self.combustor_kp.exit_tip = self.turbine_kp.inlet_tip
