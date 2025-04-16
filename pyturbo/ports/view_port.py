# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

"""Module contaning `ViewPort` and `View` classes."""

from copy import deepcopy
from dataclasses import dataclass, field

import numpy as np
from cosapp.ports import Port
from pyoccad.create import CreateTopology
from pyoccad.render import JupyterThreeJSRenderer
from pyoccad.transform import Rotate, Translate
from pyoccad.typing import VectorT
from scipy.spatial.transform import Rotation as R

from pyturbo.ports.dynamics_connector import DynamicsConnector
from pyturbo.ports.frame_port import Frame
from pyturbo.utils.view_tools import create_arrow, create_box, create_sphere, rotate


class ViewPort(Port):
    """ViewPort class to handle view in 3D space.

    Variables
    ---------
    shapes : dict
        Dictionary containing the view information (shapes and rendering options).
        Each entry is a pair `str: dict`, where the string key is the name of the shape and dict
        contains its information. The information dict has the mandatory `shape` key, storing the
        `pyoccad` object of the component. The other keys refer to rendering options.

    Example
    -------
    `ViewPort.shapes` definition:

    >>> {'cylinder': {'shape': create_cylinder(1.0, 1.0), 'face_color': 'blue'},
    ... 'sphere':{'shape': create_sphere(1.0), 'opacity': 0.7, 'face_color': 'red'}}
    """

    # TODO fix dict visualisation in docstring.

    def setup(self):
        self.add_variable("shapes", {}, desc="shapes in current frame")

    class Connector(DynamicsConnector):
        """Frame transfert connector."""

        pass

    def get_value(self):
        """Get the values stored in the port in a `View` object.

        Returns
        -------
        view: View
            The View object with the values of the port.
        """
        return View(self.shapes)

    def set_value(self, view):
        """Set the values stored in the port from a `View` or `ViewPort` object.

        Returns
        -------
        self : ViewPort
            The port with the new values.
        """
        self.shapes = view.shapes
        return self

    def copy_port(self, other):
        """Copy the values of the port into another `ViewPort` object.

        Parameters
        ----------
        other: ViewPort
            The port from which the values are taken.
        """
        self.set_value(other.get_value())

    def null(self):
        """Restart `shapes` dict as empty."""
        self.set_value(View({}))

    def render(self, **kwargs):
        """Visualise the geometry on jupyter notebook.

        Parameters
        ----------
        **kwargs :  optional
            Pyoccad rendering options.

        Returns
        -------
        render : Renderer
            The jupyter notebook widget with the visualisation.
        """
        view = self.get_value()
        return view.render(**kwargs)

    def set_shape_name(self, new_name, old_name=None):
        """Rename shape called `old_name` with `new_name`.

        If `old_name` is not given, renames the first shape as found in `shapes.keys()`.

        Parameters
        ----------
        new_name : str
            The new name of the shape.
        old_name : str, optional.
            The current name of the shape.

        Returns
        -------
        self : View
            The View object with the new names in `self.shape`.
        """
        self.set_value(self.get_value().set_shape_name(new_name, old_name))


