#!/usr/bin/env python3
"""Build standalone vector SVGs from the shared LaTeX/TikZ figure sources."""

from pathlib import Path
import argparse
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "figures"
DESTINATION = ROOT / "assets" / "img"
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

FIGURES = {
    "lindbladian-tebd": (
        1672,
        941,
        "Lindbladian TEBD",
        "Vectorize a density matrix, represent the doubled state as an MPS, "
        "and apply alternating local quantum-channel gates with SVD truncation.",
    ),
    "quantum-trajectories": (
        1672,
        941,
        "Monte Carlo wavefunction method",
        "Prepare independent pure-state trajectories, sample a no-jump or jump "
        "outcome at each time step, normalize, and average pure-state projectors. "
        "Probability labels are aligned over their corresponding outcomes. "
        "Schematic blue wavefunction paths evolve smoothly between abrupt "
        "quantum jumps shown as prominent warm red vertical arrows.",
    ),
    "open-system": (
        1672,
        360,
        "Spin chain with particle gain and loss",
        "A spin chain coupled to gain and loss channels, with operators "
        "square root of gamma g times sigma plus and square root of gamma l "
        "times sigma minus.",
    ),
    "swssb": (
        1672,
        4140,
        "Universal dynamical scaling of strong-to-weak symmetry breaking",
        "A large introductory visual story. Panel 00 explains strong and weak "
        "finite-state symmetry using framed X-basis mixture components. Strong "
        "symmetry has one fixed global parity charge; weak-only symmetry mixes "
        "different charge sectors without coherence between them. Strong symmetry "
        "also implies weak symmetry. Nonlinear SWSSB order can develop while a "
        "finite system stays in one fixed charge sector. "
        "Panel 01 explicitly separates global SWSSB, measured by whole-state "
        "nonlinear correlations, from local SWSSB, measured by fidelity in a local window. "
        "Prominent citation bands credit Lessa et al., PRX Quantum 6, 010344 (2025), "
        "for the global formulation and Divi, Lessa and Wang, arXiv:2605.28967, "
        "for the local formulation. Related references credit Carolyn Zhang, arXiv:2605.29113, "
        "for local fidelity diagnostics, and Tang, Kattel and J. H. Pixley, arXiv:2606.02713, "
        "for mean-field trajectory diagnostics. Jong Yeon Lee, arXiv:2605.05288, "
        "is cited for charge scrambling and its conditional relation to nonlinear SWSSB order. "
        "In the pair-dephasing steady state, ordinary Z-spin measurements have zero "
        "correlation. Separate staggered cards labelled Shot 1, Shot 2 and Shot 3 "
        "show independent measurements of fresh copies of the same 1D state. "
        "A nonlinear two-copy overlap reveals long-range "
        "Renyi-2 order. A single X-basis spin flip changes the ensemble, while "
        "two distant flips preserve it. A local-learnability view contrasts "
        "unbroken strong symmetry and SWSSB using the same charge flip inside "
        "a local window: a product-state reference reveals the change locally, "
        "while the fully scrambled SWSSB state hides it from every proper patch. "
        "A nested-set diagram for fidelity definitions places global SWSSB "
        "strictly inside local SWSSB. Locally thermal pure ETH states without "
        "ordinary symmetry breaking illustrate local order without global order. "
        "Global parity stays conserved in the pair-dephasing example. "
        "A vector waterfall of analytic Renyi-2 correlation profiles shows "
        "nonlinear order spreading across a chain even though ordinary Z-spin "
        "correlations stay zero in this example. A compact comparison shows "
        "exponential Z2 growth and algebraic U(1) growth, with near-ballistic "
        "finite filling and diffusive single-particle or single-hole limits.",
    ),
    "ultrasensitivity": (
        1672,
        2420,
        "Two tiny defects, one dramatic response",
        "A three-panel visual story based on Chang Shu, Kai Zhang and Kai Sun, "
        "arXiv:2409.13623. Panel 01 compares one weak local impurity with two "
        "distant weak impurities in a reciprocal non-Hermitian 2D cylinder, "
        "open along x and periodic along y. Computed complex-energy spectra "
        "show nearly unchanged energies with one defect and new branches with "
        "two. Panel 02 illustrates the two-way Green-function response, its "
        "round-trip product, and the geometry-dependent nonperturbative scale. "
        "Panel 03 shows an induced nonlocal channel and successive wavepacket "
        "returns, with a schematic log-norm decay profile showing repeated "
        "slow-decay passages. Response and wavepacket drawings are schematic; "
        "the spectrum points are a numerical reproduction of the paper's model.",
    ),
}


