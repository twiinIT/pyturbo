# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.atmosphere import Atmosphere
from pyturbo.systems.turbofan import Turbofan


class TurbofanWithAtm(System):
    """Turbofan assembly system used in atmosphere.

    Sub-systems
    -----------
    atm: Atmosphere
        simplified atmosphere from altitude, Mach and delta ambient temperature
    tf: Turbofan
        turbofan
    """

    def setup(self):
        self.add_child(Atmosphere("atm"), pulling=["altitude", "mach", "dtamb"])
        self.add_child(Turbofan("tf"), pulling=["fuel_W", "thrust"])

        self.connect(self.atm.outwards, self.tf.fl_in, ["Pt", "Tt"])
        self.connect(self.atm.outwards, self.tf.inwards, ["pamb"])
