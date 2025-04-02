# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.base import System
from pyoccad.render.threejs import Renderer

from pyturbo.ports.frame_port import FramePort
from pyturbo.ports.view_port import ViewPort
from pyturbo.utils import create_cylinder, create_sphere


class SystemView(System):
    """System for one level position ports."""

    def setup(self):
        self.add_input(FramePort, "frame")
        self.add_output(ViewPort, "view")


class SystemComponent(System):
    """System for one level position ports."""

    def setup(self):
        self.add_input(FramePort, "s1_frame")
        self.add_input(FramePort, "s2_frame")

        self.add_output(ViewPort, "view")

        self.add_child(SystemView("s1"), pulling={"view": "view1", "frame": "s1_frame"})
        self.add_child(SystemView("s2"), pulling={"view": "view2", "frame": "s2_frame"})

    def compute(self):
        self.view.set_value(self.view1.get_value().merge(self.view2.get_value()))


def test_setup():
    """Test system setup."""
    assert SystemView("sys")
    assert SystemComponent("sys")


def test_runonce():
    """Test run_once on system."""
    sys = SystemComponent("sys")
    sys.run_once()


def test_copy_view():
    """Test the copy of view object."""
    sys = SystemComponent("sys")
    sys.s1.view.get_value().add_shape(name="cyl", shape=create_cylinder(1.0, 2.0))

    view2 = sys.s1.view.get_value().copy()

    assert view2.shapes.keys() == sys.s1.view.get_value().shapes.keys()


def test_merge():
    """Test the merging of two view object."""
    sys = SystemComponent("sys")
    sys.s1.view.get_value().shapes["cyl"] = {"shape": create_cylinder(1.0, 2.0)}
    sys.s2.view.get_value().shapes["cyl"] = {"shape": create_cylinder(1.0, 2.0)}

    sys.s1.view.get_value().shapes["sph"] = {"shape": create_sphere(1.0, (0.0, 0.0, 0.0))}
    sys.s2.view.get_value().shapes["sph"] = {"shape": create_sphere(1.0, (0.0, 0.0, 0.0))}

    sys.run_once()

    view3 = sys.view1.get_value().merge(sys.view2.get_value())

    assert len(view3.shapes.keys()) == 4  # all are kept with changed names
    assert "cyl_0" in view3.shapes.keys()  # numerical sufixes

    view3 = sys.view1.get_value().merge(sys.view2.get_value(), prefixes=["first", "second"])
    assert len(view3.shapes.keys()) == 4  # all are kept with changed names
    assert "first.cyl" in view3.shapes.keys()  # custom prefixes


def test_view_render():
    """Test the rendering of view object."""
    sys = SystemComponent("sys")
    assert isinstance(sys.s1.view.get_value().start_renderer().show(), Renderer)