def command(arguments, directory, environment):
    result = subprocess.run(
        arguments,
        cwd=directory,
        env=environment,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(
            f"{arguments[0]} failed:\n{result.stdout[-6000:]}\n{result.stderr[-2000:]}"
        )


def build(name):
    width, height, title, description = FIGURES[name]
    with tempfile.TemporaryDirectory(prefix="changshu-vector-") as temporary:
        work = Path(temporary)
        environment = {
            **os.environ,
            "TEXMFVAR": str(work / "texmf-var"),
            "TEXMFCONFIG": str(work / "texmf-config"),
        }
        (work / "font-cache").mkdir()
        command(
            [
                "latex",
                "-no-shell-escape",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={work}",
                f"{name}.tex",
            ],
            SOURCE,
            environment,
        )
        output = work / f"{name}.svg"
        command(
            [
                "dvisvgm",
                "--no-fonts",
                "--bbox=papersize",
                "--exact-bbox",
                "--precision=5",
                f"--cache={work / 'font-cache'}",
                f"--output={output}",
                str(work / f"{name}.dvi"),
            ],
            SOURCE,
            environment,
        )
        root = ET.parse(output).getroot()
        # Convert every glyph to paths; reject bitmap or browser-only content.
        forbidden = {"image", "foreignObject", "script", "text"}
        assert all(
            node.tag.rsplit("}", 1)[-1] not in forbidden for node in root.iter()
        ), f"{name} contains non-vector content"
        for node in root.iter():
            for key, value in node.attrib.items():
                if key.rsplit("}", 1)[-1] == "href":
                    assert value.startswith("#"), f"External dependency in {name}"
        viewbox = [float(value) for value in root.attrib["viewBox"].split()]
        assert abs(viewbox[2] / viewbox[3] - width / height) < 0.002, (
            f"Unexpected canvas aspect ratio for {name}"
        )
        root.attrib.update(
            width=str(width),
            height=str(height),
            role="img",
            **{"aria-labelledby": "figure-title figure-description"},
        )
        root.insert(0, ET.Element(f"{{{SVG_NS}}}title", id="figure-title"))
        root[0].text = title
        root.insert(1, ET.Element(f"{{{SVG_NS}}}desc", id="figure-description"))
        root[1].text = description
        ET.register_namespace("", SVG_NS)
        ET.register_namespace("xlink", XLINK_NS)
        target = DESTINATION / f"{name}.svg"
        ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)
        print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes, vector paths")
    if name == "swssb":
        build_swssb_preview()
    elif name == "ultrasensitivity":
        build_ultrasensitivity_preview()


def build_swssb_preview():
    """Give panel 02 its own intrinsic viewport for the homepage preview."""
    root = ET.parse(DESTINATION / "swssb.svg").getroot()
    x, y, width, height = map(float, root.attrib["viewBox"].split())
    canvas_width, canvas_height = FIGURES["swssb"][:2]
    crop_top, crop_height = 2848, 941
    root.attrib.update(
        width=str(canvas_width),
        height=str(crop_height),
        viewBox=(
            f"{x:.5f} {y + crop_top * height / canvas_height:.5f} "
            f"{width:.5f} {crop_height * width / canvas_width:.5f}"
        ),
        overflow="hidden",
    )
    root.find(f"{{{SVG_NS}}}title").text = "Watch SWSSB nonlinear order spread"
    root.find(f"{{{SVG_NS}}}desc").text = (
        "Panel 02 of the SWSSB visual story. Blue analytic Renyi-2 profiles "
        "broaden with time, showing the spreading range of hidden order in "
        "the pair-dephasing example while ordinary Z-spin correlations remain zero."
    )
    target = DESTINATION / "swssb-spreading-preview.svg"
    ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)
    print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes, vector panel crop")


def build_ultrasensitivity_preview():
    """Export the spectrum comparison as a full-width homepage viewport."""
    root = ET.parse(DESTINATION / "ultrasensitivity.svg").getroot()
    x, y, width, height = map(float, root.attrib["viewBox"].split())
    canvas_width, canvas_height = FIGURES["ultrasensitivity"][:2]
    crop_height = 941
    root.attrib.update(
        width=str(canvas_width),
        height=str(crop_height),
        viewBox=f"{x:.5f} {y:.5f} {width:.5f} {crop_height * height / canvas_height:.5f}",
        overflow="hidden",
    )
    root.find(f"{{{SVG_NS}}}title").text = "One weak defect, or two?"
    root.find(f"{{{SVG_NS}}}desc").text = (
        "Panel 01 of the ultrasensitivity story. One weak defect barely shifts "
        "the computed complex-energy spectrum of a reciprocal 2D cylinder; "
        "two distant weak defects create separated spectral branches."
    )
    target = DESTINATION / "ultrasensitivity-preview.svg"
    ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)
    print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes, vector panel crop")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figures", nargs="*", choices=FIGURES, default=list(FIGURES))
    arguments = parser.parse_args()
    for tool in ("latex", "dvisvgm"):
        if not shutil.which(tool):
            parser.error(f"{tool} must be installed")
    for name in arguments.figures:
        build(name)


if __name__ == "__main__":
    main()
