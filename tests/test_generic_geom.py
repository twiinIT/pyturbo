import numpy as np

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class TestGenericSimpleGeom:
    def test_setup(self):
        # default constructor
        sys = GenericSimpleGeom("sys")

        inputs = ["kp"]
        outwards = ["axial_form_factor"]

        for p in inputs:
            assert p in sys.inputs
        for v in outwards:
            assert v in sys.outwards

    def test_compute_generic_geom(self):
        sys = GenericSimpleGeom("sys")

        sys.kp.inlet_hub = np.r_[0.0, 0.5]
        sys.kp.inlet_tip = np.r_[0.5, 0.5]
        sys.kp.exit_hub = np.r_[0.5, 1.5]
        sys.kp.exit_tip = np.r_[1.0, 1.5]

        sys.compute()
        assert sys.axial_form_factor == 0.5
