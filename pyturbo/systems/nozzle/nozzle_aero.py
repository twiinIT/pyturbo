from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class NozzleAero(System):
    """
    A simple nozzle aerodynamic model.

    It computes the gross thrust from the flow and ambient static
    pressure assuming a choked throat=exit area (convergent nozzle).

    thrust = W * v + (ps - pamb) * area

    Parameters
    ----------
    gas : IdealDryAir
        class provided the characteristics of gas.
    pamb : float
        ambiant static pressure in pa

    Inputs
    ------
    fl_in : FluidPort

    Outputs
    -------
    fl_out : FluidPort

    Inwards from geom
    -----------------
    area : float
        throat area in m**2

    Outwards
    --------
    ps: float
        static pressure at throat in pa
    mach : float
        fluid mach number at throat
    v : float
        fluid speed at throat in m/s
    thrust : float
        thrust in N computed at throat. If drag < 0, aspiration contribute to thrust

    Off design
    ----------
    fluid mass flow imposed by chocked throat

    Good practice
    -------------
    1 - fl_in.pt must be bigger than pamb.
    """

    def setup(self):
        # parameter
        self.add_inward("subsonic", True)

        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards
        self.add_inward("gas", IdealDryAir())
        self.add_inward("area", 1.0, unit="m**2", desc="choked/exit area")
        self.add_inward("pamb", 101325.0, unit="Pa", desc="ambient static pressure")

        # outwards
        self.add_outward("ps", 0.0, unit="pa", desc="static pressure at throat")
        self.add_outward("mach", 0.0, unit="", desc="mach at throat")
        self.add_outward("v", 0.0, unit="m/s", desc="fluid flow speed at throat")
        self.add_outward("thrust", unit="N")

        # off design
        self.add_equation("fl_in.W == fl_out.W")

        # init
        self.fl_in.W = 100.0

    def compute(self):
        # outputs
        self.fl_out.pt = self.fl_in.pt
        self.fl_out.Tt = self.fl_in.Tt

        # assumes convergent nozzle (throat at exit)
        self.mach = self.gas.mach_ptpstt(self.fl_in.pt, self.pamb, self.fl_in.Tt)

        if self.mach > 1.0:
            self.mach = 1.0

        ts = self.gas.static_t(self.fl_in.Tt, self.mach)
        self.ps = self.gas.static_p(self.fl_in.pt, self.fl_in.Tt, self.mach)
        rho = self.gas.density(self.ps, ts)
        self.v = self.gas.c(ts) * self.mach
        self.fl_out.W = rho * self.v * self.area

        self.thrust = self.fl_out.W * self.v + (self.ps - self.pamb) * self.area
