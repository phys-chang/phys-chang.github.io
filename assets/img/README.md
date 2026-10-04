# Images

Place the real headshot and any research figures here, then update the image paths in `index.html` if needed.

`lindbladian-tebd.png` is the methodology figure used in `../../notes.html` and previewed on the homepage. It was created with the built-in Imagegen tool using Chang Shu's two slides as a scientific reference, then edited to remove the large title from the image. The generation and edit prompts are saved in `lindbladian-tebd.prompt.txt`.

The figure uses the generator convention ∂t|ρ⟩⟩ = 𝓛|ρ⟩⟩, so the channel is 𝓔(Δt) = exp(Δt 𝓛). It illustrates vectorization, an MPS representation, alternating local gates, and SVD truncation; it is a schematic rather than simulation output. Method reference: [Zwolak & Vidal (2004)](https://arxiv.org/abs/cond-mat/0406440).

`quantum-trajectories.png` is the second methodology illustration in `../../notes.html`. It was created with the built-in Imagegen tool, using the title-free TEBD image as the style reference. The prompt is saved in `quantum-trajectories.prompt.txt`. Its scientific source is [Section IV of the DQPT supplement](https://arxiv.org/pdf/2509.03570v2#page=13), Eqs. (50)-(57) and the numerical steps that follow. It shows discrete-time no-jump/jump sampling, normalization, and the average of pure-state projectors. The depicted histories are schematic, not simulation data.

## Shared figure style

Use the title-free `lindbladian-tebd.png` as the visual reference for every new figure in this series.

- Match the landscape 16:9 framing, margins, white and ice-blue background, and navy serif typography.
- Use blue outlines and pale-blue fills for states, sage-green operators, and small gold arrows or jump markers. Match line widths, corner radii, and subtle shadows.
- Keep numbered panel badges, thin pale-blue separators, label sizes, and the bottom process strip consistent where the scientific narrative uses them.
- Use a modest descriptive subtitle; put the method or paper title in the webpage heading.
- Keep equations legible and scientifically grounded. Label schematic histories as such and use the actual data when displaying numerical results.