@dataclass
class View:
    """Class containing view of components' geometrical representations.

    Parameters
    ----------
    shapes : dict
        Dictionary containing the view information (shapes and rendering options).
        Each entry is a pair `str: dict`, where the string key is the name of the shape and dict
        contains its information. The information dict has the mandatory `shape` key, storing the
        `pyoccad` object of the component. The other keys refer to rendering options.

    Example
    -------
    `View.shapes` definition:

    >>> {'cylinder': {'shape': create_cylinder(1.0, 1.0), 'face_color': 'blue'},
    ... 'sphere':{'shape': create_sphere(1.0), 'opacity': 0.7, 'face_color': 'red'}}
    """

    shapes: dict = field(default_factory=dict)

    def add_shape(self, name, shape, **kwargs):
        """Add shape to view.

        Parameters
        ----------
        name : str
            The name of the shape.
        shape : pyoccad shape
            The pyoccad object.
        kwargs : optional
            Additional geometry options (`face_color`, `opacity`, etc.).
        """
        self.shapes[name] = {"shape": shape} | kwargs

    def set_color(self, name, color):
        """Set color to view.

        Parameters
        ----------
        name : str
            The name of the shape.
        color : str
            The color to apply. It can be its html name (ex. `'dodgerblue'`) or its hexadecimal form
            (ex. `'#1E90FF'`).
        """
        self.shapes[name]["face_color"] = color

    def copy(self) -> "View":
        """Copy view into another `View` object.

        Returns
        -------
        view : View
            The object's copy.
        """
        view = View()
        view.shapes = deepcopy(self.shapes)
        return view

    def _check_names(self, names=None):
        """Handle name arguments."""
        if names is None:
            names = self.shapes.keys()
        elif isinstance(names, str):
            names = [names]
        return names

    def _handle_repeated_keys(self, *args, **kwargs):
        """Create new keys if necessary when merging several dicts."""
        if args and kwargs:
            raise NameError("Only args or kwargs are permitted, not both.")

        if kwargs:
            nd = {}
            for prefix, view in kwargs.items():
                for shape in view:
                    nd[f"{prefix}.{shape}"] = view[shape]
        else:
            nd = {}
            if not self._repeated_names(*args):
                for view in args:
                    nd = nd | view
                return nd
            for i, view in enumerate(args):
                for shape in view:
                    nd[f"{shape}_{i :d}"] = view[shape]
        return nd

    def _repeated_names(self, *args):
        """Check whether there are repeated keys in several dicts."""
        keys = []
        for a in args:
            keys += a.keys()
        counts = np.unique(keys, return_counts=True)[1]
        return np.any(counts > 1)

    def translate(self, vec: VectorT, names=None, inplace=True) -> "View":
        """Translate shapes by a given vectors.

        A new object is returned independendly of the value given to the `inplace` parameter. It
        determines however whether `self.shapes` will be modified or not.

        Parameters
        ----------
        vec[m] : iterable
            The vector to be translated by.
        names : str or list of str, optional
            The name or names of the shapes to be translated. If not given, all shapes are
            translated together.
        inplace : bool, default=True
            Whether to change the shapes in place or create a new view object containing the
            translated shapes.

        Returns
        -------
        view : View
            A view with the translated shapes.
        """
        names = self._check_names(names)
        shapes = {key: value for key, value in self.shapes.items() if key in names}
        for name in names:
            shapes[name]["shape"] = Translate.from_vector(shapes[name]["shape"], vec, inplace=False)

        if inplace:
            for name in names:
                self.shapes[name] = shapes[name]

        return View(shapes)

    def rotate(self, vec, point: VectorT = (0.0, 0.0, 0.0), names=None, inplace=True) -> "View":
        """Rotate shapes by a given rotation vector.

        A new object is returned independendly of the value given to the `inplace` parameter. It
        determines however whether `self.shapes` will be modified or not.

        Parameters
        ----------
        angle[rad] : np.array
            Rotation vector.
        point[m] : iterable, defult=(0.0, 0.0, 0.0)
            The reference point where the rotation axis pass, in other words the origin of `vec`.
        names : str or list of str, optional
            The name or names of the shapes to be rotated. If not given, all shapes are rotated
            together.
        inplace : bool, default=True
            Whether to change the shapes in place or create a new view object containing the
            translated shapes.

        Returns
        -------
        view : View
            A view with the rotated shapes.
        """
        names = self._check_names(names)

        point = np.array(point)
        shapes = self.translate(-point, names, inplace=False).shapes
        for name in names:
            angs = R.from_rotvec(vec).as_euler("xyz", False)
            shapes[name]["shape"] = Rotate.around_x(shapes[name]["shape"], angs[0], inplace=False)
            shapes[name]["shape"] = Rotate.around_y(shapes[name]["shape"], angs[1], inplace=False)
            shapes[name]["shape"] = Rotate.around_z(shapes[name]["shape"], angs[2], inplace=False)
        shapes = self.translate(point, names, inplace=False).shapes

        if inplace:
            for name in names:
                self.shapes[name] = shapes[name]
        return View(shapes)

    def change_from_frame(self, frame: Frame) -> "View":
        """Change the values of View from one frame to objects own frame.

        Parameters
        ----------
        frame: Frame
            Object contaning information about position and rotation vector of other frame.

        Returns
        -------
        view: View
            The new object with values transported from `frame` to base frame.
        """
        view = self.copy()
        view.rotate(frame.angle)
        view.translate(frame.position)
        return view

    def change_to_frame(self, frame):
        """Change the values of View base frame to another frame.

        Parameters
        ----------
        frame: Frame
            Object contaning information about position and rotation vector of other frame.

        Returns
        -------
        view: View
            The new object with values transported from base frame to `frame`.
        """
        return self.change_from_frame(frame.inv())

    def merge(self, *args: "View", prefixes=None) -> "View":
        """Merge two or more Views into one.

        Parameters
        ----------
        args : View
            The shapes to be merged with `self`.
        prefixes : list of str, optional
            If given, the prefixes will be added to the name of every shape accordingly to avoid
            name conflicts. If not given, numerical sufixes will be used instead. Example:

        Examples
        --------
        >>> v1 = View({'cyl': {'shape': create_cylinder(1.0, 1.0)},
        ... 'sph':{'shape': create_sphere(1.0)}})
        >>> v2 = View({'cyl': {'shape': create_cylinder(2.0, 2.0)},
        ... 'sph':{'shape': create_sphere(2.0)}})
        >>> v1.merge(v2).shapes.keys()
        {'cyl_0', 'sph_0', 'cyl_1', 'sph_1'}
        >>> v1.merge(v2, prefixes=['first', 'second']).shapes.keys()
        {'first.cyl', 'first.sph', 'second.cyl', 'second.sph'}
        """
        dicts = [view.shapes for view in args]
        dicts.insert(0, self.shapes)
        if prefixes:
            kwargs = {p: d for p, d in zip(prefixes, dicts)}
            return View(self._handle_repeated_keys(**kwargs))
        else:
            return View(self._handle_repeated_keys(*dicts))

    def merge_shapes(self, names=None, new_name=None, options=None, inplace=True) -> "View":
        """Merge several OCC shapes into one and save them under a new name.

        Parameters
        ----------
        names : list of str, optional
            The names of the shapes to merge. If not given, all shapes are merged.
        new_name : str, optional
            The new name of the shape. If not given, the name of the first shape is used.
        options : dict, optional
            The shape options to be applied. If not given, the options of the first shape are kept.
        inplace : bool, default=True
            Whether to update `self.shapes` or not. An object with the merged shapes is returned
            independently of the value passed here.

        Returns
        -------
        view : View
            A `View` object with the new shapes.
        """
        names = self._check_names(names)
        new_name = new_name or names[0]
        if options:
            new_options = options
        else:
            new_options = {
                i: self.shapes[names[0]][i] for i in self.shapes[names[0]] if i != "shape"
            }
        new_shape = CreateTopology.make_compound(*(self.shapes[name]["shape"] for name in names))
        view = View({new_name: {"shape": new_shape, **new_options}})

        if inplace:
            kept_names = [name for name in self.shapes.keys() if name not in names]
            self.shapes = {name: self.shapes[name] for name in kept_names} | view.shapes

        return view

    def add_number(self, number: float, pos: VectorT, name: str = "number", **kwargs):
        """Add the geometrical representation of a number, i.e. a sphere.

        Parameters
        ----------
        number : float
            The number to be represented.
        pos[m] : iterable
            The position where to put the sphere.
        name : str, default='number'
            The name of the shape.
        kwargs :
            Shape options.

        Returns
        -------
        self : View
            The view with the added shape.
        """
        self.shapes[name] = {
            "shape": create_sphere(number, pos),
            "options": {"face_color": "gray", "opacity": 0.5} | kwargs,
        }
        return self

    def add_sym_matrix(
        self,
        matrix=None,
        values=None,
        angle=None,
        pos=(0.0, 0.0, 0.0),
        name: str = "matrix",
        **kwargs,
    ):
        """Add a box representation of a symmetrical matrix.

        If the matrix is not given, its eigenvalues and rotation vector should be provided.
        Since the main application is to represent inertia matrices, the dimensions of the box are
        normalised such that `norm(1/values) = 1.0`. This generates a box where the dimensions are
        approximately aligned with the expected inertia values used in input.

        Parameters
        ----------
        matrix : np.array
            The matrix to be represented. If given, `values` and `angle` are ignored and directly
            calculated from the matrix.
        values : np.array
            The dimensions of the box to be created.
        angle[rad] : np.array
            The rotation vector to apply to the box.
        pos[m] : iterable
            The position where to put the box.
        name : str, default='matrix'
            The name of the shape.
        kwargs :
            Shape options.

        Returns
        -------
        self : View
            The view with the added shape.
        """
        if matrix is not None:
            if not np.all(matrix == matrix.T):
                raise ValueError("Matrix is not symmetric!")

            # Perform eigen decomposition
            values, vectors = np.linalg.eig(matrix)
            # The eigenvectors are the directions of the principal axes
            principal_axes = vectors

            # Compute the rotation matrix that aligns the original axes with the principal axes
            rotation_matrix = principal_axes.T

            # Convert the rotation matrix to Euler angles (in degrees)
            rotation = R.from_matrix(rotation_matrix)
            angle = rotation.as_rotvec()

        dims = (1 / values) / np.linalg.norm(1 / values)
        pos = np.array(pos)
        self.shapes[name] = {
            "shape": rotate(create_box(dims, pos), pos, angle),
            "face_color": "yellow",
            "opacity": 0.5,
        } | kwargs

        return self

    def add_vector(
        self, vec, pos, name: str = None, scaling: float = 1.0, size: float = 1.0, **kwargs
    ):
        """Add an arrow representation of a vector.

        Parameters
        ----------
        vec: iterable
            Numpy array, tuple or list with the vector to be represented.
        origin[m] : iterable
            Numpy array, tuple or list with the origin of the vector.
        scaling[-]: float, optional
            The scale factor to apply to `vec`.
        size[-]: float, optional
            The size factor to apply to the geometry radius and tip dimensions.
        kwargs :
            Shape options.

        Returns
        -------
        self: View
            The view contaning the arrow shape.
        """
        self.shapes[name] = {
            "shape": create_arrow(vec, pos, scaling, size),
            "face_color": "gold",
            "opacity": 0.5,
        } | kwargs
        return self

    def start_renderer(self, **kwargs):
        """Start renderer for future visualisation on jupyter notebook.

        Parameters
        ----------
        kwargs :
            Renderer options.

        Returns
        -------
        renderer : JupyterThreeJSRenderer
            The jupyter notebook renderer.
        """
        options = (
            dict(
                view_size=(1800, 800),
                camera_target=(0.0, 0.0, 0.0),
                camera_position=(5.0, 5.0, 1.0),
                grid_normal=(0.0, 1.0, 0.0),
                camera_quaternion=(0.0, 0.0, 0.0, 1.0),
            )
            | kwargs
        )

        renderer = JupyterThreeJSRenderer(**options)
        ang = -np.pi / 2.0
        renderer._displayed.rotateX(ang)
        renderer._ax.rotateX(ang)

        for name, dicts in self.shapes.items():
            shape_opts = {i: dicts[i] for i in dicts if i != "shape"}
            renderer.add_shape(dicts["shape"], uid=name, **shape_opts)

        return renderer

    def update_renderer(self, renderer):
        """Update renderer.

        Parameters
        ----------
        renderer : JupyterThreeJSRenderer
            Renderer to be updated.

        Returns
        -------
        renderer : JupyterThreeJSRenderer
            The updated renderer.
        """
        for name, value in self.shapes.items():
            shape = value.pop("shape")
            if name in renderer._mapping.keys():  # updating existant
                renderer.update_shape(shape, uid=name)
            else:  # adding new
                renderer.add_shape(shape, uid=name, **value)

        old = [i for i in renderer._mapping.keys() if i not in self.shapes.keys()]
        for name in old:  # removing old
            renderer.remove_shape(name)

        return renderer

    def render(self, **kwargs):
        """Visualise the geometry on jupyter notebook.

        Parameters
        ----------
        **kwargs :  optional
            Pyoccad rendering options.

        Returns
        -------
        render : Renderer
            The jupyter notebook widget with the visualisation.
        """
        renderer = self.start_renderer(**kwargs)
        return renderer.show()

    def set_shape_name(self, new_name, old_name=None):
        """Rename shape called `old_name` with `new_name`.

        If `old_name` is not given, renames the first shape as found in `shapes.keys()`.

        Parameters
        ----------
        new_name : str
            The new name of the shape.
        old_name : str, optional.
            The current name of the shape.

        Returns
        -------
        self : View
            The View object with the new names in `self.shape`.
        """
        old_name = old_name or list(self.shapes.keys())[0]
        self.shapes = {new_name if k == old_name else k: v for k, v in self.shapes.items()}
        return self
