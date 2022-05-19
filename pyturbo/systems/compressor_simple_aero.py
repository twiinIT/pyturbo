from re import U
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
        self.add_inward("inlet_tip_radius", 1.0, unit="m", desc="inlet tip radius")
        self.add_inward("exit_tip_radius", 1.0, unit="m", desc="exit tip radius")
        self.add_inward("inlet_section", 1.0, unit="m**2", desc="inlet section")

        # aero characteristics
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward("phiP", 0.4, desc="")

        # functional characteristics
        self.add_outward("utip", 0.0, unit="m/s", desc="tip speed")
        self.add_outward("phi", 0.0, unit="", desc="axial flow velocity coefficient")
        self.add_outward("psi", 0.0, unit="", desc="load coefficient")

        self.add_outward("pr", 1.0, desc="total pressure ratio")
        self.add_outward("tr", 1.0, desc="total temperature ratio")

        # off design
        self.add_outward(
            "eps_psi",
            0.0,
            unit="",
            desc="difference between psi from caracteristics and from energy",
        )
        self.add_equation("eps_psi == 0")

        # design methods
        self.add_inward("design_utip", unit="m/s", desc="tip speed at design point")
        self.add_inward("design_pr", 1.3, unit="", desc="pressure ratio at design point")

        self.add_design_method("sizing").add_equation("utip == design_utip").add_equation(
            "pr == design_pr"
        )
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
        self.utip = self.shaft_in.N * np.pi / 30.0 * self.exit_tip_radius
        rho = self.gas.density(self.fl_in.pt, self.fl_in.Tt)
        vm = self.fl_in.W / (rho * self.inlet_section)
        self.phi = vm / self.utip

        # load coefficient
        self.psi = self.exit_tip_radius / self.inlet_tip_radius * (1 - self.phi / self.phiP)
        self.eps_psi = delta_h / (self.stage_count * self.utip**2) - self.psi
