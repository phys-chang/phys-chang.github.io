# Chang Shu — personal homepage

A clean static academic homepage designed for GitHub Pages. The layout is inspired by Ethan Lake's spare academic homepage style: large centered title, thin pale-blue rules, simple navigation, concise intro text, and list-based notes / papers.

The research narrative is written with **open quantum systems** and **many-body dynamics** as the current focus, while **non-Hermitian physics** appears as a set of spectral and boundary-sensitive tools. The visual system is deliberately line-based rather than card-based, with a pale-blue palette.

## Files

- `index.html` — homepage
- `publications.html` — selected publications with topic filters
- `papers.html` — redirect alias to `publications.html`
- `notes.html` — placeholder notes page
- `styles.css` — typography, layout, responsive styling; pale-blue palette with line separators rather than boxed cards
- `script.js` — topic filter and dynamic footer year
- `publications.bib` — BibTeX entries for selected papers
- `assets/portrait-placeholder.svg` — replace with a real portrait when ready
- `assets/open-system-placeholder.svg` — replace with a spectrum, phase diagram, or dynamics sketch
- `notes/README.md` — placeholder for future PDFs, HTML notes, and notebooks
- `.nojekyll` — keeps GitHub Pages from running Jekyll

## Customize

1. Replace `assets/portrait-placeholder.svg` with your headshot, for example `assets/headshot.jpg`.
2. In `index.html`, update the `<img>` path to `assets/headshot.jpg`.
3. Replace the placeholder GitHub link with your GitHub profile.
4. Add PDFs, HTML notes, or Mathematica notebooks under `notes/` and link them from `notes.html`.
5. Keep publication metadata current by copying entries from arXiv or Google Scholar.

## Deploy on GitHub Pages

Upload these files to a repository named `username.github.io`, or to any repository with Pages enabled. In GitHub, go to **Settings → Pages**, choose the branch/folder, and save.
