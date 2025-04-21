# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import importlib.util
import inspect
import os

from cosapp.base import System

SYSTEMS_DIR = os.path.join(os.path.dirname(__file__), "pyturbo", "systems")
BASE_PATH = os.path.abspath(SYSTEMS_DIR)


def find_cosapp_classes(base_path):
    """Find all CoSApp Systems in systems folder."""
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
                    if issubclass(obj, System) and obj is not System:
                        cls_list.append(obj)

    seen = set()
    unique = []
    for cls in cls_list:
        if cls.__name__ not in seen:
            seen.add(cls.__name__)
            unique.append(cls)
    return unique


def get_all_design_methods(classes):
    """Get all design methods in classes, but off_design method."""
    pairs = []
    for cls in classes:
        try:
            instance = cls("sys")
            for name in instance.design_methods:
                if name != "off_design":
                    pairs.append((cls, name))
        except Exception:
            pass  # skip classes that can't be instantiated
    return pairs


def pytest_addoption(parser):
    """Manage option in pytest."""
    parser.addoption(
        "--cosapp_system",
        action="store",
        default=None,
        help="Run tests only for classes with this exact name",
    )


def pytest_generate_tests(metafunc):
    """Generate tests for CoSApp Systems and their design methods."""
    class_name_filter = metafunc.config.getoption("cosapp_system")
    all_classes = find_cosapp_classes(BASE_PATH)

    if class_name_filter:
        all_classes = [cls for cls in all_classes if cls.__name__ == class_name_filter]

    if "cls" in metafunc.fixturenames:
        metafunc.parametrize("cls", all_classes, scope="module")

    if "cls_and_method" in metafunc.fixturenames:
        metafunc.parametrize(
            "cls_and_method", get_all_design_methods(all_classes), scope="function"
        )
