import numpy as np
from cosapp.systems import System

from pyturbo.systems.turbine.turbine_aero import TurbineAero
from pyturbo.systems.turbine.turbine_geom import TurbineGeom
from pyturbo.utils.jupyter_view import JupyterViewable


class Turbine(System, JupyterViewable):
    """
    Turbine simple assembly model.

    Sub-systems
    -----------
    geom: TurbineGeom
        geometry value from envelop
    aero: TurbineAero
        performance characteristics

    Inputs
    ------
    stage_count: integer
        number of stages

    kp: KeypointPort
        geometrical envelop
    fl_in: FluidPort
        inlet gas

    Outputs
    -------
    fl_out: FluidPort
        exit gas
    sh_out: ShaftPort
        exit shaft
    fp_exit_hub_kp[m]: np.array(2)
        exit hub flow position

    pr[-]: float
        total to total pressure ratio
    N[rpm]: float
        shaft speed rotation
    """

    def setup(self):
        # children
        self.add_child(
            TurbineGeom("geom"),
            pulling=["stage_count", "kp", "fp_exit_hub_kp"],
        )
        self.add_child(TurbineAero("aero"), pulling=["fl_in", "fl_out", "sh_out", "stage_count"])

        # connections
        self.connect(
            self.geom.outwards,
            self.aero.inwards,
            ["area_in", "mean_radius"],
        )

    def _to_occt(self):
        return dict(geom=self.geom._to_occt())


class HPT(Turbine):
    """High pressure turbine

    It may contain aero and/or geometry sub-models.
    """

    def setup(self):
        super().setup()

        # init param
        self.stage_count = 1

        # init inputs
        self.fl_in.W = 60
        self.fl_in.Tt = 1500.0
        self.fl_in.pt = 33e5

        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.4, 0.0]
        self.kp.exit_hub = np.r_[0.0, 0.1]
        self.kp.exit_tip = np.r_[0.4, 0.1]

        # init geom
        self.geom.blade_height_ratio = 0.2

        # init aero
        self.aero.eff_poly = 0.9
        self.aero.Ncdes = 40.0
        self.aero.er = 4.0


class LPT(Turbine):
    """Low pressure turbine

    It may contain aero and/or geometry sub-models.
    """

    def setup(self):
        super().setup()

        # init param
        self.stage_count = 5

        # init inputs
        self.fl_in.W = 60
        self.fl_in.Tt = 1100.0
        self.fl_in.pt = 8e5

        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.4, 0.0]
        self.kp.exit_hub = np.r_[0.0, 0.4]
        self.kp.exit_tip = np.r_[0.6, 0.4]

        # init geom
        self.geom.blade_height_ratio = 0.4

        # init aero
        self.aero.eff_poly = 0.9
        self.aero.Ncdes = 15.0
        self.aero.er = 4.0
