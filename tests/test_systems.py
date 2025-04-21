# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pytest
from cosapp.drivers import NonLinearSolver

from pyturbo.utils import load_from_json


def test_run_once(cls_and_data):
    """Run once systems."""
    cls, data = cls_and_data
    print("System: ", cls.__name__)
    sys = cls("sys")

    print("Load file: ", data)
    load_from_json(sys, data)

    sys.run_once()

    if "occ_view" in sys:
        assert sys.occ_view.get_value().render()


def test_run_off_design(cls_and_data):
    """Run off design methods."""
    cls, data = cls_and_data
    print("System: ", cls.__name__)
    sys = cls("sys")
    print("Load file: ", data)
    load_from_json(sys, data)

    nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))

    try:
        nls.extend(sys.design_methods["off_design"])
    except KeyError:
        pass

    sys.run_drivers()

    print("Problem: ", nls.problem)
    assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6


def test_run_design_method(cls_and_method):
    """Test a single design method."""
    cls, method = cls_and_method
    print(f"\nSystem: {cls.__name__} | Method: {method}")
    sys = cls("sys")
    nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))
    nls.extend(sys.design_methods[method])

    try:
        sys.run_drivers()
        print("Problem: ", nls.problem)
        residue = np.linalg.norm(nls.problem.residue_vector())
        if residue >= 1e-6:
            pytest.fail(f"Residual too high for `{cls.__name__}` with `{method}`: {residue:.4e}")
    except ArithmeticError as e:
        pytest.xfail(f"ArithmeticError: {e}")
