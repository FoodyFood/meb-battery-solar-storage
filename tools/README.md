# Tools

Shared scripts and utilities.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/WSL
pip install -r tools/requirements.txt
```

## Scripts

| Script | Purpose |
|--------|---------|
| `render_schematics.py` | Discovers and renders all `hardware/**/schematics/*.py` → SVG |

## Rendering Schematics

```bash
python tools/render_schematics.py
```

A GitHub Actions workflow auto-renders and commits SVGs when schematic source files change.

## Adding a New Schematic

1. Create a `.py` file in `hardware/schematics/` (or a subsection)
2. Output SVG to the same directory using `Path(__file__).resolve().parent`
3. Reference it in markdown: `![description](schematics/<name>.svg)`
4. Push — the workflow renders and commits the SVG automatically
