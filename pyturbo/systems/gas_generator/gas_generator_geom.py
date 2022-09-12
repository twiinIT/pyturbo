import numpy as np
from cosapp.systems import System

from pyturbo.ports import KeypointsPort


class GasGeneratorGeom(System):
    """
    A simple gas generator geometrical model.

    This model defines the gas generator keypoints {r, z} coordinates. It is made of:
    
    - compressor
    - combustor
    - tubine

    Sub-systems
    -----------
    compressor: Compressor
        compressor
    combustor: Combustor
        combustor
    turbine: Turbine
        turbine

    Inputs
    ------
    kp: KeypointPort
        gas generator geometrical envelop

    compressor_length_ratio[-]: float
        compressor length over gg length ratio
    turbine_length_ratio[-]: float
        turbine length over gg length ratio

    Outputs
    -------
    compressor_kp: KeypointPort
        compressor geometrical envelop
    combustor_kp: KeypointPort
        combustor geometrical envelop
    turbine_kp: KeypointPort
        turbine geometrical envelop
    """

    def setup(self):
        # inputs/outputs
        self.add_input(KeypointsPort, "kp")
        for subsystem in ["compressor", "combustor", "turbine"]:
            self.add_output(KeypointsPort, f"{subsystem}_kp")

        # inwards
        self.add_inward(
            "compressor_length_ratio", 0.5, desc="compressor over gas generator length ratio"
        )
        self.add_inward("turbine_length_ratio", 0.2, desc="")

        # init
        self.kp.inlet_hub = np.r_[0.0, 0.0]
        self.kp.inlet_tip = np.r_[0.25, 0.0]
        self.kp.exit_hub = np.r_[0.0, 0.4]
        self.kp.exit_tip = np.r_[0.5, 0.4]

    def compute(self):
        # compute lengths
        length = self.turbine_kp.exit_hub_z - self.compressor_kp.inlet_hub_z
        cmp_length = length * self.compressor_length_ratio
        trb_length = length * self.turbine_length_ratio

        # compressor/combustor interface
        # constant compressor internal and external radii
        self.compressor_kp.inlet_hub = self.kp.inlet_hub
        self.compressor_kp.inlet_tip = self.kp.inlet_tip
        self.compressor_kp.exit_hub = self.kp.inlet_hub + np.r_[0.0, cmp_length]
        self.compressor_kp.exit_tip = self.kp.inlet_tip + np.r_[0.0, cmp_length]

        # combustor/turbine interface
        # constant turbine internal and external radii
        self.turbine_kp.exit_hub = self.kp.exit_hub
        self.turbine_kp.exit_tip = self.kp.exit_tip
        self.turbine_kp.inlet_hub = self.kp.exit_hub - np.r_[0.0, trb_length]
        self.turbine_kp.inlet_tip = self.kp.exit_tip - np.r_[0.0, trb_length]

        # combustor interfaces
        self.combustor_kp.inlet_hub = self.compressor_kp.exit_hub
        self.combustor_kp.inlet_tip = self.compressor_kp.exit_tip
        self.combustor_kp.exit_hub = self.turbine_kp.inlet_hub
        self.combustor_kp.exit_tip = self.turbine_kp.inlet_tip
