# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

"""The setup script."""

from setuptools import find_packages, setup

with open("requirements.txt") as requirements_file:
    requirements = [package.strip() for package in requirements_file.readlines()]

packages = find_packages()
package_root = packages[0]

setup(
    install_requires=requirements,
    package_data={
        package_root: ["**/data/*.json"],
    },
    include_package_data=True,
)
