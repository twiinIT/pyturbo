# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.base import System

from pyturbo.ports import View, ViewPort


class GenericSystemView(System):
    """Visual representation of a system.

    Parameter
    ---------
    children_name: list[str]
        children name to merge in the view

    Inputs
    -------
    f"child_name"_view : ViewPort
        child view

    Outputs
    -------
    occ_view : ViewPort
        system view
    """

    def setup(self, children_name=None):
        self.add_property("children_name", children_name or [])

        # inputs/outputs
        for child_name in self.children_name:
            self.add_input(ViewPort, f"{child_name}_view")

        self.add_output(ViewPort, "occ_view")

    def compute(self):

        view = View()

        for child_name in self.children_name:
            view = view.merge(self[f"{child_name}_view"])

        self.occ_view.set_value(view)
