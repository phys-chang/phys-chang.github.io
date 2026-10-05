# Visual Stories

The Visual Stories section lives at `../notes.html` and has two sections:

1. **Methodology** — how Chang Shu numerically studies open quantum systems: Lindbladian TEBD and Monte Carlo wavefunctions (quantum trajectories).
2. **Research Stories** — detailed illustrated stories of individual papers.

The first Research Story, `#swssb`, illustrates arXiv:2603.06363v2. It uses a taller figure than the methodology entries, with most of the space explaining SWSSB and the spreading nonlinear order before a compact scaling comparison.

Add SVG illustrations under `../assets/img/`, with editable LaTeX/TikZ sources under `../assets/figures/`, then feature them in the appropriate section. Link research stories to their corresponding papers.

Keep every new figure consistent with the visual conventions in `../assets/img/README.md` and the shared styles in `../assets/figures/figure-style.tex`. Rebuild figures from the repository root with `python3 scripts/build_figures.py`.
