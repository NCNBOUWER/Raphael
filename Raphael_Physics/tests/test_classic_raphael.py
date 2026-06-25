import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Raphael_Runner import run_all
from natural_phenomena.fractal_expansion import generate_fractal_3d, mandelbrot_escape_counts
from natural_phenomena.time_dynamics import cosmic_expansion, evolve_quantum_state
from Simulations.simulation_controller import run_simulation


def test_fractal_generation():
    x, y, z = generate_fractal_3d(levels=4, num_points=101, seed=11)
    assert len(x) == len(y) == len(z) == 101
    assert all(-1 <= v <= 1 for v in x + y + z)


def test_mandelbrot_grid():
    grid = mandelbrot_escape_counts(8, 6, zoom=1.0, max_iter=20)
    assert len(grid) == 6
    assert len(grid[0]) == 8


def test_time_dynamics():
    x, y, z, density = evolve_quantum_state(time_step=5, num_points=50)
    assert len(density) == 50
    cx, cy, cz, scale = cosmic_expansion(time_step=5, num_points=50)
    assert scale > 1.0
    assert len(cx) == 50


def test_controller_and_runner():
    assert run_simulation("atomic", num_points=32)["points"] == 32
    report = run_all()
    assert set(report.keys()) == {"atomic", "cosmic", "quantum", "feedback", "helium_surrogate"}
    assert report["helium_surrogate"]["Total Energy"] > 0


if __name__ == "__main__":
    test_fractal_generation()
    test_mandelbrot_grid()
    test_time_dynamics()
    test_controller_and_runner()
    print("all classic Raphael validation tests passed")
