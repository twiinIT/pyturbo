import numpy as np
from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateBezier, CreateEdge, CreateRevolution

from pyturbo.utils import JupyterViewable, rz_to_3d


class PlugGeom(System, JupyterViewable):
    """
    A plug geometrical model.

    In a turbofan, the plug is the physical part at engine exit (after the
    Turbine Rear Frame TRF) protecting the Low-Pressure Turbine LPT inner
    parts, bearings, etc.
    It also has an aerodynamical function to guide the primary (core) flow
    after the nozzle exit section.

    Parameters
    ----------
    lpt_exit_hub_kp [m] : np.ndarray[2]
        low pressure turbine exit hub keypoint
    LqD [-] : float
        length over diameter ratio (form factor)
    exit_radius_ratio [-] : float
        exit radius over inlet one ratio
    """

    def setup(self):

        # inwards
        self.add_inward(
            "trf_exit_hub_kp",
            np.ones(2),
            unit="m",
            desc="low pressure turbine rear frame exit hub keypoint",
        )
        self.add_inward("LqD", 1.0, unit="", desc="length over diameter ratio (form factor)")

        self.add_inward("exit_radius_ratio", 0.1, unit="", desc="exit radius over inlet one ratio")

        self.add_inward("exit_kp", np.ones(2), unit="m", desc="exit keypoint")

    def compute(self):
        self.exit_kp = (
            self.trf_exit_hub_kp * np.r_[self.exit_radius_ratio, 1.0]
            + np.r_[0.0, self.LqD * self.trf_exit_hub_kp[0] * 2.0]
        )

    def _to_occt(self):
        bezier = CreateBezier.g1_relative_tension(
            rz_to_3d(self.trf_exit_hub_kp),
            rz_to_3d(self.exit_kp),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            0.5,
            0.5,
        )
        e = CreateEdge.from_curve(bezier)

        return CreateRevolution.solid_from_curve(e, CreateAxis.oz())
