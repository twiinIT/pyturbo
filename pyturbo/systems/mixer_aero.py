import numpy as np

from cosapp.systems import System

from pyturbo.ports.fluidport import FluidPort


class MixerAero(System):
    """Mixer aero

    Mix n_in fluid ports in and split into n_out fluid port out
    ri (for i in 0 to n_out-1) is the mass flow ratio going in fluid port fli_out
    """

    def setup(self, n_in: int = 1, n_out: int = 1):
        self.add_property("n_in", n_in)
        self.add_property("n_out", n_out)

        # inputs / outputs
        for n in range(n_in):
            self.add_input(FluidPort, f"fl{n}_in")

        for n in range(n_out):
            self.add_output(FluidPort, f"fl{n}_out")

        # inwards / outwards
        for n in range(n_out):
            self.add_inward(f"r{n}", 1.0 / n_out)

        self.add_outward("pt", unit="Pa")
        self.add_outward("Tt", unit="K")
        self.add_outward("W", unit="kg/s")

        # solver
        # TODO: consider ps equilibrium
        for n in range(1, n_in):
            self.add_equation(f"fl{n}_in.pt == pt")

        for n in range(1, n_out):
            self.add_unknown(f"r{n}", lower_bound=0.0, upper_bound=1.0, max_rel_step=0.1)

    def compute(self):
        n_in = self.n_in
        n_out = self.n_out

        # input conditions
        W_tot = self.fl0_in.W
        ptW_tot = self.fl0_in.W * self.fl0_in.pt
        TtW_tot = self.fl0_in.W * self.fl0_in.Tt

        for n in range(1, n_in):
            fl = self[f"fl{n}_in"]
            W = fl.W

            W_tot += W
            ptW_tot += W * fl.pt
            TtW_tot += W * fl.Tt

        self.W = W_tot
        self.pt = ptW_tot / W_tot
        self.Tt = TtW_tot / W_tot  # TODO : enthalpie

        # output conditions
        self.r0 = 1.0
        for n in range(1, n_out):
            self.r0 -= self[f"r{n}"]

        for n in range(n_out):
            self[f"fl{n}_out"].W = W_tot * self[f"r{n}"]
            self[f"fl{n}_out"].pt = self.pt
            self[f"fl{n}_out"].Tt = self.Tt
