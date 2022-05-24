import numpy as np
from cosapp.systems import System
from pyoccad.create import CreateAxis, CreateRevolution, CreateTopology, CreateWire
from pyoccad.transform import Scale, Translate

from pyturbo.ports import KeypointsPort


class GenericSimpleGeom(System):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):
        # inwards/outwards
        self.add_input(KeypointsPort, "kp")
        self.add_outward("axial_form_factor", 1.0, unit="", desc="height over length form factor")

    def compute(self):
        l = self.kp.exit_tip_z - self.kp.inlet_tip_z
        assert l
        self.axial_form_factor = (
            np.mean(
                (self.kp.inlet_tip_r - self.kp.inlet_hub_r, self.kp.exit_tip_r - self.kp.exit_hub_r)
            )
            / l
        )

    def to_occt(self):

        w1 = CreateWire.from_points(
            (
                (self.kp.inlet_hub_z, self.kp.inlet_hub_r, 0.0),
                (self.kp.exit_hub_z, self.kp.exit_hub_r, 0.0),
            ),
        )
        w2 = CreateWire.from_points(
            (
                (self.kp.inlet_tip_z, self.kp.inlet_tip_r, 0.0),
                (self.kp.exit_tip_z, self.kp.exit_tip_r, 0.0),
            ),
        )

        inner_shell = CreateRevolution.surface_from_curve(w1, CreateAxis.ox())
        outer_shell = CreateRevolution.surface_from_curve(w2, CreateAxis.ox())

        return CreateTopology.make_compound(inner_shell, outer_shell)
