# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import importlib.util
import inspect
import os
import sys

from cosapp.base import System

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SYSTEMS_DIR = os.path.join(os.path.dirname(__file__), "pyturbo", "systems")
BASE_PATH = os.path.abspath(SYSTEMS_DIR)


def pytest_addoption(parser):
    """Manage option in pytest."""
    parser.addoption(
        "--cosapp_system",
        action="store",
        default=None,
        help="Run tests only for classes with this exact name",
    )


def find_cosapp_classes(base_path):
    """Find and return all CoSApp Systems in base_path."""
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
                    if (
                        issubclass(obj, System)
                        and obj is not System
                        and obj.__module__ == module_name  # ✅ classe définie dans ce fichier
                    ):
                        cls_list.append((obj, module_path))

    seen = set()
    unique = []
    for cls, path in cls_list:
        identity = (cls.__name__, os.path.normpath(path))
        if identity not in seen:
            seen.add(identity)
            unique.append((cls, path))
    return unique


def get_all_data_files(class_and_path_list):
    """Get all .json data files in the 'data' folder adjacent to each class file."""
    pairs = []

    for cls, module_path in class_and_path_list:
        try:
            class_dir = os.path.dirname(module_path)
            data_dir = os.path.join(class_dir, "data")

            if os.path.isdir(data_dir):
                json_files = [
                    os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")
                ]
                if json_files:
                    for f in json_files:
                        pairs.append((cls, f))
                    continue

            pairs.append((cls, None))

        except Exception as e:
            print(f"[ERROR] Failed to get data files for {cls.__name__}: {e}")
            pairs.append((cls, None))

    return pairs


def get_all_design_methods_and_data(class_and_path_list):
    """Get all design methods + .json data files for each class."""
    pairs = []

    for cls, module_path in class_and_path_list:
        try:
            instance = cls("sys")
            class_dir = os.path.dirname(module_path)
            data_dir = os.path.join(class_dir, "data")

            json_files = []
            if os.path.isdir(data_dir):
                json_files = [
                    os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")
                ]

            for method in instance.design_methods:
                if method == "off_design_stand_alone":
                    continue

                if json_files:
                    for f in json_files:
                        pairs.append((cls, method, f))
                else:
                    pairs.append((cls, method, None))

        except Exception as e:
            print(f"[ERROR] Failed to get design methods/data for {cls.__name__}: {e}")
            continue

    return pairs


def pytest_generate_tests(metafunc):
    """Generate tests for CoSApp Systems and their design methods."""
    class_and_path_list = find_cosapp_classes(BASE_PATH)

    class_name_filter = metafunc.config.getoption("cosapp_system")
    if class_name_filter:
        class_and_path_list = [
            (cls, path) for cls, path in class_and_path_list if cls.__name__ == class_name_filter
        ]

    if "cls" in metafunc.fixturenames:
        metafunc.parametrize("cls", [cls for cls, _ in class_and_path_list], scope="function")

    if "cls_and_data" in metafunc.fixturenames:
        metafunc.parametrize(
            "cls_and_data", get_all_data_files(class_and_path_list), scope="function"
        )

    if "cls_and_method_and_data" in metafunc.fixturenames:
        metafunc.parametrize(
            "cls_and_method_and_data",
            get_all_design_methods_and_data(class_and_path_list),
            scope="function",
        )
