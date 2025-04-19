# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

import os
import importlib.util
import inspect

import numpy as np

from cosapp.base import System
from cosapp.drivers import NonLinearSolver


directory_path = os.path.join(os.path.dirname(__file__), "..", "pyturbo", "systems")


def get_all_system_classes_from_directory(directory_path):
    cls_list = []

    base_path = os.path.abspath(directory_path)

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                module_path = os.path.join(root, file)

                relative_path = os.path.relpath(module_path, base_path)
                module_name = (
                    os.path.splitext(relative_path)[0]
                    .replace(os.path.sep, '.')
                )

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, System):
                        cls_list.append(obj)

    unique_cls_list = []
    seen = set()
    for cls in cls_list:
        if (name := cls.__name__) not in seen:
            seen.add(name)
            unique_cls_list.append(cls)

    return unique_cls_list


def pytest_generate_tests(metafunc):
    class_name_filter = metafunc.config.getoption("class_name")
    all_classes = get_all_system_classes_from_directory(directory_path)

    if class_name_filter:
        all_classes = [
            cls for cls in all_classes
            if cls.__name__ == class_name_filter
        ]

    metafunc.parametrize("cls", all_classes, scope="module")


cls_list = get_all_system_classes_from_directory(directory_path)


@pytest.fixture(params=cls_list)
def system(request):
    cls = request.param
    print(f"Creating system instance for: {cls.__name__}")
    return cls("sys")


def test_setup(cls):
    assert cls('sys') is not None


def test_run_once(cls):
    print(cls)
    cls('sys').run_once()


def test_run_design_methods(cls):
    for name in cls('sys').design_methods.keys():
        print(f"Design method: {name}")
        sys = cls("sys")
        nls = sys.add_driver(NonLinearSolver('nls', tol=1e-6))
        nls.extend(sys.design_methods[name])

        sys.run_drivers()
        assert np.linalg.norm(nls.problem.residue_vector()) < 1e-6