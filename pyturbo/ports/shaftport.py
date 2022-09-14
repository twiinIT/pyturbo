# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.ports import Port


class ShaftPort(Port):
    """A mechanical shaft port.

    Variables
    ---------
    power[W]: float, default=1e6
        shaft mechanical power
    N[rpm]: float, default=5000.0
        shaft rotationnal speed
    """

    def setup(self):
        self.add_variable("power", 1e6, unit="W", desc="mechanical power")
        self.add_variable("N", 5000.0, unit="rpm", desc="rotational speed")
