from cosapp.systems import System

from pyturbo.systems.nacelle import PlugGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Plug(System, JupyterViewable):
    """
    Plug assembly model.

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
            PlugGeom("geom"),
            pulling=["trf_exit_hub_kp"],
        )

    def _to_occt(self):
        return self.geom._to_occt()
