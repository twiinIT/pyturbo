# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.thermo import IdealGas


class IdealDryAir(IdealGas):
    """Dry Air."""

    def __init__(self) -> None:
        super().__init__(287.058, 1004.0)
