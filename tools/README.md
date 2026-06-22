# Tools

Shared scripts and utilities.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac
pip install -r tools/requirements.txt
```

## Scripts

| Script | Purpose |
|--------|---------|
| `render_schematics.py` | Discovers and renders all `docs/**/schematics/*.py` → SVG |

## Rendering Schematics

```bash
python tools/render_schematics.py
```

This finds all `.py` files in any `schematics/` folder under `docs/` and runs them. Each script outputs an SVG alongside itself.

A GitHub Actions workflow auto-renders and commits SVGs when schematic source files change.

## Adding a New Schematic

1. Create a `.py` file in the relevant `docs/<section>/schematics/` folder
2. Script outputs SVG to the same directory (use `Path(__file__).resolve().parent`)
3. Reference it in markdown: `![description](schematics/<name>.svg)`
4. Push — the workflow renders and commits the SVG automatically
