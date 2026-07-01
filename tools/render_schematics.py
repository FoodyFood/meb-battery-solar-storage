"""Render all circuit diagrams found in docs/**/schematics/*.py.

Usage: python tools/render_schematics.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    scripts = sorted(ROOT.glob("engineering/hardware/**/schematics/*.py"))

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
            print("OK")

    print(f"\n{len(scripts)} schematic(s), {errors} error(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
