# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class CompressorSimpleGeom(GenericSimpleGeom):
    """Compressor geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    The geometry exposed to aero module is made of:
      - inlet area
      - inlet and exit tip radius
    """

    def setup(self, stage_count: int = 1):
        super().setup()

        self.add_inward("stage_count", 1)
        self.add_inward("h_over_cx", 1.0, unit="", desc="height over axial chord ratio of a row")

        # aero outputs
        self.add_outward("inlet_area", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_outward("tip_out_r", 1.0, unit="m", desc="exit tip radius")

        # design method
        self.add_design_method("axial_length").add_equation(
            "axial_form_factor == h_over_cx / (2. * stage_count)"
        )

    def compute(self):
        super().compute()

        self.inlet_area = np.pi * (self.kp.inlet_tip_r**2 - self.kp.inlet_hub_r**2)
        self.tip_in_r = self.kp.inlet_tip_r
        self.tip_out_r = self.kp.exit_tip_r
