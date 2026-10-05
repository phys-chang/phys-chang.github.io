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
        "quantum jumps shown as green vertical arrows.",
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
        2720,
        "Universal dynamical scaling of strong-to-weak symmetry breaking",
        "A large introductory visual story with three complementary views of "
        "SWSSB. In the pair-dephasing steady state, ordinary Z-spin measurements have zero "
        "correlation. Separate staggered cards labelled Shot 1, Shot 2 and Shot 3 "
        "show independent measurements of fresh copies of the same 1D state. "
        "A nonlinear two-copy overlap reveals long-range "
        "Renyi-2 order. A single X-basis spin flip changes the ensemble, while "
        "two distant flips preserve it. A local-learnability view contrasts "
        "unbroken strong symmetry and SWSSB using the same charge flip inside "
        "a local window: a product-state reference reveals the change locally, "
        "while the fully scrambled SWSSB state hides it from every proper patch. "
        "Global parity stays conserved. "
        "A vector waterfall of analytic Renyi-2 correlation profiles shows "
        "nonlinear order spreading across a chain even though ordinary Z-spin "
        "correlations stay zero in this example. A compact comparison shows "
        "exponential Z2 growth and algebraic U(1) growth, with near-ballistic "
        "finite filling and diffusive single-particle or single-hole limits.",
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
