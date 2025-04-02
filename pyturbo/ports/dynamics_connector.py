# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.base import BaseConnector
from cosapp.ports import Port


class DynamicsConnector(BaseConnector):
    """Custom connector with automatic transformation between coordinate systems."""

    def __init__(self, name: str, sink: Port, source: Port, *args, **kwargs):
        super().__init__(name, sink, source)

    def transfer(self) -> None:

        sink = self.sink
        source = self.source

        # Implement: sink.target = source.origin
        for target, origin in self.mapping.items():
            setattr(sink, target, getattr(source, origin))

        # source(parent) --> sink(child)
        if sink.owner.parent == source.owner:
            parent = source.owner

            frame_name = f"{sink.owner.name}_frame"
            if frame_name in parent:
                frame = parent[frame_name].get_value()
                sink.set_value(source.get_value().change_to_frame(frame))

        # source(child) --> sink(parent)
        if sink.owner == source.owner.parent:
            parent = sink.owner

            frame_name = f"{source.owner.name}_frame"
            if frame_name in parent:
                frame = parent[frame_name].get_value()
                sink.set_value(source.get_value().change_from_frame(frame))

        # source(child) --> sink(child)
        if sink.owner.parent == source.owner.parent:
            parent = sink.owner.parent

            frame_name = f"{source.owner.name}_frame"
            if frame_name in parent:
                frame = parent[frame_name].get_value()
                sink.set_value(source.get_value().change_from_frame(frame))

            frame_name = f"{sink.owner.name}_frame"
            if frame_name in parent:
                frame = parent[frame_name].get_value()
                sink.set_value(source.get_value().change_to_frame(frame))
