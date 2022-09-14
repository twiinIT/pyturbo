import numpy as np
import pytest

from pyturbo.systems.inlet import Inlet


class TestInlet:
    """Define tests for the inlet assembly model."""

    sys = Inlet("inlet")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["fan_inlet_tip_kp", "fl_in", "pamb"]
        data_output = ["fl_out", "drag", "fl_out", "hilite_kp"]

        for data in data_input:
            assert data in sys.inputs or data in sys.inwards
        for data in data_output:
            assert data in sys.outputs or data in sys.outwards

    def test_run_once(self):
        # basic run
        sys = self.sys

        sys.fan_inlet_tip_kp = np.r_[0.8, 0.0]

        sys.pamb = 1e5
        sys.fl_in.W = 400.0
        sys.fl_in.Pt = 101325.0
        sys.fl_in.Tt = 300.0

        sys.run_once()

        assert sys.drag == pytest.approx(41992, 0.1)
