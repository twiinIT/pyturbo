# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

"""Module contaning `FramePort` and `Frame` classes."""

import numpy as np
from cosapp.base import Port
from scipy.spatial.transform import Rotation as R

from pyturbo.ports.dynamics_connector import DynamicsConnector


class FramePort(Port):
    """Frame Port.

    Variables
    ---------
    position[m] : np.array
        Position of analysis.
    angle[rad] : np.array
        Rotation vector.
    """

    def setup(self):
        self.add_variable("position", np.r_[0.0, 0.0, 0.0], unit="m", desc="position")
        self.add_variable("angle", np.r_[0.0, 0.0, 0.0], unit="rad", desc="rotation")

    class Connector(DynamicsConnector):
        """Frame transfert connector."""

        pass

    def get_value(self):
        """Get the values stored in the port in a `Frame` object.

        Returns
        -------
        frame: Frame
            The Frame object with the values of the port.
        """
        frame = Frame()

        frame.position = self.position
        frame.angle = self.angle
        return frame

    def set_value(self, other):
        """Set the values stored in the port from a `Frame` or `FramePort` object.

        Returns
        -------
        self : FramePort
            The port with the new values.
        """
        self.position = other.position
        self.angle = other.angle
        return self

    def copy_port(self, other):
        """Copy the values of the port into another `FramePort` object.

        Parameters
        ----------
        other: FramePort
            The port from which the values are taken.
        """
        self.set_value(other.get_value())

    def null(self):
        """Restart all values as zero vectors."""
        self.set_value(Frame())


class Frame:
    """Frame class to handle frame in 3D space.

    Attributes
    ----------
    position[m] : np.array
        Position of analysis.
    angle[rad] : np.array
        Rotation vector.
    """

    def __init__(self):
        self.position: np.ndarray = np.r_[0.0, 0.0, 0.0]
        self.angle: np.ndarray = np.r_[0.0, 0.0, 0.0]  # radian

    def change_from_frame(self, frame):
        """Change the values of other from one frame to frame.

        Parameters
        ----------
        frame: Frame
            Object contaning information about position and rotation vector of other frame.

        Returns
        -------
        frame: Frame
            The new object with values transported from `frame` to base frame.
        """
        new_frame = Frame()
        rot_frame = R.from_rotvec(frame.angle)

        new_frame.position = frame.position + rot_frame.apply(self.position)
        new_frame.angle = R.as_rotvec(R.from_rotvec(self.angle) * R.from_rotvec(frame.angle))
        return new_frame

    def change_to_frame(self, frame):
        """Change other coordinate from frame self defined in reference frame to reference frame."""
        return self.change_from_frame(frame.inv())

    def inv(self):
        """Invert frame transformation.

        Returns
        -------
        inv: Frame
            The inverted frame.
        """
        inv = Frame()
        invrot = R.from_rotvec(-self.angle)

        inv.position = -invrot.apply(self.position)
        inv.angle = -invrot.apply(self.angle)

        return inv

    def __repr__(self):
        """Return a string representation."""
        return f"Frame: {self.position}, {self.angle}"
