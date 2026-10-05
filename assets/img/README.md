# Images

All research figures displayed on the website are self-contained SVGs. Their lines, shapes, text, and LaTeX equations are vector paths, with no embedded bitmap labels or external fonts. `profile.png` is the original portrait photograph.

- `lindbladian-tebd.svg` — methodology figure in `../../notes.html`, also previewed on the homepage. It illustrates density-matrix vectorization, an MPS, alternating local channel gates, and SVD truncation, based on Chang Shu's slides. The convention is `\partial_t |\rho\rangle\!\rangle = \mathcal{L}|\rho\rangle\!\rangle`, so `\mathcal{E}(\Delta t) = \exp(\Delta t\,\mathcal{L})`. Method reference: [Zwolak & Vidal (2004)](https://arxiv.org/abs/cond-mat/0406440).
- `quantum-trajectories.svg` — Monte Carlo wavefunction figure in `../../notes.html`. Its source is [Section IV of the DQPT supplement](https://arxiv.org/pdf/2509.03570v2#page=13), Eqs. (50)–(57) and the numerical steps that follow. It shows discrete-time no-jump/jump sampling, normalization, and the average of pure-state projectors. The histories are schematic, not simulation data.
- `open-system.svg` — homepage spin-chain schematic, preserving the gain and loss channels of the original illustration. Its operator labels are now genuine LaTeX vector paths.
- `swssb.svg` — the first Research Story, based on [arXiv:2603.06363v2](https://arxiv.org/html/2603.06363v2). Its larger 1672 × 2680 canvas gives most of the space to explaining SWSSB. Panel 01 compares ordinary and nonlinear probes of the same mixed state and contrasts unbroken strong symmetry with SWSSB through local charge learnability; panel 02 is the spreading-order waterfall. The original diagnostics and waterfall use the `H=0`, `L_j=\sqrt{\gamma}Z_jZ_{j+1}` example of Appendix A, starting from the all-`+x` state. The late-time state reached from this initial condition is `\rho_+=(I+X)/2^L`, with `X=\prod_jX_j`. Global parity stays fixed in this evolution.

In panel 01, the blue arrows are schematic **Z-measurement outcomes**, not an ensemble decomposition: the state retains global off-diagonal Z-basis coherence. The two abstract density-matrix sheets and green loop represent the normalized two-copy overlap; they do not depict aligned physical copies or entanglement bonds. The mini plots show the exact steady-state limits `C_Z(r>0)=0` and `R_2(r>0)=1`. In the flip-test inset, `Z_i` flips an **X-basis** spin: `Z_i\rho_+Z_i=\rho_-=(I-X)/2^L`, which is orthogonal to `\rho_+`, while `Z_iZ_j\rho_+Z_jZ_i=\rho_+` even for distant sites. The latter permutes individual configurations within the original ensemble. The one-flip test is included to distinguish nonlinear order from simple pair invariance of a completely mixed state.

The local-learnability view follows [Divi, Lessa and Wang, arXiv:2605.28967v1, Introduction and Section III](https://arxiv.org/html/2605.28967v1). Both columns compare `\rho` with the same charge-changing probe `\sigma=Z_i\rho Z_i`, with the insertion **inside** the local patch `A`. Left: the all-`+x` product state and its single-flip partner have opposite global parities and orthogonal local states, so measuring `X_i` identifies the charge change (`F_A=0`). The plus/minus symbols label X eigenstates. Right: the fully scrambled fixed-point sectors `\rho_\pm=(I\pm Q)/2^L`, with `Q=\prod_jX_j`, have `\rho_A=\sigma_A=I_A/2^{|A|}` on every proper subset (`F_A=1`). Neutral site circles represent identical local mixed states, not individual outcomes. The gold arrows denote the same local probe, not charge-preserving evolution.

Here `F_A=F(\rho_A,\sigma_A)` is root fidelity. In the local infinite-system formulation, the growing-window limit vanishes in an unbroken strong phase and is nonzero for local SWSSB. Global fidelity SWSSB implies the local criterion; the converse need not hold. Generic SWSSB only prevents perfect local discrimination, rather than requiring exactly identical patch states. Do not assert that any arbitrary patch reveals the absolute charge of an arbitrary strongly symmetric state: a flip outside the patch is invisible even in a product state. [Unlearnable phases of matter, arXiv:2602.11262v2](https://arxiv.org/html/2602.11262v2) provides a complementary result for learning global charge from local statistical queries; monitored charge learning instead uses a time-dependent measurement record. These are related but distinct protocols.

The SWSSB waterfall contains analytic profiles `R_2(r,t)=[\tanh(2\gamma t)]^{|r|}` at `\gamma t=0.30,0.45,\ldots,1.20`, with signed displacement `r=i-j` and range `\xi=-1/\ln[\tanh(2\gamma t)]`. Ordinary separated-site `Z` correlations vanish in this introductory example. These profiles are not TEBD simulation data. The small final comparison summarizes the exponential `\mathbb{Z}_2` and algebraic `U(1)` growth established in Sections III–IV. Do not apply the zero ordinary-correlation claim to every model: the original gapless `\mathbb{Z}_2` example has an intermediate SWSSB window before its eventual GHZ state also develops conventional order. Onset times are effective finite-size scales; the infinite-chain transition is asymptotic.

## Editing and rebuilding

Edit the LaTeX/TikZ sources in `../figures/`. Colors, typography, line widths, panel headings, and process strips are shared in `../figures/figure-style.tex`. From the repository root, run:

```sh
python3 scripts/build_figures.py
```

The builder requires Python 3, LaTeX with `standalone`, `newtx`, and TikZ, and `dvisvgm` on `PATH`. It outlines every glyph and checks that exports contain no raster content or external dependencies. To rebuild one figure, pass its basename, for example `python3 scripts/build_figures.py quantum-trajectories`.

The earlier Imagegen PNGs and `.prompt.txt` files remain as design references. `open-system-placeholder.svg` is also archived; the website uses the new vector schematic.

## Shared figure style

Use `lindbladian-tebd.svg` and the shared TikZ styles as the reference for new figures.

- Match the margins, pale ice-blue background, and navy serif typography. Methodology figures use a 1672 × 941 landscape canvas; simple schematics can use a shorter canvas, and research stories can use a taller canvas to explain unfamiliar concepts.
- Use blue outlines and pale-blue fills for states, sage-green operators, and small gold arrows or jump markers. Keep line widths, corner radii, and subtle shadows consistent.
- Keep numbered panel badges, pale-blue separators, label sizes, and the bottom process strip consistent where the scientific narrative uses them.
- Use a modest descriptive subtitle; put the method or paper title in the webpage heading.
- Write every equation in LaTeX and export glyphs as paths. Label schematic histories as such and use actual data when displaying numerical results.
