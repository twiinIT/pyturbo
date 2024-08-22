import time

import matplotlib.pyplot as plt
import numpy as np
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder

from pyturbo.systems.nozzle.nozzle_aero import NozzleAero

t1 = time.time()

system = NozzleAero("nozzle")
driver = system.add_driver(RungeKutta("rk", order=2))
solver = driver.add_child(NonLinearSolver("solver", tol=1e-5))
# solver.add_equation("capacitor.elec_out.v==0.0")

driver.time_interval = (0, 1.0)
driver.dt = 0.005

driver.set_scenario(
    init={},
    values={"pamb": 101325.0 - 300 * time},
)

recorder = driver.add_recorder(DataFrameRecorder())

system.run_drivers()

print("fluid time = ", time.time() - t1)

data = driver.recorder.export_data()


Ul = np.asarray(data["inductance.elec_in.v"] - data["inductance.elec_out.v"])
Il = np.asarray(data["inductance.elec_in.intensity"])
Ur = np.asarray(data["resistor.elec_in.v"] - data["resistor.elec_out.v"])
Uc = np.asarray(data["capacitor.elec_in.v"] - data["capacitor.elec_out.v"])
E = np.asarray(data["battery.E"])
time = np.asarray(data["time"])
