# History

## 0.2.0 (2023-01-10)

### Features

- Add new system `Atmosphere` to ease computing of ambient conditions

### Code quality & packaging

- Add `Compressor` to public API of the `systems.compressor` and `systems` modules

### Bug fix

- Fix `TurbineAero` exit total pressure computation from polytropic efficiency
- Fix some descriptions, especially related to gas models

## 0.1.0 (2022-10-18)

### Features

- Add additional models
  - add assemblies: `Turbofan`, `FanModule`, `Inlet`, `MixerFluid`/`MixerShaft`, `Nacelle`, `Nozzle`, `Channel`
  - add various standalone and base models: `FanDuctGeom`, `TurbofanGeom`, etc.
- Improve gas thermodynamic modeling (`IdealGas`)

### Code quality & packaging

- Add documentation using `sphinx` (incl. demo notebook rendering using `nbsphinx`)
- Improve code quality using `black`, `isosort` and `flake8`
- Improve tests coverage

## 0.0.1 (2022-05-25)

### Features

- First release
  - base models added: compressor, turbine, combustor, etc.
  - systems/assemblies added: fan module, gas generator, etc.

### Code quality & packaging

- Package structure (license file, etc.)
- Tests using `pytest`
