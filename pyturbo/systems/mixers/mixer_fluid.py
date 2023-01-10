import numpy as np
from cosapp.systems import System

from pyturbo.ports.fluidport import FluidPort


class MixerFluid(System):
    """Mixer aero model.

    A mixer and splitter of fluid that forwards the mass fluid received at input(s) to output(s).
    Their must have at least an input and an output.

    Parameters
    ----------
    input_fluid: list[str]
        list of the input fluid names. If name is 'fl_in', fluid will be self.fl_in
        default is ("fl_in")
    output_fluid: list[str]
        list of output fluid names
        default is ("fl_out")

    Inputs
    ------
    fl_in: FluidPort
        inlet fluid (for each name in input_fluid)

    fluid_fraction: numpy array
        size is len(output_shaft) - 1
        proportion of fluid that goes to flow_out in the order of output_fluid list

    Outputs
    -------
    fl_out: FluidPort
        exit fluid (for each name in output_fluid)

    Pt[Pa]: float, default=1.0
        mean fluid total pressure
        all flow_in total pressure should be the same
    W[kg/s]: float, default=1.0
        mass fluid in kg/s
        total flow_in mass fluid and flow_out mass fluid are equal
    Tt[K]: float, default=1.0
        mean fluid total temperature in K

    Design methods
    ------------------
    off design:
        parameters - fluid_fraction
        equations - input_fluid total pressure are equal to mean total pressure

    Good practice
    -------------
    1
        consider at last the bigest fluid mass flow in output_fluids list
    2
        If fluid out have very different mass flow, it should be good to initiate fluid_fraction
        with a good order of magnitude
    """

    def setup(
        self,
        input_fluids: list[str] = ("fl_in",),
        output_fluids: list[str] = ("fl_out",),
    ):

        self.add_inward("n_in", len(input_fluids))
        self.add_inward("n_out", len(output_fluids))

        # inputs
        for p in input_fluids:
            self.add_input(FluidPort, p)

        # outputs
        for p in output_fluids:
            self.add_output(FluidPort, p)

        # inwards/outwards
        if self.n_out > 1:
            self.add_inward("fluid_fractions", np.ones(self.n_out - 1) / self.n_out)

        self.add_outward("W", 1.0, unit="kg/s", desc="mean fluid total pressure")
        self.add_outward("Pt", 1.0, unit="pa", desc="mass fluid")
        self.add_outward("Tt", 1.0, unit="K", desc="mean fluid total temperature")

        # off design
        for i, p in enumerate(input_fluids):
            if i != 0:
                self.add_equation(f"Pt == {p}.Pt")

        if self.n_out > 1:
            self.add_unknown("fluid_fractions", max_rel_step=0.1)

    def compute(self):

        # input flows
        fluid_in_ports = [p for p in self.inputs.values() if type(p) == FluidPort]

        self.W = np.sum([p.W for p in fluid_in_ports])
        self.Pt = np.mean([p.Pt for p in fluid_in_ports])
        self.Tt = np.mean([p.W * p.Tt for p in fluid_in_ports]) / self.W

        # output flows
        fluid_out_ports = [p for p in self.outputs.values() if type(p) == FluidPort]

        W = 0.0
        for i, p in enumerate(fluid_out_ports):
            p.Pt = self.Pt
            p.Tt = self.Tt
            if i < self.n_out - 1:
                p.W = self.W * self.fluid_fractions[i]
                W += p.W
            else:
                p.W = self.W - W
