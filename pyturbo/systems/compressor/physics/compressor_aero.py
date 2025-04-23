# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from math import sqrt

import numpy as np
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo import IdealDryAir


class CompressorAero(System):
    """A compressor aero simple model.

    The methodology is consistent with https://oatao.univ-toulouse.fr/17882
    Binder, Nicolas Aéro-thermodynamique des Turbomachines en Fonctionnement
    Hors-Adaptation. (2016) [HDR]
    - exit flow is computed from inlet one
    - polytropic efficiency is constant
    - aerodynamic load and axial flow velocity are linked using a linear modeling

    Parameters
    ----------
    FluidLaw: Class, default=IdealDryAir
        Class providing gas characteristics

    Inputs
    ------
    fl_in: FluidPort
        fluid going into the compressor
    sh_in: ShaftPort
        shaft driving the compressor

    eff_poly[-]: float, default=0.9
        polytropic efficiency
    phiP[-]: float, default=0.4
        axial flow velocity coefficient for no power consumption of the compressor

    stage_count[-]: int, default=1
        number of compressor stages
    tip_in_r[m]: float, default=1.0
        inlet tip radius
    tip_out_r[m]: float, default=1.0
        exit tip radius
    inlet_area[m**2]: float, default=1.0
        inlet area

    Outputs
    -------
    fl_out: FluidPort
        fluid leaving the compressor

    utip[m/s]: float, default=0.0
        blade tip speed at inlet
    phi[-]: float, default=0.0
        axial flow velocity coefficient
    psi[-]: float, default=0.0
        load coefficient
    pr[-]: float, default=1.0
        total to total pressure ratio
    tr[-]: float, default=1.0
        total to total temperature ratio
    spec_flow[kg/s]: float, default=1.0
        inlet specific flow

    Design methods
    --------------
    off design:
        psi computed from enthalpy conservation equal psi computed from characteristics

    Good practice
    -------------
    1:
        initiate sh_in.power with the good order of magnitude of shaft power
    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_inward("gas", FluidLaw())

        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_input(ShaftPort, "sh_in")

        self.add_output(FluidPort, "fl_out")

        # inwards
        # geom characteristics
        self.add_inward("stage_count", 1, unit="", desc="number of stages")
        self.add_inward("tip_in_r", 1.0, unit="m", desc="inlet tip radius")
        self.add_inward("tip_out_r", 1.0, unit="m", desc="exit tip radius")
        self.add_inward("inlet_area", 2.0, unit="m**2", desc="inlet area")

        # aero characteristics
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward(
            "phiP",
            0.4,
            desc="axial flow velocity coefficient for zero compressor consumption",
        )
        self.add_inward("xnd", 10000.0, unit="rpm", desc="Rotational speed at design point")

        # outwards
        # functional characteristics
        self.add_outward("utip", 400.0, unit="m/s", desc="tip speed")
        self.add_outward("phi", 0.5, unit="", desc="axial flow velocity coefficient")
        self.add_outward("psi", 0.2, unit="", desc="load coefficient per stage")

        self.add_outward("pr", 1.0, unit="", desc="total to total pressure ratio")
        self.add_outward("tr", 1.0, unit="", desc="total to total temperature ratio")
        self.add_outward("spec_flow", 1.0, unit="kg/s/m**2", desc="inlet specific flow")

        self.add_outward("pcnr", 95.0, unit="", desc="Percentage of rotational speed vs reference")

        # off design
        self.add_outward(
            "eps_psi",
            0.0,
            unit="",
            desc="difference between psi from caracteristics and from enthalpy",
        )
        self.add_equation("eps_psi == 0")
        self.add_unknown("sh_in.N")

        # design methods
        # generic
        scaling = self.add_design_method("scaling")
        scaling.add_unknown("xnd")
        scaling.add_target("pcnr")

        # scaling booster
        scaling_booster = self.add_design_method("scaling_booster")
        scaling_booster.extend(scaling)
        scaling_booster.add_unknown("phiP", max_rel_step=0.5)

        scaling_booster.add_target("phi")
        scaling_booster.add_target("psi")

        # scaling hpc
        scaling_hpc = self.add_design_method("scaling_hpc")
        scaling_hpc.extend(scaling)

        scaling_hpc.add_unknown("phiP")
        scaling_hpc.add_target("phi")
        scaling_hpc.add_target("utip")
        scaling_hpc.add_target("psi")

        # init
        self.sh_in.power = 1e6

    def compute(self):
        # fl_out computed from fl_in, enthalpy and mass conservation
        self.fl_out.W = self.fl_in.W

        delta_h = self.sh_in.power / self.fl_in.W
        h = self.gas.h(self.fl_in.Tt) + delta_h
        self.fl_out.Tt = self.gas.t_f_h(h, tol=1e-6)

        self.tr = self.fl_out.Tt / self.fl_in.Tt
        self.pr = self.gas.pr(self.fl_in.Tt, self.fl_out.Tt, self.eff_poly)
        self.fl_out.Pt = self.fl_in.Pt * self.pr

        # axial flow coefficient
        self.utip = self.sh_in.N * np.pi / 30.0 * self.tip_out_r
        rho = self.gas.density(self.fl_in.Pt, self.fl_in.Tt)
        vm = self.fl_in.W / (rho * self.inlet_area)
        self.phi = vm / self.utip

        # load coefficient
        self.psi = self.tip_out_r / self.tip_in_r * (1 - self.phi / self.phiP)
        self.eps_psi = delta_h / (self.stage_count * self.utip**2) - self.psi

        Wc = self.fl_in.W * sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.Pt / 101325.0)

        self.spec_flow = Wc / self.inlet_area
        self.pcnr = self.sh_in.N / self.xnd * 100.0
