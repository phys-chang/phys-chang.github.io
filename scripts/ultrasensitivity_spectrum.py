#!/usr/bin/env python3
"""Recompute the finite-cylinder spectra used in the ultrasensitivity story.

This is a 40 x 40 numerical illustration of Eq. (1) of arXiv:2409.13623,
not a digitization of its 60 x 60 Fig. 1. Dependencies: NumPy, SciPy,
threadpoolctl. Run from any directory; generated data live in assets/figures.

The hopping matrix is complex symmetric, H.T == H, not Hermitian:
the reverse hopping has the same complex coefficient, not its conjugate.
Open x boundaries and periodic y boundaries are implemented explicitly.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigvals
from scipy.spatial import cKDTree
from threadpoolctl import threadpool_limits


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "figures"
LX = LY = 40
IMPURITY = 0.01
TX, TY, TXY, U = 1j, 0.0, 3.0, -2j
PLOT_WIDTH, PLOT_HEIGHT = 550.0, 220.0
RE_LIMITS, IM_LIMITS = (-6.5, 6.5), (-4.2, 0.2)


def cylinder_hamiltonian(lx: int, ly: int) -> np.ndarray:
    """Site index x*ly+y; each undirected bond is added exactly once."""
    h = np.eye(lx * ly, dtype=complex) * U
    for x in range(lx):
        for y in range(ly):
            site = x * ly + y
            if TY:
                other = x * ly + (y + 1) % ly
                h[site, other] += TY
                h[other, site] += TY
            if x + 1 < lx:
                for yy, hopping in ((y, TX), ((y + 1) % ly, TXY)):
                    other = (x + 1) * ly + yy
                    h[site, other] += hopping
                    h[other, site] += hopping
    assert np.array_equal(h, h.T)
    return h


def clean_spectrum(lx: int, ly: int) -> np.ndarray:
    """Exact finite-size tridiagonal spectrum after Fourier transforming y."""
    ky = 2 * np.pi * np.arange(ly) / ly
    a = TX + TXY * np.exp(1j * ky)
    b = TX + TXY * np.exp(-1j * ky)
    standing_wave = np.cos(np.arange(1, lx + 1) * np.pi / (lx + 1))
    return (
        U
        + 2 * TY * np.cos(ky)[None, :]
        + 2 * standing_wave[:, None] * np.sqrt(a * b)[None, :]
    ).ravel()


def edge_green(energy: complex, lx: int, ly: int) -> tuple[complex, complex, complex]:
    """Analytic edge Green functions for two sites at y=0 on opposite edges.

    For each ky block, D_n is the determinant of its n-site tridiagonal
    E-H matrix. The inverse's diagonal and endpoint elements then follow
    from cofactors, without diagonalizing a nonnormal matrix.
    """
    ky = 2 * np.pi * np.arange(ly) / ly
    a = TX + TXY * np.exp(1j * ky)
    b = TX + TXY * np.exp(-1j * ky)
    z = energy - U - 2 * TY * np.cos(ky)
    previous = np.ones(ly, dtype=complex)
    current = z.copy()
    for _ in range(2, lx + 1):
        previous, current = current, z * current - a * b * previous
    diagonal = np.mean(previous / current)
    left_right = np.mean(a ** (lx - 1) / current)
    right_left = np.mean(b ** (lx - 1) / current)
    return diagonal, left_right, right_left


def nearest_distances(values: np.ndarray, reference: np.ndarray) -> np.ndarray:
    tree = cKDTree(np.column_stack((reference.real, reference.imag)))
    return tree.query(np.column_stack((values.real, values.imag)))[0]


def validate_model() -> dict[str, float]:
    """Independent finite-matrix checks, including Green-function cofactors."""
    lx, ly = 10, 12
    h = cylinder_hamiltonian(lx, ly)
    computed = eigvals(h, check_finite=False)
    exact = clean_spectrum(lx, ly)
    error = float(max(nearest_distances(computed, exact).max(), nearest_distances(exact, computed).max()))
    assert error < 1e-9, f"Finite-cylinder analytic spectrum mismatch: {error}"
    green_error = 0.0
    left, right = 0, (lx - 1) * ly
    for energy in (0.3 - 0.6j, 0.4 - 3.5j, 7.0 - 2j):
        inverse = np.linalg.inv(energy * np.eye(lx * ly) - h)
        predicted = edge_green(energy, lx, ly)
        measured = (inverse[left, left], inverse[left, right], inverse[right, left])
        green_error = max(green_error, max(abs(p - m) for p, m in zip(predicted, measured)))
    assert green_error < 1e-9, f"Edge Green function mismatch: {green_error}"
    return {"small_matrix_spectrum_max_error": error, "small_matrix_green_max_error": float(green_error)}


def write_coordinates(name: str, values: np.ndarray) -> str:
    """Coordinates in a 550 x 220 box, with y increasing down the page."""
    values = values[np.lexsort((values.imag, values.real))]
    x = (values.real - RE_LIMITS[0]) / (RE_LIMITS[1] - RE_LIMITS[0]) * PLOT_WIDTH
    y = (IM_LIMITS[1] - values.imag) / (IM_LIMITS[1] - IM_LIMITS[0]) * PLOT_HEIGHT
    assert np.all((x >= 0) & (x <= PLOT_WIDTH) & (y >= 0) & (y <= PLOT_HEIGHT))
    coords = [f"({xx:.5f},{yy:.5f})" for xx, yy in zip(x, y)]
    lines = [" ".join(coords[i:i + 8]) for i in range(0, len(coords), 8)]
    return "\\def\\" + name + "{%\n" + "\n".join(lines) + "\n}\n"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(limits=2):
        validation = validate_model()
        base = clean_spectrum(LX, LY)
        clean_h = cylinder_hamiltonian(LX, LY)
        # The exact clean spectrum avoids artificial eigenvalue motion caused
        # by a generic eigensolver's sensitivity on a nonnormal matrix.
        clean_numerical = eigvals(clean_h, check_finite=False)
        validation["full_matrix_clean_nearest_error"] = float(nearest_distances(clean_numerical, base).max())
        assert validation["full_matrix_clean_nearest_error"] < 1e-4
        one_h = clean_h.copy()
        one_h[0, 0] += IMPURITY
        one = eigvals(one_h, overwrite_a=True, check_finite=False)
        two_h = clean_h.copy()
        two_h[0, 0] += IMPURITY
        right = (LX - 1) * LY
        two_h[right, right] += IMPURITY
        two = eigvals(two_h, overwrite_a=True, check_finite=False)

    one_distances = nearest_distances(one, base)
    two_distances = nearest_distances(two, base)
    validation["one_impurity_max_nearest_distance"] = float(one_distances.max())
    validation["two_impurity_max_nearest_distance"] = float(two_distances.max())
    validation["two_impurity_eigenvalues_distance_above_0_15"] = int((two_distances > 0.15).sum())
    # Check induced states against the exact two-site resolvent determinant,
    # independently of the full matrix eigensolver.
    residuals = []
    for energy in two[two_distances > 0.15]:
        diagonal, left_right, right_left = edge_green(energy, LX, LY)
        residuals.append(abs((1 - IMPURITY * diagonal) ** 2 - IMPURITY ** 2 * left_right * right_left))
    validation["induced_state_max_secular_residual"] = float(max(residuals))
    assert validation["one_impurity_max_nearest_distance"] < 1e-3
    assert validation["two_impurity_max_nearest_distance"] > 0.5
    assert validation["induced_state_max_secular_residual"] < 1e-6

    metadata = {
        "source": "https://arxiv.org/abs/2409.13623",
        "description": "Independently recomputed finite-size illustration; not source-paper Fig. 1 data",
        "size": [LX, LY],
        "boundary_conditions": {"x": "open", "y": "periodic"},
        "parameters": {"tx": "i", "ty": "0", "txy": "3", "u": "-2i", "V": IMPURITY},
        "impurity_positions_zero_based": {"one": [[0, 0]], "two": [[0, 0], [LX - 1, 0]]},
        "plot": {"width": PLOT_WIDTH, "height": PLOT_HEIGHT, "real_limits": RE_LIMITS, "imaginary_limits": IM_LIMITS, "y_direction": "down"},
        "validation": validation,
    }
    (OUTPUT / "ultrasensitivity-spectrum-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    with (OUTPUT / "ultrasensitivity-spectrum-data.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["series", "real_E", "imaginary_E"])
        for name, values in (("clean", base), ("one", one), ("two", two)):
            for energy in values[np.lexsort((values.imag, values.real))]:
                writer.writerow([name, f"{energy.real:.12g}", f"{energy.imag:.12g}"])
    tex = "% Generated by scripts/ultrasensitivity_spectrum.py; do not hand edit.\n"
    tex += "% 40 x 40 cylinder, tx=i, ty=0, txy=3, u=-2i, V=0.01.\n"
    for name, values in (
        ("SpectrumCleanCoordinates", base),
        ("SpectrumOneCoordinates", one),
        ("SpectrumTwoCoordinates", two),
        ("SpectrumInducedCoordinates", two[two_distances > 0.15]),
    ):
        tex += write_coordinates(name, values)
    (OUTPUT / "ultrasensitivity-spectrum-data.tex").write_text(tex)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
