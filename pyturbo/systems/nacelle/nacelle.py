from cosapp.systems import System

from pyturbo.systems.nacelle import NacelleGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Nacelle(System, JupyterViewable):
    """
    Nacelle simple assembly model.

    Physics
    -------
    geom : NacelleGeom

    Inputs
    ------
    kp : KeypointPort
    """

    def setup(self):
        # children
        self.add_child(
            NacelleGeom("geom"),
            pulling=[
                "hilite_kp",
                "ogv_exit_tip_kp",
                # "turbine_exit_tip_kp",
                "sec_nozzle_exit_kp",
                "fan_diameter",
            ],
        )

    def _to_occt(self):
        return self.geom._to_occt()
