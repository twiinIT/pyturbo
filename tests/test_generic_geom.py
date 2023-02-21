# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class TestGenericSimpleGeom:
    """Define tests for the generic simple geometry."""

    def test_system_setup(self):
        # default constructor
        sys = GenericSimpleGeom("sys")

        inputs = ["kp"]
        outwards = []

        for p in inputs:
            assert p in sys.inputs
        for v in outwards:
            assert v in sys.outwards
