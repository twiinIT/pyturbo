import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class ChannelGeom(GenericSimpleGeom):
    """Channel geometry model.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    Inputs
    ------
    kp : KeypointsPort
        nozzle geometrical envelop

    Outputs
    -------
    area_in[m**2]: float, default=1.
        inlet area section
    area_exit[m**2]: float, default=1.
        exit area section
    """

    def setup(self):
        super().setup()

        # aero
        self.add_outward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_outward("area_exit", 1.0, unit="m**2", desc="exit area")

    def compute(self):
        # area
        r_tip = self.kp.inlet_tip_r
        r_hub = self.kp.inlet_hub_r
        self.area_in = np.pi * (r_tip**2 - r_hub**2)

        r_tip = self.kp.exit_tip_r
        r_hub = self.kp.exit_hub_r
        self.area_exit = np.pi * (r_tip**2 - r_hub**2)
