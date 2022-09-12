# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System


class TurbofanWeight(System):
    """
    A simple weight model.

    Weight is evaluated from diameter and length
    coef are computed from CFM family value

    ipps_weight_EIS = ipps_weight_ref * (fan_diameter/fan_diameter_ref)**c1 * (length/length_ref)**c2 * (EIS-EIS_ref)**c3

    Inputs
    ------
    c1, c2, c3[-]: float
        constant coefficient
    
    ipps_weight_ref[m]: float
        CFM56-7 ipps weight

    fan_diameter_ref[m]: float
        CFM56-7 fan diameter
    length_ref[m]: float
        CFM56-7 length
    EIS_ref[year]: float
        CFM56-7 eentry into service year
    
    fan_diameter[m]: float
        fan diameter
    length[m]: float
        engine length
    EIS[year]: float
        Entry into service

    Outputs
    -------
    ipps_weight[kg]: float
        ipps weight
    """

    def setup(self):
        # coef - evaluated from CFM family
        self.add_inward("c1", -1.1)
        self.add_inward("c2", 4.3)
        self.add_inward("c3", 0.95)

        # reference
        self.add_inward("fan_diameter_ref", 1.549, unit="m", desc="CFM56-7 fan diameter")
        self.add_inward("length_ref", 3.461, unit="m", desc="CFM56-7 length")
        self.add_inward("ipps_weight_ref", 1.0, unit="kg", desc="CFM56-7 ipps weight")
        self.add_inward("EIS_ref", 1997.0, unit="", desc="CFM56-7 entry into service year")

        # inward / outward
        self.add_inward("fan_diameter", 1.0, unit="m", desc="fan diameter")
        self.add_inward("length", 1.0, unit="m", desc="length")
        self.add_inward("EIS", 2022, unit="", desc="Entry into service")

        self.add_outward("ipps_weight", 1.0, unit="kg")

    def compute(self):

        self.ipps_weight = (self.ipps_weight_ref
            * (self.fan_diameter / self.fan_diameter_ref) ** self.c1
            * (self.length / self.length_ref) ** self.c2
            * self.c3 ** (self.EIS - self.EIS_ref)
        )
