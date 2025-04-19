# Copyright (C) 2025, twiinIT
# SPDX-License-Identifier: BSD-3-Clause


def pytest_addoption(parser):
    """Manage option in pytest."""
    parser.addoption(
        "--cosapp_system",
        action="store",
        default=None,
        help="Run tests only for classes with this exact name",
    )
