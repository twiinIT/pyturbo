from math import sqrt
import numpy as np

from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class TurbofanWeight(System):
    """A simple weight model.

    Weight is evaluated from diameter and length
    coef are computed from CFM family value
    """

    def setup(self):
        # coef - evaluated from CFM family
        self.add_inward('c1', -1.1)
        self.add_inward('c2', 4.3)
        self.add_inward('c3', - 0.05)

        # reference
        self.add_inward('fan_diameter_ref', 1.549, unit='m', desc='CFM56-7 fan diameter')
        self.add_inward('length_ref', 3.461, unit='m', desc='CFM56-7 length')
        self.add_inward('ipps_weight_ref', 1., unit='kg', desc='CFM56-7 ipps weight')
        self.add_inward('EIS_ref', 1997., unit='', desc='CFM56-7 eentry into service year')

        # inward / outward
        self.add_inward('fan_diameter', 1., unit='m', desc='fan diameter')
        self.add_inward('length', 1., unit='m', desc='length')
        self.add_inward('EIS', 2022, unit='', desc='Entry into service')

        self.add_outward('ipps_weight', 1., unit='kg')

    def compute(self):
        
        self.ipps_weight = \
            self.ipps_weight_ref * (self.fan_diameter / self.fan_diameter_ref) ** self.c1 \
                * (self.length / self.length_ref) ** self.c2 \
                    * max([abs(self.EIS - self.EIS_ref), 1.]) ** (self.EIS_ref - self.EIS)
