"""Test that all schematic scripts render successfully."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RENDER_SCRIPT = ROOT / "tools" / "render_schematics.py"


def test_render_schematics():
    """All schematic scripts should exit 0 and produce SVG files."""
    result = subprocess.run(
        [sys.executable, str(RENDER_SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Render failed:\n{result.stdout}\n{result.stderr}"


def test_svg_files_exist():
    """Each .py schematic should have a corresponding .svg."""
    schematic_scripts = list(ROOT.glob("engineering/hardware/**/schematics/*.py"))
    assert len(schematic_scripts) > 0, "No schematic scripts found"

    for script in schematic_scripts:
        svg = script.with_suffix(".svg")
        assert svg.exists(), f"Missing SVG for {script.name}: expected {svg}"


if __name__ == "__main__":
    test_render_schematics()
    test_svg_files_exist()
    print("All tests passed.")
