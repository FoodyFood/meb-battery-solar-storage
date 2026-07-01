"""Render all circuit diagrams found in engineering/**/schematics/*.py.

Usage: python tools/render_schematics.py
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def add_white_background(svg_path: Path):
    """Inject a white background into an SVG via style on the root element."""
    content = svg_path.read_text()
    # Add background-color to the root svg element's style
    if 'style=' in content.split('>')[0]:
        content = re.sub(r'(<svg[^>]*style=")', r'\1background-color:white;', content, count=1)
    else:
        content = re.sub(r'(<svg)([^>]*>)', r'\1 style="background-color:white;"\2', content, count=1)
    svg_path.write_text(content)


def main():
    scripts = sorted(ROOT.glob("engineering/**/schematics/*.py"))

    if not scripts:
        print("No schematic scripts found.")
        return

    errors = 0
    for script in scripts:
        print(f"  {script.relative_to(ROOT)} ...", end=" ")
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FAIL\n    {result.stderr.strip()}")
            errors += 1
        else:
            svg = script.with_suffix(".svg")
            if svg.exists():
                add_white_background(svg)
            print("OK")

    print(f"\n{len(scripts)} schematic(s), {errors} error(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
