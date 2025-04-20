# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import importlib.util
import inspect
import os

import numpy as np
import pytest
from cosapp.base import System
from cosapp.drivers import NonLinearSolver

directory_path = os.path.join(os.path.dirname(__file__), "..", "pyturbo", "systems")
base_path = os.path.abspath(directory_path)


def pytest_generate_tests(metafunc):
    """Generate tests for recursive CoSApp Systems tests."""
    class_name_filter = metafunc.config.getoption("cosapp_system")
    cls_list = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file)

                relative_path = os.path.relpath(module_path, base_path)
                module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, ".")

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, System):
                        cls_list.append(obj)

    all_classes = []
    seen = set()
    for cls in cls_list:
        if (name := cls.__name__) not in seen:
            seen.add(name)
            all_classes.append(cls)

    if class_name_filter:
        all_classes = [cls for cls in all_classes if cls.__name__ == class_name_filter]

    metafunc.parametrize("cls", all_classes, scope="module")


def test_setup(cls):
    """Setup systems."""
    cls("sys")


def test_run_once(cls):
    """Run once systems."""
    cls("sys").run_once()


def test_run_off_design(cls):
    """Run off design methods."""
    sys = cls("sys")
    nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))

    try:
        nls.extend(sys.design_methods["off_design"])
    except KeyError:
        pass

    sys.run_drivers()

    print(nls.problem)
    assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6


@pytest.mark.skip
def test_run_design_methods(cls):
    """Run all design methods."""
    for name in cls("sys").design_methods.keys():
        print(f"Design method: {name}")
        sys = cls("sys")
        nls = sys.add_driver(NonLinearSolver("nls", tol=1e-6))
        nls.extend(sys.design_methods[name])

        sys.run_drivers()

        print(nls.problem)
        assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6
