from cosapp.base import System
from pyturbo.ports import FluidPort


class SimpleNozzle(System):
    def setup(self):

        # Define the ports
        self.add_input(FluidPort, "F_in")
        self.add_output(FluidPort, "F_out")

        # Define inwards
        self.add_inward("S_inlet", value=3.14159)
        self.add_inward("S_outlet", value=2.0)

        self.add_inward("P_atm", value=100000)
        self.add_inward("gamma", value=1.4)
        self.add_inward("R", value=287)

        # Define outwards
        self.add_outward("rho_inlet")
        self.add_outward("rho_outlet")
        self.add_outward("speed_outlet")
        self.add_outward("Thrust")
        self.add_outward("Mach_in")
        self.add_outward("Mach_out")

    def compute(self):

        self.Mach_in = (
            (2 / (self.gamma - 1))
            * ((self.F_in.Pt / self.P_atm) ** ((self.gamma - 1) / self.gamma) - 1)
        ) ** 0.5

        self.F_out.Tt = self.F_in.Tt / (1 + (((self.gamma - 1) / 2) * self.Mach_in))

        # self.F_out.Tt = (
        #     self.F_in.Tt / (1 + (((self.gamma - 1) / 2) * ((self.gamma**2) * (self.R**2))))
        # ) ** (1 / 3)

        self.Mach_out = self.gamma * self.R * self.F_out.Tt

        self.F_out.Pt = self.F_in.Pt / (1 + ((self.gamma - 1) / 2) * self.Mach_out**2) ** (
            1 / (self.gamma - 1)
        )

        self.rho_inlet = self.F_in.Pt / (self.R * self.F_in.Tt)
        self.rho_outlet = self.rho_inlet / (1 + ((self.gamma - 1) / 2) * self.Mach_out**2) ** (
            1 / (self.gamma - 1)
        )

        self.speed_outlet = self.Mach_out * (self.gamma * self.R * self.F_out.Tt) ** 0.5

        self.F_out.W = self.rho_outlet * self.S_outlet * self.speed_outlet

        self.Thrust = (
            self.F_out.W * self.speed_outlet + (self.F_out.Pt - self.P_atm) * self.S_outlet
        )
