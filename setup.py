"""The setup script."""

from setuptools import setup

with open("requirements.txt") as requirements_file:
    requirements = [package.strip() for package in requirements_file.readlines()]

setup(install_requires=requirements)
