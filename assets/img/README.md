# Images

All research figures displayed on the website are self-contained SVGs. Their lines, shapes, text, and LaTeX equations are vector paths, with no embedded bitmap labels or external fonts. `profile.png` is the original portrait photograph.

- `lindbladian-tebd.svg` — methodology figure in `../../notes.html`, also previewed on the homepage. It illustrates density-matrix vectorization, an MPS, alternating local channel gates, and SVD truncation, based on Chang Shu's slides. The convention is `\partial_t |\rho\rangle\!\rangle = \mathcal{L}|\rho\rangle\!\rangle`, so `\mathcal{E}(\Delta t) = \exp(\Delta t\,\mathcal{L})`. Method reference: [Zwolak & Vidal (2004)](https://arxiv.org/abs/cond-mat/0406440).
- `quantum-trajectories.svg` — Monte Carlo wavefunction figure in `../../notes.html`. Its source is [Section IV of the DQPT supplement](https://arxiv.org/pdf/2509.03570v2#page=13), Eqs. (50)–(57) and the numerical steps that follow. It shows discrete-time no-jump/jump sampling, normalization, and the average of pure-state projectors. The histories are schematic, not simulation data.
- `open-system.svg` — homepage spin-chain schematic, preserving the gain and loss channels of the original illustration. Its operator labels are now genuine LaTeX vector paths.

## Editing and rebuilding

Edit the LaTeX/TikZ sources in `../figures/`. Colors, typography, line widths, panel headings, and process strips are shared in `../figures/figure-style.tex`. From the repository root, run:

```sh
python3 scripts/build_figures.py
```

The builder requires Python 3, LaTeX with `standalone`, `newtx`, and TikZ, and `dvisvgm` on `PATH`. It outlines every glyph and checks that exports contain no raster content or external dependencies. To rebuild one figure, pass its basename, for example `python3 scripts/build_figures.py quantum-trajectories`.

The earlier Imagegen PNGs and `.prompt.txt` files remain as design references. `open-system-placeholder.svg` is also archived; the website uses the new vector schematic.

## Shared figure style

Use `lindbladian-tebd.svg` and the shared TikZ styles as the reference for new figures.

- Match the landscape framing, margins, pale ice-blue background, and navy serif typography. Methodology figures use a 1672 × 941 canvas; simple schematics can use a shorter canvas.
- Use blue outlines and pale-blue fills for states, sage-green operators, and small gold arrows or jump markers. Keep line widths, corner radii, and subtle shadows consistent.
- Keep numbered panel badges, pale-blue separators, label sizes, and the bottom process strip consistent where the scientific narrative uses them.
- Use a modest descriptive subtitle; put the method or paper title in the webpage heading.
- Write every equation in LaTeX and export glyphs as paths. Label schematic histories as such and use actual data when displaying numerical results.
