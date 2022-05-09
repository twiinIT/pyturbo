from cosapp.ports import Port


class FluidPort(Port):
    def setup(self):
        self.add_variable("W", 1.0, unit="kg/s", desc="mass flow rate")
        self.add_variable("pt", 101325.0, unit="Pa", desc="total pressure")
        self.add_variable("Tt", 288.15, unit="K", desc="total temperature")
