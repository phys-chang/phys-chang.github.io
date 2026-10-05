# Chang Shu — personal homepage

A clean static academic homepage designed for GitHub Pages. The layout is inspired by Ethan Lake's spare academic homepage style: large centered title, thin pale-blue rules, simple navigation, concise intro text, publications, and illustrated research stories.

The research narrative is written with **open quantum systems** and **many-body dynamics** as the current focus, while **non-Hermitian physics** appears as a set of spectral and boundary-sensitive tools. The visual system is deliberately line-based rather than card-based, with a pale-blue palette.

## Files

- `index.html` — homepage
- `publications.html` — selected publications with topic filters
- `papers.html` — redirect alias to `publications.html`
- `notes.html` — Visual Stories: numerical methodology first, followed by illustrated stories of individual papers
- `styles.css` — typography, layout, responsive styling; pale-blue palette with line separators rather than boxed cards
- `script.js` — LaTeX rendering, topic filter, and dynamic footer year
- `publications.bib` — BibTeX entries for selected papers
- `assets/img/profile.png` — portrait photograph
- `assets/img/open-system.svg` — vector spin-chain schematic with gain and loss channels
- `assets/img/lindbladian-tebd.svg` — vector methodology illustration, based on the author's slides
- `assets/img/quantum-trajectories.svg` — vector Monte Carlo wavefunction illustration, based on the DQPT supplement
- `assets/img/swssb.svg` — larger introductory research story with analytic waterfall profiles, based on arXiv:2603.06363v2
- `assets/figures/*.tex` — editable LaTeX/TikZ sources with a shared visual style
- `scripts/build_figures.py` — rebuilds the self-contained SVGs with outlined LaTeX glyphs
- `assets/img/README.md` — figure conventions, scientific references, and build instructions
- `notes/README.md` — guidance for adding future visual research stories
- `.nojekyll` — keeps GitHub Pages from running Jekyll

## Customize

1. Update the introduction, portrait, and contact details in `index.html`.
2. Add vector research illustrations under `assets/img/`, with editable sources under `assets/figures/`. In `notes.html`, put numerical methods in Methodology and illustrated accounts of individual papers in Research Stories.
3. Keep publication metadata current by copying entries from arXiv or Google Scholar.

## Vector figures

All displayed research figures use SVG, including LaTeX equations exported as vector paths. To rebuild them, install LaTeX with `standalone`, `newtx`, and TikZ plus `dvisvgm`, then run `python3 scripts/build_figures.py`. See `assets/img/README.md` for the shared figure style and source references. The older PNG illustrations are retained as design references.

## Equations

All content pages load [KaTeX](https://katex.org/docs/autorender.html) 0.19.0 with shared rendering options in `script.js`. Write inline mathematics as `\(d^2\)` and display equations as `\[ ... \]`. Use LaTeX source for every equation in webpage text; keep image alt text readable without a math renderer. Display equations sit in a `.method-equation` container and can scroll horizontally on small screens.

The KaTeX CSS and JavaScript come from pinned CDN URLs with integrity checks. When changing the shared CSS or JavaScript, update their `?v=` value in all content pages so browsers fetch the new version.

## Deploy on GitHub Pages

Upload these files to a repository named `username.github.io`, or to any repository with Pages enabled. In GitHub, go to **Settings → Pages**, choose the branch/folder, and save.
