# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems.generic import GenericSimpleView


class TestGenericSimpleView:
    """Define tests for the generic simple view."""

    def test_view(self):
        sys = GenericSimpleView("sys")
        sys.run_once()
        sys.occ_view.get_value().render()

        assert True
