from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class CombustorAero(System):
    """A simple aerodynamic model of a combustor.

    This model takes into account a burner efficiency to compute exit temperature from
    inlet fluid (air) and fuel.
    The Fuel Heating Value is also an input of the model.

    Components
    ----------

    Physics
    -------

    Parameters
    ----------
    gas : IdealDryAir
        class provided the characteristics of gas as a simplistic air without fuel
        gas.h           : to get enthalpy from temperature
        gas.t_from_h    : to get temperature from enthapie

    Inputs
    ------
    fl_in : FluidPort

    Outputs
    -------
    fl_out : FluidPort

    Inwards
    -------
    fuel_W : float
        fuel consumption in kg/s
    fvh : float
        Fuel Heating Value in J/Kg
        default value is 46e6 J/Kg corresponding at fuel cosumption in air
    eff : float
        efficiency of combustion
        default value is 0.99

    Outwards
    --------
    Tcomb : float
        combustion temperature

    Off design methods
    ------------------

    Good practice
    -------------

    """

    def setup(self):
        # properties
        self.add_property("gas", IdealDryAir())  # not representing fuel/air mix yet

        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards / outwards
        self.add_inward("fuel_W", 1.0, unit="kg/s", desc="fuel flow")
        self.add_inward("fhv", 46.2e6, unit="J/kg", desc="Fuel Heating Value")
        self.add_inward("eff", 0.99, unit="", desc="combustion efficiency")

        self.add_outward("Tcomb", 0.0, unit="K", desc="combustion temperature")

    def compute(self):
        self.fl_out.pt = self.fl_in.pt
        self.fl_out.W = self.fl_in.W + self.fuel_W

        h_out = self.gas.h(self.fl_in.Tt) + self.fuel_W / self.fl_out.W * self.fhv * self.eff
        self.Tcomb = self.gas.t_from_h(h_out)
        self.fl_out.Tt = self.Tcomb
