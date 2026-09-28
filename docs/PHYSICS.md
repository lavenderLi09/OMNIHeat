# Equations and symbolic factors

This is a general single-fluid thermodynamic MHD formulation with a
Lionello-inspired composite heating prescription. It documents mathematical
structure, not a calibrated case. All adjustable coefficients, reference scales,
composition choices, and magnetic-field evaluation choices remain unspecified.
The audit CLI checks exported scalars; it does not solve these equations.

## Three heating terms

Let $r$ be physical heliocentric distance and $r_0$ a reference radius. Use the
same length unit for all radii and scale lengths, and the same magnetic unit for
all field quantities. In Gaussian cgs, heating has units erg cm$^{-3}$ s$^{-1}$.

$$
H=H_{\exp}+H_{\rm QS}+H_{\rm AR},
\qquad H_{\exp}=A_{\exp}\exp\!\left[-\frac{r-r_0}{L_{\exp}}\right].
$$

$$
H_{\rm QS}=A_{\rm QS} f_{\rm QS}(r) w_{\rm QS}(\mathbf B_h),
\qquad
f_{\rm QS}(r)=\frac12\left[1+\tanh\!\left(\frac{r_c-r}{\Delta r}\right)\right]
\exp\!\left[-\frac{r-r_0}{L_{\rm QS}}\right].
$$

$$
w_{\rm QS}(\mathbf B_h)=\frac{B_{h,t}^{\,2}}{B_h(|B_{h,r}|+B_s)},
\qquad B_{h,t}^{\,2}=B_{h,\theta}^{\,2}+B_{h,\phi}^{\,2},
\qquad B_h=|\mathbf B_h|.
$$

$$
H_{\rm AR}=A_{\rm AR}g_{\rm AR}(B_h)
\left(\frac{B_h}{B_{\rm ref}}\right)^m,
\qquad
 g_{\rm AR}(B_h)=\frac12\left[1+\tanh\!\left(\frac{B_h-B_c}{\Delta B}\right)\right].
$$

At $B_h=0$, define $w_{\rm QS}=0$ by continuity for $B_s>0$.
A numerical field floor is an implementation choice and must be documented
separately. The QS magnetic factor is dimensionless but need not be bounded by
one; the tanh gates lie between zero and one.

