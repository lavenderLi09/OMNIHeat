# OMNI-Heat

A public starter for checking integrated heating budgets and comparing
thermodynamic solar-wind model samples with observations prepared from OMNI.
It contains generic utilities, symbolic physics documentation, and **synthetic examples only**.


## Physics at a glance

The three-term heating law is

$$
H=A_{\exp}e^{-(r-r_0)/L_{\exp}}
+A_{\rm QS}f_{\rm QS}(r)\frac{B_{h,t}^{\,2}}{B_h(|B_{h,r}|+B_s)}
+A_{\rm AR}g_{\rm AR}(B_h)\left(\frac{B_h}{B_{\rm ref}}\right)^m,
$$

with radial and magnetic gates

$$
f_{\rm QS}(r)=\frac12\left[1+\tanh\left(\frac{r_c-r}{\Delta r}\right)\right]
e^{-(r-r_0)/L_{\rm QS}},\qquad
g_{\rm AR}(B_h)=\frac12\left[1+\tanh\left(\frac{B_h-B_c}{\Delta B}\right)\right].
$$

$\mathbf B_h$ is the field supplied to heating, $B_h=|\mathbf B_h|$, and
$B_{h,t}^{\,2}=B_{h,\theta}^{\,2}+B_{h,\phi}^{\,2}$. The amplitudes $A_i$,
length scales, field scales, and exponent $m$ are symbolic; no fitted values
are published. Define the QS magnetic factor as zero at a field null.

A compact ideal-MHD formulation with thermodynamic sources is

$$
\begin{aligned}
\partial_t\rho+\nabla\cdot(\rho\mathbf v)&=0,\\
\rho\frac{D\mathbf v}{Dt}&=-\nabla p+
\frac{(\nabla\times\mathbf B)\times\mathbf B}{4\pi}+\rho\mathbf g,\\
\partial_t\mathbf B&=\nabla\times(\mathbf v\times\mathbf B),
\quad\nabla\cdot\mathbf B=0,\\
\partial_t e+\nabla\cdot(e\mathbf v)&=-p\nabla\cdot\mathbf v
+H-\nabla\cdot\mathbf q-Q_{\rm rad}.
\end{aligned}
$$

Here $D/Dt=\partial_t+\mathbf v\cdot\nabla$, $e=p/(\gamma-1)$,
$p=\rho k_BT/(\mu m_p)$, and $\mathbf g=-GM_\odot\hat{\mathbf r}/r^2$.
These use Gaussian cgs in an inertial frame; $\mathbf q$ is heat flux and
$Q_{\rm rad}\ge0$ is radiative loss. The evolved field $\mathbf B$ and heating
field $\mathbf B_h$ are distinguished deliberately.

[Full equations, factor definitions, units, and references](docs/PHYSICS.md)
cover all three terms, internal and total energy, and transport. This is a
symbolic generalization of published models, not a selected simulation setup.

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
