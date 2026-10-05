# Images

All research figures displayed on the website are self-contained SVGs. Their lines, shapes, text, and LaTeX equations are vector paths, with no embedded bitmap labels or external fonts. `profile.png` is the original portrait photograph.

- `lindbladian-tebd.svg` — methodology figure in `../../notes.html`, also previewed on the homepage. It illustrates density-matrix vectorization, an MPS, alternating local channel gates, and SVD truncation, based on Chang Shu's slides. The convention is `\partial_t |\rho\rangle\!\rangle = \mathcal{L}|\rho\rangle\!\rangle`, so `\mathcal{E}(\Delta t) = \exp(\Delta t\,\mathcal{L})`. Method reference: [Zwolak & Vidal (2004)](https://arxiv.org/abs/cond-mat/0406440).
- `quantum-trajectories.svg` — Monte Carlo wavefunction figure in `../../notes.html`. Its source is [Section IV of the DQPT supplement](https://arxiv.org/pdf/2509.03570v2#page=13), Eqs. (50)–(57) and the numerical steps that follow. It shows discrete-time no-jump/jump sampling, normalization, and the average of pure-state projectors. The histories are schematic, not simulation data.
- `open-system.svg` — homepage spin-chain schematic, preserving the gain and loss channels of the original illustration. Its operator labels are now genuine LaTeX vector paths.
- `swssb.svg` — the first Research Story, based on [arXiv:2603.06363v2](https://arxiv.org/html/2603.06363v2). Its larger 1672 × 2500 canvas gives most of the space to explaining SWSSB. Panel 01 compares ordinary and nonlinear probes of the same mixed state and adds a local-information viewpoint; panel 02 is the spreading-order waterfall. These use the `H=0`, `L_j=\sqrt{\gamma}Z_jZ_{j+1}` example of Appendix A, starting from the all-`+x` state. The late-time state reached from this initial condition is `\rho_+=(I+X)/2^L`, with `X=\prod_jX_j`. Global parity stays fixed.

In panel 01, the blue arrows are schematic **Z-measurement outcomes**, not an ensemble decomposition: the state retains global off-diagonal Z-basis coherence. The two abstract density-matrix sheets and green loop represent the normalized two-copy overlap; they do not depict aligned physical copies or entanglement bonds. The mini plots show the exact steady-state limits `C_Z(r>0)=0` and `R_2(r>0)=1`. In the flip-test inset, `Z_i` flips an **X-basis** spin: `Z_i\rho_+Z_i=\rho_-=(I-X)/2^L`, which is orthogonal to `\rho_+`, while `Z_iZ_j\rho_+Z_jZ_i=\rho_+` even for distant sites. The latter permutes individual configurations within the original ensemble. The one-flip test is included to distinguish nonlinear order from simple pair invariance of a completely mixed state.

The local-information view compares the two fixed-point charge sectors `\rho_\pm=(I\pm Q)/2^L`, with `Q=\prod_jX_j` and eigenvalues `q=\pm1`. For any proper subset `A`, tracing out its nonempty complement removes the global Pauli string, giving `\rho_A^+=\rho_A^-=I_A/2^{|A|}`. Every measurement on `A` therefore has identical statistics in both sectors. Neutral site circles and arrows show restricting each state to the same patch, not configurations or evolution between sectors. This is an exact illustration for this pair-dephasing fixed point; local indistinguishability alone is not a full definition of generic SWSSB.

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
