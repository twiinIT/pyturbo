from typing import Collection

import numpy as np
from cosapp.systems import System

from pyturbo.ports import ShaftPort


class Shaft(System):
    """
    A simple shaft model.

    It forwards the power received at input(s) to output(s) with a given
    transmission efficiency.
    If multiple shaft outputs are created, the power fraction is automatically
    created using the same sequence as the model `output_shafts` argument.

    Note: a power extraction can be simply added using an output shaft port.
    """

    def setup(
        self,
        input_shafts: Collection[str] = ("sh_in",),
        output_shafts: Collection[str] = ("sh_out",),
    ):
        # inputs/outputs
        for p in input_shafts:
            self.add_input(ShaftPort, p)

        for p in output_shafts:
            self.add_output(ShaftPort, p)

        outputs_count = len(output_shafts)
        has_many_outputs = outputs_count > 1
        self.add_property("has_many_outputs", has_many_outputs)

        self.add_inward("eff", 0.995, desc="transmission efficiency")
        self.add_inward("fraction_scalar", 1.0, unit="", desc="scalar on all fraction")
        self.add_inward("power_fractions", np.ones(len(output_shafts)) / outputs_count)
        self.add_outward("total_input_power", 1.0, unit="W")
        self.add_outward("total_output_power", 1.0, unit="W")

        # off-design equations/unknowns
        if has_many_outputs:
            self.add_unknown("fraction_scalar").add_equation(
                "total_input_power == total_output_power"
            )

    def compute(self):
        shaft_in_ports = [p for p in self.inputs.values() if type(p) == ShaftPort]
        shaft_out_ports = [p for p in self.outputs.values() if type(p) == ShaftPort]

        # this is user responsability to add equations/unknowns to ensure consistency
        mean_input_N = np.mean([p.N for p in shaft_in_ports])
        self.total_input_power = np.sum([p.power for p in shaft_in_ports])

        shaft_out_powers = (
            np.sum([p.power for p in shaft_in_ports])
            * self.power_fractions
            * self.fraction_scalar
            * self.eff
        )
        self.total_output_power = np.sum(shaft_out_powers)

        for i, p in enumerate(shaft_out_ports):
            p.N = mean_input_N
            p.power = shaft_out_powers[i]
