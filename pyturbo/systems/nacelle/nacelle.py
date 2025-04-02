# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.nacelle.nacelle_view import NacelleView


class Nacelle(System):
    """Nacelle simple assembly model.

    Sub-systems
    -----------
    view: NacelleView
        compute visualisation

    Inputs
    ------
    kp: KeypointsPort
        nacelle geometrical envelop
    """

    def setup(self):  # noqa: TWI009
        # children
        self.add_child(NacelleView("view"), pulling=["occ_view", "kp"])
