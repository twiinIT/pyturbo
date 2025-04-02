# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Any, Dict, Iterable, Union

import numpy as np
from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape


class JupyterViewable:
    """JupyterViewable utils."""

    def jupyter_view(
        self,
        *,
        required: Union[Iterable[Union[System, str]], str] = "*",
        options: Dict[str, Dict[str, Any]] = None,
        **kwargs
    ):
        try:
            from pyoccad.render import JupyterThreeJSRenderer
        except ImportError:
            raise ImportError("Please install 'pyoccad' before using this function")

        super(System, self).__setattr__("_renderer", None)

        kwargs["view_size"] = kwargs.get("view_size", (1800, 800))
        kwargs["camera_target"] = kwargs.get("camera_target", (1.0, 0.0, 0.0))
        kwargs["camera_position"] = kwargs.get("camera_position", (-2.0, 1.0, 2.0))
        self._renderer = JupyterThreeJSRenderer(**kwargs)

        if options is None:
            options = {}

        def get_shape_options(name):
            split_name = name.split(".")
            names = [split_name[0]]
            for i in range(1, len(split_name)):
                names.append(".".join((names[-1], split_name[i])))
            opt = {}
            for n in names:
                opt.update(options.get(n, {}))
            return opt

        def add_to_renderer(name, shape):
            if isinstance(shape, TopoDS_Shape):
                opt = get_shape_options(name)
                self._renderer.add_shape(shape, uid=name, **opt)
            elif isinstance(shape, dict):
                for n, s in shape.items():
                    add_to_renderer(".".join((name, n)), s)
            else:
                raise TypeError("Unsupported type")

        for name, shape in self._to_occt().items():
            add_to_renderer(name, shape)

        return self._renderer.show()

    def update_jupyter_view(self):
        self._renderer.update_shape(self._to_occt(), uid=self.name)


def add_nacelle_brand(nacelle_geom: System, renderer, brand_path: str):
    """Add brand on nacelle geometry."""
    try:
        from pythreejs import ImageTexture, MeshStandardMaterial
    except ImportError:
        raise ImportError("Please install 'pythreejs' before using this function")

    logo = ImageTexture(imageUri=brand_path)
    renderer.add_shape(
        nacelle_geom._brand_shape(),
        uid="brand",
        plot_edges=False,
        face_material=MeshStandardMaterial(
            map=logo,
            transparent=True,
            side="DoubleSide",
        ),
        uv_rotation=np.pi / 2,
    )
