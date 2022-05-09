from cosapp.ports import Port


class ShaftPort(Port):
    def setup(self):
        self.add_variable("power", 1e6, unit="W", desc="mechanical power")
        self.add_variable("N", 5000.0, unit="rpm", desc="rotational speed")
