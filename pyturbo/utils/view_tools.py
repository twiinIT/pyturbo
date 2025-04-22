# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

"""Utility functions for visualisation."""

import numpy as np
from cosapp.base import System
from pyoccad.create import (
    CreateAxis,
    CreateBox,
    CreateRevolution,
    CreateSphere,
    CreateTopology,
    CreateWire,
)
from pyoccad.transform import Rotate, Translate
from scipy.spatial.transform import Rotation as R


def view_system(sys: System):
    """View System in Jupyter Lab environement."""
    try:
        return sys.occ_view.get_value().render()
    except KeyError:
        raise (f"Missing occ_view port in system{sys.name}")


def create_cylinder(r: float, h: float, r_top_bottom: float = 1.0):
    """Create a cylinder from radius and height, with base in the xy plane.

    Parameters
    ----------
    r[m] : float
        Cylinder radius.
    h[m] : float
        Cylinder height.
    r_top_bottom[-] : float, optional
        Ratio R_top/R_bottom if the section of a cone is desired.

    Returns
    -------
    shape: pyoccad shape
        The pyoccad shape of the cylinder.
    """
    w = CreateWire.from_points(
        ([0.0, 0.0, h], [r * r_top_bottom, 0.0, h], [r, 0.0, 0], [0.0, 0.0, 0]),
        auto_close=True,
    )
    return CreateRevolution.surface_from_curve(w, CreateAxis.oz())


def create_cone(r: float, h: float):
    """Generate a cone from radius and height, with base in the xy plane.

    Parameters
    ----------
    r[m] : float
        Base radius.
    h[m] : float
        Cone height.

    Returns
    -------
    shape: pyoccad shape
        The pyoccad shape of the cone.
    """
    w = CreateWire.from_points(
        ([0.0, 0.0, h], [r, 0.0, 0], [0.0, 0.0, 0]),
        auto_close=True,
    )
    return CreateRevolution.surface_from_curve(w, CreateAxis.oz())


def create_sphere(r: float, pos):
    """Generate a sphere from radius and center position.

    Parameters
    ----------
    r[m] : float
        Sphere radius.
    pos[m] : np.array
        Sphere center position..

    Returns
    -------
    shape: pyoccad shape
        The pyoccad shape of the sphere.
    """
    return CreateSphere.solid_from_radius_and_center(r, pos)


def create_box(dims, pos):
    """Create a box with dimensions `dims` and center `pos`.

    Parameters
    ----------
    dims[m] : np.array
        x, y, and z dimensions of the box.
    pos[m] : np.array
        Box center position..

    Returns
    -------
    shape: pyoccad shape
        The pyoccad shape of the box.
    """
    return CreateBox.from_dimensions_and_center(dims, pos)


def translate(shape, vec):
    """Translate `shape` by `vec`.

    Parameters
    ----------
    shape: pyoccad shape
        The shape to be translated
    vec[m] : iterable
        A numpy array, list or tuple with the translation vector.

    Returns
    -------
    shape: pyoccad shape
        The translated shape
    """
    return Translate.from_vector(shape, vec, inplace=False)


def rotate(shape, point, vec):
    """Rotate `shape` around axis defined by `point` and `vec`.

    Parameters
    ----------
    shape: pyoccad shape
        The shape to be rotated
    point[m] : iterable
        A numpy array, list or tuple with the origin of the rotation vector.
    vec[rad] : iterable
        A numpy array, list or tuple with the rotation vector.

    Returns
    -------
    shape: pyoccad shape
        The rotated shape
    """
    shape = translate(shape, -point)

    angs = R.from_rotvec(vec).as_euler("xyz", False)
    Rotate.around_x(shape, angs[0], inplace=True)
    Rotate.around_y(shape, angs[1], inplace=True)
    Rotate.around_z(shape, angs[2], inplace=True)

    return translate(shape, point)


def create_arrow(vec, origin, scaling=1.0, size=1.0):
    """Generate an arrow shape to represent a vector.

    Parameters
    ----------
    vec: iterable
        Numpy array, tuple or list with the vector to be represented.
    origin[m] : iterable
        Numpy array, tuple or list with the origin of the vector.
    scaling: float, optional
        The scale factor to apply to `vec`.
    size: float, optional
        The size factor to apply to the geometry radius and tip dimensions.

    Returns
    -------
    shape: pyoccad shape
        The arrow shape representing the vector.
    """
    # getting direction
    if np.linalg.norm(vec) == 0.0:
        tip_pos = tuple(np.array(origin))
        tip = translate(create_cone(0.0, 1.0), tip_pos)
        return tip

    rot_vec = R.align_vectors(vec, (0.0, 0.0, 1.0))[0].as_rotvec()

    # generating tip
    tip_pos = tuple(np.array(origin) + np.array(vec) * scaling)
    tip = translate(rotate(create_cone(0.15 * size, 0.5 * size), np.zeros(3), rot_vec), tip_pos)

    # generating line
    h = np.linalg.norm(vec) * scaling
    column = translate(rotate(create_cylinder(0.05 * size, h), np.zeros(3), rot_vec), origin)

    # combining and returning
    return CreateTopology.make_compound(tip, column)
