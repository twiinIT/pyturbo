from typing import Collection

import numpy as np
from cosapp.systems import System

from pyturbo.ports import ShaftPort
from pyturbo.thermo.ideal_gas import IdealGas


class Shaft(System):
    """
    A simple shaft model.

    It forwards the power received at input(s) to output(s) with a given
    transmission efficiency.
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

        outputs_count = len(output_shafts)
        has_many_outputs = outputs_count > 1
        self.add_property("has_many_outputs", has_many_outputs)

        self.add_outward("total_input_power", 1.0, unit="W")
        self.add_outward("total_output_power", 1.0, unit="W")

        if has_many_outputs:
            self.add_inward("fraction_scalar", 1.0, unit="", desc="scalar on all fraction")
            self.add_unknown("fraction_scalar").add_equation(
                "total_input_power == total_output_power"
            )

        for i, p in enumerate(output_shafts):
            self.add_output(ShaftPort, p)
            self.add_inward(f"{p}_power_fraction", 1 / outputs_count)

        # additional inwards/outwards
        self.add_inward("eff", 0.995, desc="transmission efficiency")

    def compute(self):
        # this is user responsability to add equations/unknowns to ensure consistency
        mean_input_N = np.mean([p.N for p in self.inputs.values() if type(p) == ShaftPort])

        self.total_input_power = np.sum(
            [p.power for p in self.inputs.values() if type(p) == ShaftPort]
        )

        self.total_output_power = 0.0
        for p in [p for p in self.outputs.values() if type(p) == ShaftPort]:
            p.N = mean_input_N
            fraction = self[f"{p.name}_power_fraction"]
            if self.has_many_outputs:
                fraction *= self.fraction_scalar
            p.power = self.total_input_power * fraction
            self.total_output_power += p.power
