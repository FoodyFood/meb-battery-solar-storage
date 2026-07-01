"""Render all circuit diagrams found in engineering/**/schematics/*.py.

Usage: python tools/render_schematics.py
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def add_white_background(svg_path: Path):
    """Inject a white background rect into an SVG using its viewBox dimensions."""
    content = svg_path.read_text()
    match = re.search(r'viewBox="([^"]+)"', content)
    if match:
        x, y, w, h = match.group(1).split()
        bg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>'
        content = re.sub(r'(<svg[^>]*>)', r'\1' + bg, content, count=1)
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
