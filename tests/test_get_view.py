# Copyright (C) 2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems import Compressor, Inlet, Nacelle, Nozzle, Turbine


class TestGetView:
    """Define tests for get_view."""

    def test_get_view_nozzle(self):
        sys = Nozzle("sys")
        nozzle_view = sys.occ_view
        assert nozzle_view.get_value()

    def test_get_view_compressor(self):
        sys = Compressor("sys")
        compressor_view = sys.occ_view
        assert compressor_view.get_value()

    def test_get_view_turbine(self):
        sys = Turbine("sys")
        turbine_view = sys.occ_view
        assert turbine_view.get_value()

    def test_get_view_inlet(self):
        sys = Inlet("sys")
        inlet_view = sys.occ_view
        assert inlet_view.get_value()

    def test_get_view_nacelle(self):
        sys = Nacelle("sys")
        nacelle_view = sys.occ_view
        assert nacelle_view.get_value()
