# Chang Shu — personal homepage

A clean static academic homepage designed for GitHub Pages. The layout is inspired by Ethan Lake's spare academic homepage style: large centered title, thin pale-blue rules, simple navigation, concise intro text, publications, and illustrated research stories.

The research narrative is written with **open quantum systems** and **many-body dynamics** as the current focus, while **non-Hermitian physics** appears as a set of spectral and boundary-sensitive tools. The visual system is deliberately line-based rather than card-based, with a pale-blue palette.

## Files

- `index.html` — homepage
- `publications.html` — selected publications with topic filters
- `papers.html` — redirect alias to `publications.html`
- `notes.html` — Visual Stories: numerical methodology first, followed by illustrated stories of individual papers
- `styles.css` — typography, layout, responsive styling; pale-blue palette with line separators rather than boxed cards
- `script.js` — topic filter and dynamic footer year
- `publications.bib` — BibTeX entries for selected papers
- `assets/portrait-placeholder.svg` — replace with a real portrait when ready
- `assets/open-system-placeholder.svg` — replace with a spectrum, phase diagram, or dynamics sketch
- `assets/img/lindbladian-tebd.png` — generated methodology illustration, based on the author's slides
- `assets/img/lindbladian-tebd.prompt.txt` — full Imagegen prompt for the TEBD illustration
- `assets/img/quantum-trajectories.png` — Monte Carlo wavefunction illustration, based on the DQPT supplement and styled to match TEBD
- `assets/img/quantum-trajectories.prompt.txt` — full Imagegen prompt for the quantum trajectory illustration
- `notes/README.md` — guidance for adding future visual research stories
- `.nojekyll` — keeps GitHub Pages from running Jekyll

## Customize

1. Replace `assets/portrait-placeholder.svg` with your headshot, for example `assets/headshot.jpg`.
2. In `index.html`, update the `<img>` path to `assets/headshot.jpg`.
3. Replace the placeholder GitHub link with your GitHub profile.
4. Add research illustrations under `assets/img/`. In `notes.html`, put numerical methods in Methodology and illustrated accounts of individual papers in Research Stories.
5. Keep publication metadata current by copying entries from arXiv or Google Scholar.

## Deploy on GitHub Pages

Upload these files to a repository named `username.github.io`, or to any repository with Pages enabled. In GitHub, go to **Settings → Pages**, choose the branch/folder, and save.