These are symbolic generalizations of the exponential and composite heating
forms in [Lionello, Linker & Mikić (2009), Eqs. (12), (16)–(18), journal pp.
905 and 907](https://doi.org/10.1088/0004-637X/690/1/902).
The reference radius, gates, scales, amplitudes, and exponent here are free
symbols; this is not a claim to reproduce the paper's parameter choices.

## Amplitudes and weighting factors

| Symbol | Meaning | Units or constraint |
|---|---|---|
| $A_{\exp},A_{\rm QS},A_{\rm AR}$ | Heating amplitudes | erg cm$^{-3}$ s$^{-1}$; nonnegative |
| $r_0$ | Reference radius for exponential envelopes | cm |
| $L_{\exp},L_{\rm QS}$ | Radial decay lengths | cm; positive |
| $r_c,\Delta r$ | QS cutoff radius and transition width | cm; $\Delta r>0$ |
| $B_s$ | Radial-field softening scale in the QS factor | G; positive |
| $B_{\rm ref}$ | AR field normalization | G; positive |
| $B_c,\Delta B$ | AR gate threshold and width | G; $\Delta B>0$ |
| $m$ | AR magnetic-strength exponent | dimensionless; positive |
| $f_{\rm QS}$ | Radial cutoff times radial decay | dimensionless |
| $w_{\rm QS}$ | Tangential/radial magnetic weighting | dimensionless |
| $g_{\rm AR}$ | Smooth magnetic-strength gate | dimensionless |
| $\mathbf B_h$ | Field supplied to the heating law | G |

The supplied heating field may be frozen, $\mathbf B_h(\mathbf x)=\mathbf
B(\mathbf x,t_0)$, or evolving, $\mathbf B_h(\mathbf x,t)=\mathbf B(\mathbf
x,t)$. These are different closures; neither is selected by this public
repository. A magnetic-strength gate is not an open/closed field-line mask.
No topology multiplier appears in the equations above.

## Thermodynamic MHD

In an inertial frame, for ideal induction, isotropic gas pressure, solar gravity,
and no explicit viscosity or resistivity, use Gaussian cgs:

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0,
$$

$$
\frac{\partial(\rho\mathbf v)}{\partial t}
+\nabla\cdot\left[\rho\mathbf v\mathbf v+
\left(p+\frac{B^2}{8\pi}\right)\mathbf I-
\frac{\mathbf B\mathbf B}{4\pi}\right]=\rho\mathbf g,
\qquad \mathbf g=-\frac{GM_\odot}{r^2}\hat{\mathbf r},
$$

$$
\frac{\partial\mathbf B}{\partial t}=\nabla\times(\mathbf v\times\mathbf B),
\qquad \nabla\cdot\mathbf B=0,
$$

$$
\frac{\partial e}{\partial t}+\nabla\cdot(e\mathbf v)
=-p\nabla\cdot\mathbf v+H-\nabla\cdot\mathbf q-Q_{\rm rad},
\qquad e=\frac{p}{\gamma-1},
\qquad p=\frac{\rho k_B T}{\mu m_p}.
$$

Here $\rho$, $\mathbf v$, $p$, $\mathbf B$, and $e$ are mass density, velocity,
gas pressure, evolved magnetic field, and internal-energy density. $\mathbf I$
is the identity tensor and juxtaposed vectors denote dyadic products.
$\gamma>1$ is the evolved adiabatic index; $\mu$ is dimensionless mean molecular
weight for the chosen composition and single-temperature closure. Neither is
specified numerically. The heating field $\mathbf B_h$ need not equal $\mathbf B$.

The equivalent smooth-solution total-energy form is

$$
E=e+\frac12\rho v^2+\frac{B^2}{8\pi},
$$

$$
\frac{\partial E}{\partial t}
+\nabla\cdot\left[\left(E+p+\frac{B^2}{8\pi}\right)\mathbf v
-\frac{(\mathbf v\cdot\mathbf B)\mathbf B}{4\pi}+\mathbf q\right]
=\rho\mathbf v\cdot\mathbf g+H-Q_{\rm rad}.
$$

$E$ excludes gravitational potential energy. Gravity contributes mechanical work
in this total-energy equation, not an additional empirical internal heating
term. Shock heating and numerical dissipation require a consistent discrete
energy treatment; the internal-energy equation alone does not specify it.
These dimensional equations do not specify solver normalization, rotation-frame
terms, divergence cleaning, or floors. See the [MPI-AMRVAC equation reference](https://amrvac.org/md_doc_2equations.html)
for the distinction between continuum equations and supported numerical forms.

## Transport and radiation factors

A field-aligned Spitzer flux and a symbolic Spitzer/Hollweg blend can be written

$$
\mathbf q_S=-\kappa_0T^{5/2}\hat{\mathbf b}
(\hat{\mathbf b}\cdot\nabla T),\qquad \hat{\mathbf b}=\mathbf B/B,
$$

$$
\mathbf q=f_c(r)\mathbf q_S+[1-f_c(r)]\mathbf q_H,
\qquad f_c(r)=\frac{1}{1+(r/r_H)^2},
\qquad \mathbf q_H=C_Hp\mathbf v.
$$

$\kappa_0$ has units erg s$^{-1}$ cm$^{-1}$ K$^{-7/2}$, $r_H>0$ is a
transition length, and $C_H$ is dimensionless. This symbolic blend follows the
structure in [Fan (2017), Eqs. (9)–(12)](https://doi.org/10.3847/1538-4357/aa7a56);
no numerical transport coefficients are selected here. A null-field treatment
must be specified in an implementation. Use the divergence of the complete
weighted flux: spatial derivatives of $f_c$ cannot simply be omitted.

Choose a nonnegative loss convention, for example

$$
Q_{\rm rad}=n_en_H\Lambda(T)\ge0.
$$

$n_e$ and $n_H$ are electron and hydrogen-nucleus number densities in cm$^{-3}$;
$\Lambda$ has units erg cm$^3$ s$^{-1}$ for this convention. Other cooling-table
normalizations require explicit conversion; the table and composition are not
specified. Heat flux has units erg cm$^{-2}$ s$^{-1}$, so its divergence has
volumetric-heating units. Conduction redistributes energy and is not inherently
positive local heating.

## Connection to an OMNI audit

For each heating component, compute $P_i=\int_V H_i\,dV$ in erg/s. The budget
checker verifies sums of these supplied powers. Comparing them with an
observation-derived energy requirement requires an additional transport,
radiative-loss, mass-flux, geometry, and propagation model; these equations do
not turn a single-spacecraft sample into a measured global heating power.
See [the audit method](METHOD.md) for alignment and validation limitations.
