# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import ShaftPort


class MixerShaft(System):
    """Shaft splitter and mixer model.

    A mixer and splitter of shafts that forwards the power received at input(s) to output(s).
    Their must have at least an input and an output.

    Parameters
    ----------
    input_shafts: list[str]
        list of the input shaft names. If name is 'sh_in', shaft will be self.sh_in
        default is ("sh_in")
    output_shafts: list[str]
        list of output shaft names
        default is ("sh_out")
    n_in: int
        number ou input shafts
    n_out: int
        number ou output shafts

    Inputs
    ------
    power_fraction: numpy array
        size is len(output_shaft) - 1
        proportion of power that goes to shaft_out in the order of output_shaft list

    Outputs
    -------
    N[rpm]: float, default=1.0
        mean shaft speed rotation
        all sh_in power should have the same speed rotation
    power[W]: float, default=1.0
        shaft power.
        total sh_in power and sh_out power are equal

    Design methods
    --------------
    off design:
        parameter: power_fraction
        equations: input_shaft speed rotation are equal to mean speed rotation

    Good practice
    -------------
    1:
        consider at least the most powerfull shaft in output_shafts list
    2:
        If shaft out have very different power, it should be good to initiate power_fraction with
        a good order of magnitude

    """

    def setup(
        self,
        input_shafts: list[str] = ("sh_in",),
        output_shafts: list[str] = ("sh_out",),
    ):

        self.add_inward("n_in", len(input_shafts))
        self.add_inward("n_out", len(output_shafts))

        # inputs
        for p in input_shafts:
            self.add_input(ShaftPort, p)

        # outputs
        for p in output_shafts:
            self.add_output(ShaftPort, p)

        # inwards/outwards
        if self.n_out > 1:
            self.add_inward("power_fractions", np.ones(self.n_out - 1) / self.n_out)

        self.add_outward("power", 1.0, unit="W")
        self.add_outward("N", 1.0, unit="rpm")

        # off design
        for i, p in enumerate(input_shafts):
            if i != 0:
                self.add_equation(f"N == {p}.N")

        if self.n_out > 1:
            self.add_unknown("power_fractions", max_rel_step=0.1)

    def compute(self):  # noqa: TWI002

        # input shafts
        shaft_in_ports = [p for p in self.inputs.values() if isinstance(p, ShaftPort)]

        self.power = np.sum([p.power for p in shaft_in_ports])
        self.N = np.mean([p.N for p in shaft_in_ports])

        # output shafts
        shaft_out_ports = [p for p in self.outputs.values() if isinstance(p, ShaftPort)]

        power = 0.0
        for i, p in enumerate(shaft_out_ports):
            p.N = self.N
            if i < self.n_out - 1:
                p.power = self.power * self.power_fractions[i]
                power += p.power
            else:
                p.power = self.power - power
