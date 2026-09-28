# Thermodynamic heating and OMNI audit

A public starter for checking integrated heating budgets and comparing
thermodynamic solar-wind model samples with observations prepared from OMNI.
It contains generic utilities and **synthetic examples only**.

This is not a release of a calibrated thermodynamic model, an OMNI downloader,
or a reproduction package for a particular simulation. There are no heating
coefficients, boundary conditions, magnetic inputs, observation windows, or
scientific results in this repository.

## Run

Python 3.9 or newer; standard library only. From the repository root:

```sh
python3 audit.py budget examples/synthetic_budget.json
python3 audit.py compare examples/synthetic_pairs.csv
python3 -m unittest discover -s tests -v
```

The budget example returns a synthetic total of 10 erg/s. The comparison
example returns count 2, bias 0, MAE 2, and RMSE 2 in arbitrary example units.
Neither example represents physical solar values. Commands write JSON to
stdout and do not upload input data.

## Inputs

- `budget`: JSON containing `global_power_erg_s` with arbitrary component
  names and `Htotal`. Optional `radial_band_power_erg_s` records must form
  an exhaustive, nonoverlapping partition and use identical component names.
  Powers must be finite and nonnegative. Sum checks use relative tolerance
  `1e-9` with zero absolute tolerance; this is a numerical consistency check,
  not an uncertainty estimate or a physical-validation criterion.
- `compare`: CSV with `model` and `observed` columns for **one variable in
  matching units**, with one already aligned pair per row. Additional columns
  are ignored. All samples receive equal weight. Invalid/nonfinite values
  fail the command; finite fill codes must be removed before use.

See [method and limitations](docs/METHOD.md) for preparation requirements and
[publication boundary](docs/PUBLICATION.md) before adding files.
