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
    print(f"\nSystem: {cls.__name__} | Data: {data}")

    sys = cls("sys")
    load_from_json(sys, data)

    nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))

    if "off_design_standalone" in sys.design_methods:
        nls.extend(sys.design_methods["off_design_standalone"])

    sys.run_drivers()

    print("Problem: ", nls.problem)
    assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6


def test_run_design_method(cls_and_method_and_data):
    """Test a single design method."""
    cls, method, data = cls_and_method_and_data
    print(f"\nSystem: {cls.__name__} | Method: {method} | Data: {data}")

    sys = cls("sys")
    load_from_json(sys, data)

    nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))
    nls.extend(sys.design_methods[method])

    try:
        sys.run_drivers()
        print("Problem: ", nls.problem)
        assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6
    except ArithmeticError as e:
        if "Nonlinear problem nls error" in str(e):
            pytest.xfail(f"ArithmeticError: {e}")
        else:
            raise ArithmeticError(e)
