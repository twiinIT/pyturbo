from cosapp.drivers import NonLinearSolver
from numpy import pi

from pyturbo.systems import CompressorSimpleAero, CompressorSimpleGeom
from pyturbo.systems.compressor_simple import CompressorSimple


class TestCompressorSimpleAero:
    def test_setup(self):
        # default constructor
        sys = CompressorSimpleAero("cmp")

        data_input = ["fl_in", "shaft_in"]
        data_inward = ["tip_in_r", "inlet_area", "eff_poly", "phiP"]
        data_output = ["fl_out"]
        data_outward = ["phi", "psi"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimpleAero("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("shaft_in.power")

        # CFM56-3B
        sys.tip_in_r = 0.8
        sys.tip_out_r = 0.8
        sys.inlet_area = pi * sys.tip_in_r**2 * (1 - 0.3**2)
        sys.shaft_in.N = 5500
        sys.shaft_in.power = 5e6

        sys.fl_in.W = 300.0
        sys.fl_in.pt = 1e5
        sys.fl_in.Tt = 288.15

        sys.phiP = 0.4
        sys.eff_poly = 0.8

        sys.run_drivers()

        assert abs(sys.shaft_in.power / 16.8e6 - 1) < 1e-2


class TestCompressorSimpleGeom:
    def test_setup(self):
        # default constructor
        sys = CompressorSimpleGeom("sys")

        data_outward = ["tip_in_r", "tip_out_r", "inlet_area"]

        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimpleGeom("sys")

        sys.hub_in_r_ref = 0.5
        sys.tip_in_r_ref = 1.0
        sys.scale = 1.0

        sys.compute()
        assert abs(sys.inlet_area - pi * (1 - 0.5**2)) < 1e-6


class TestCompressorSimple:
    def test_setup(self):
        # default constructor
        sys = CompressorSimple("cmp")

        data_input = ["fl_in", "shaft_in"]
        data_inward = []
        data_output = ["fl_out"]
        data_outward = []

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute(self):
        sys = CompressorSimple("cmp")
        sys.add_driver(NonLinearSolver("run"))
        sys.add_unknown("shaft_in.power")

        # CFM56-3B
        sys.geom.tip_in_r_ref = 0.8
        sys.geom.hub_in_r_ref = 0.8 * 0.3
        sys.geom.tip_out_r_ref = 0.8

        sys.shaft_in.N = 5500
        sys.shaft_in.power = 5e6

        sys.fl_in.W = 300.0
        sys.fl_in.pt = 1e5
        sys.fl_in.Tt = 288.15

        sys.aero.phiP = 0.4
        sys.aero.eff_poly = 0.8

        sys.run_drivers()

        assert abs(sys.shaft_in.power / 16.7e6 - 1) < 1e-2
