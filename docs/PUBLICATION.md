# Publication boundary

This repository starts with new history and independently written generic
utilities. Only documentation, code, tests, and explicitly synthetic fixtures
are included. No prior repository history or case files are imported.

Keep these outside the public repository:

- Model configurations, parameter values, fitted coefficients, solver sources,
  boundary conditions, magnetic inputs, and selected observation intervals.
- Actual observations, model outputs, calibration products, plots, and logs.
- Internal paths, hostnames, job identifiers, source checksums, access details,
  conversation exports, credentials, and unpublished provenance.

The root `.gitignore` allows only individually reviewed files. It is an accidental
staging safeguard, not a security boundary: forced additions and already tracked
files bypass it. Review every staged diff and commit author identity before
pushing. Changing examples to real inputs also requires a new disclosure review.

Store real inputs and generated reports in a separate private directory. Do not
add a private Git remote or private history to this public checkout. Check Git
history as well as the current tree when reviewing a future release.
