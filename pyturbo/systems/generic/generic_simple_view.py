# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports import KeypointsPort, View, ViewPort


class GenericSimpleView(System):
    """Class with visual representation of a generic simple view.

    Inputs
    ------
    kp : KeypointsPort
        Geometrical envelop.

    Outputs
    -------
    occ_view : ViewPort
        The visualisation.
    """

    def setup(self, shell_view=False):
        self.add_inward("shell_view", shell_view)

        # inputs/outputs
        self.add_input(KeypointsPort, "kp")
        self.add_output(ViewPort, "occ_view")

        # inwards
        self.add_inward("n", 1, unit="", desc="stage count")

    def compute(self):
        shell = {
            "shape": self.kp.view(self.shell_view),
            "face_color": "white",
            "opacity": 0.9,
        }

        view = View({"shell": shell})

        self.occ_view.set_value(view)
