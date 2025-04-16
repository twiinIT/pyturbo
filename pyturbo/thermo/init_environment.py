# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import ambiance

from cosapp.base import System
from pyturbo.thermo import IdealDryAir


def init_environment(sys: System, alt : float = 0.0, mach : float = 0.0, dtamb : float = 0.0):
    """Init fluid data with mission values."""
    
    gas = IdealDryAir()
    atm = ambiance.Atmosphere(alt)
    pamb = atm.pressure[0]
    tamb = atm.temperature[0] + dtamb

    sys.pamb = pamb
    sys.fl_in.Tt = gas.total_t(tamb, mach)
    sys.fl_in.Pt = gas.total_p(pamb, tamb, sys.fl_in.Tt)

    return sys
