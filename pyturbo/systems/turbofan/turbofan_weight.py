# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System


class TurbofanWeight(System):
    """A simple weight model.

    Weight is evaluated from diameter and length
    coef are computed from CFM family value

    weight_EIS = weight_ref * (
        fan_diameter/fan_diameter_ref)**c1 *
        (length/length_ref)**c2 *
        (EIS-EIS_ref)**c3

    Inputs
    ------
    c1, c2, c3[-]: float, default= -1.1, 4.3, 0.95
        constant coefficient

    weight_ref[m]: float, default=2370.0

    fan_diameter_ref[m]: float, default=1.0
    length_ref[m]: float, default=3.451
    EIS_ref[year]: float, default=1997

    fan_diameter[m]: float, default=1.0
        fan diameter
    length[m]: float, default=1.0
        engine length
    EIS[year]: float, default=2022
        Entry into service

    Outputs
    -------
    weight[kg]: float
        weight
    """

    def setup(self):
        # data
        self.add_inward("param", [1900.0, 0.5, 0.01, 1.006])

        # inward / outward
        self.add_inward("fan_diameter", 1.0, unit="m", desc="fan diameter")
        self.add_inward("length", 1.0, unit="m", desc="length")
        self.add_inward("eis", 2022, unit="", desc="Entry into service")

        self.add_outward("weight", 0.0, unit="kg")

    def compute(self):
        param = self.param
        self.weight = (
            param[0]
            * self.fan_diameter ** param[1]
            * self.length ** param[2]
            * param[3] ** (self.eis - 2000)
        )

        """Param are estimated to minimize error on:

                     ['weight', 'diameter', 'length', 'eis'])
        ['LEAP1A'] = [2990., 1.98, 3.328, 2015]
        ['LEAP1B'] = [2780., 1.76, 3.147, 2016]
        ['CFM56-5A'] = [2331., 1.734, 2.422, 1987]
        ['CFM56-7B'] = [2386., 1.549, 2.508, 1997]
        ['V2500'] = [2404., 1.682, 3.201, 1993]
        """
