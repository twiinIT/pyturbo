import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class CompressorGeom(GenericSimpleGeom):
    """
    Compressor geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit. 
    The geometry exposed to aero module is made of:
      - inlet area
      - inlet and exit tip radius

    Inputs
    ------
    kp: KeypointPort
        compressor geometrical envelop

    stage_count: integer
        number of stages

    blade_height_ratio[-]: float
        inlet blade height relative to compressor inlet tip radius

    Outputs
    -------
    tip_in_r[m]: float
        inlet tip radius
    tip_out_r[m]: float
        exit tip radius
    inlet_area[m**2]: float
        inlet area
    """

    def setup(self):
        super().setup()

        self.add_inward("stage_count", 1, unit="", desc="number of stages")
        self.add_inward(
            "blade_hub_to_tip_ratio",
            0.2,
            unit="",
            desc="blade hub-to-tip radius ratio",
        )

        # aero outputs
        self.add_outward("inlet_area", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_outward("tip_out_r", 1.0, unit="m", desc="exit tip radius")

    def compute(self):
        super().compute()

        # aero outputs
        hub_in_r = self.kp.inlet_tip_r * self.blade_hub_to_tip_ratio

        self.inlet_area = np.pi * (self.kp.inlet_tip_r**2 - hub_in_r**2)
        self.tip_in_r = self.kp.inlet_tip_r
        self.tip_out_r = self.kp.exit_tip_r
