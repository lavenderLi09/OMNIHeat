# Method and limitations

## Heating budget

Integrate volumetric heating with physical cell volumes, including the actual
stretched mesh and AMR leaf structure when applicable. Convert to erg/s before
using the checker. Supply each component separately and include its total.
If radial bands are supplied, they must cover the whole integration domain
without overlap. The utility checks arithmetic only; it cannot infer geometry,
units, integration correctness, or physical adequacy from scalar powers.

Heating inputs here are nonnegative deposition terms. Signed conduction,
radiation, mechanical work, and numerical corrections need a separate energy
ledger. Heating-power consistency does not establish thermal balance.

## Preparing model/OMNI comparisons

Before exporting pairs, record privately the OMNI product, retrieval/version,
variable definitions, units, quality flags and fill-value rules. Specify the
observation interval and retain valid/excluded sample counts. Model temperature
and number-density definitions must be reconciled with the observed species;
do not equate total-particle and proton quantities without a composition model.

Explicitly align epochs, sampling positions, reference frames, and any travel-time
mapping. Relaxation time is not automatically observation time. If propagation
or longitude mapping is used, retain its assumptions and uncertainty. This
repository performs no propagation, interpolation, resampling, or alignment.

For each accepted pair, define error as model minus observation. The comparison
reports arithmetic mean error (bias), mean absolute error (MAE), and root mean
square error (RMSE). Metrics share the input variable's units. Equal row weights
are appropriate only for the intended sampling design; missing-data patterns,
cadence, transients, and autocorrelation can affect interpretation. No confidence
interval or global solar-wind inference is provided.

## Calibration versus validation

Separate data used to choose parameters from independent evaluation data.
An observation-derived energy or mass-flux proxy is an assumption-dependent
constraint, not proof that the evolved MHD solution matches observations.
Assess numerical health, convergence, transport, and observational agreement
separately. The synthetic examples establish software behavior only.
