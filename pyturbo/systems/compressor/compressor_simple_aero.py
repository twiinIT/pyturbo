from math import sqrt

import numpy as np
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo.ideal_gas import IdealDryAir


class CompressorSimpleAero(System):
    """Compressor aero simple model.

    The methodology is consistent with https://oatao.univ-toulouse.fr/17882
    Binder, Nicolas Aéro-thermodynamique des Turbomachines en Fonctionnement
    Hors-Adaptation. (2016) [HDR]
      - exit flow is computed from inlet one
      - polytropic efficiency is constant
      - aerodynamic load and axial flow velocity are linked using a linear
      modeling
    """

    def setup(self):
        # properties
        self.add_inward("stage_count", 1)
        self.add_property("gas", IdealDryAir())

        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_input(ShaftPort, "shaft_in")

        # geom characteristics
        self.add_inward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_inward("tip_out_r", 1.0, unit="m", desc="exit tip radius")
        self.add_inward("inlet_area", 1.0, unit="m**2", desc="inlet area")

        # aero characteristics
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward("phiP", 0.4, desc="")

        # functional characteristics
        self.add_outward("utip", 0.0, unit="m/s", desc="tip speed")
        self.add_outward("phi", 0.0, unit="", desc="axial flow velocity coefficient")
        self.add_outward("psi", 0.0, unit="", desc="load coefficient")

        self.add_outward("pr", 1.0, unit="", desc="total pressure ratio")
        self.add_outward("tr", 1.0, unit="", desc="total temperature ratio")
        self.add_outward("spec_flow", 1.0, desc="inlet specific flow")

        # off design
        self.add_outward(
            "eps_psi",
            0.0,
            unit="",
            desc="difference between psi from caracteristics and from energy",
        )
        self.add_equation("eps_psi == 0")

        # design methods
        self.add_inward("design_utip", 400.0, unit="m/s", desc="tip speed at design point")
        self.add_inward("design_pr", 5.0, unit="", desc="pressure ratio at design point")

        self.add_design_method("sizing").add_equation("utip == design_utip").add_equation(
            "pr == design_pr"
        ).add_equation("spec_flow == 200.")

        # calibration methods
        self.add_design_method("calib").add_unknown("design_utip").add_unknown(
            "design_pr"
        ).add_equation("utip == design_utip").add_equation("pr == design_pr").add_unknown("phiP")

    def compute(self):
        # fl_out computed from fl_in, enthalpy and mass conservation
        self.fl_out.W = self.fl_in.W

        delta_h = self.shaft_in.power / self.fl_in.W
        h = self.gas.h(self.fl_in.Tt) + delta_h
        self.fl_out.Tt = self.gas.t_from_h(h)

        self.tr = self.fl_out.Tt / self.fl_in.Tt
        self.pr = self.gas.pr(self.fl_in.Tt, self.fl_out.Tt, self.eff_poly)
        self.fl_out.pt = self.fl_in.pt * self.pr

        # axial flow coefficient
        self.utip = self.shaft_in.N * np.pi / 30.0 * self.tip_out_r
        rho = self.gas.density(self.fl_in.pt, self.fl_in.Tt)
        vm = self.fl_in.W / (rho * self.inlet_area)
        self.phi = vm / self.utip

        self.spec_flow = (
            self.fl_in.W
            * sqrt(self.fl_in.Tt / 288.15)
            / (self.fl_in.pt / 101325.0)
            / self.inlet_area
        )

        # load coefficient
        self.psi = self.tip_out_r / self.tip_in_r * (1 - self.phi / self.phiP)
        self.eps_psi = delta_h / (self.stage_count * self.utip**2) - self.psi
