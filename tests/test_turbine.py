import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.systems import HPT, LPT
from pyturbo.systems.turbine import Turbine


class TestTurbine:
    def test_system_setup(self):
        # default constructor
        sys = Turbine("tur")

        data_input = ["fl_in", "kp"]
        data_inward = []
        data_output = ["fl_out", "sh_out"]
        data_outward = []

        for data in data_input:
            assert data in sys.inputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_output:
            assert data in sys.outputs
        for data in data_outward:
            assert data in sys.outwards

    def test_compute_HPT(self):
        sys = HPT("tur")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 15000.")

        sys.run_drivers()

        assert sys.sh_out.power == pytest.approx(27.1e6, rel=1e-2)
        assert sys.aero.Ncqdes == pytest.approx(101.0, rel=1e-2)

    def test_compute_LPT(self):
        sys = LPT("tur")
        run = sys.add_driver(NonLinearSolver("run"))
        run.add_equation("sh_out.N == 5000.")

        sys.run_drivers()

        assert sys.sh_out.power == pytest.approx(19.8e6, rel=1e-2)
        assert sys.aero.Ncqdes == pytest.approx(105.0, rel=1e-2)
