import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class NozzleGeom(GenericSimpleGeom):
    """
    Nozzle geometry.

    The geometrical envelop is a trapezoidal revolution with fully radial inlet and exit.

    Inputs
    ------
    kp : KeypointPort
        nozzle geometrical envelop

    Outputs
    -------
    area[m**2] : float
        exit area
    """

    def setup(self):
        super().setup()

        # aero
        self.add_outward("area", 1.0, unit="m ** 2", desc="exit area")

    def compute(self):
        # area
        r_tip = self.kp.exit_tip_r
        r_hub = self.kp.exit_hub_r
        self.area = np.pi * (r_tip**2 - r_hub**2)