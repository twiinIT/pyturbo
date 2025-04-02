# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import json

import numpy as np


def load_from_json(system, file):
    """Add init system data from JSON file."""
    try:
        with open(file, "r") as f:
            params = json.load(f)

            for key, val in params.items():
                try:
                    if isinstance(system[key], np.ndarray):
                        system[key] = np.array(val)
                    else:
                        system[key] = val
                except KeyError:
                    raise KeyError(
                        f"File '{file}' is not consistent with system '{system.name}'"
                        f"(unknown key '{key}')."
                    )

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' does not exist.")

    return system


def save_to_json(system, file):
    """Save system data to JSON file."""

    def to_dict(system):
        def save(name, data, dd):
            if isinstance(data, float) or isinstance(data, int):
                dd[name] = data
            elif isinstance(data, np.ndarray):
                dd[name] = data.tolist
            else:
                print(f"Variable '{name}' of type '{type(data)}' is not saved.")

        dd = {}
        for _, child in system.children.items():
            dd.update({f"{child.name}.{name}": data for name, data in to_dict(child).items()})

        for name, data in system.inwards.items():
            save(name, data, dd)

        for _, port in system.inputs.items():
            for name, data in port.items():
                save(f"{port.name}.{name}", data, dd)

        return dd

    data = to_dict(system)
    try:
        with open(file, "w") as outfile:
            json.dump(data, outfile)

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' does not exist.")

    return system
