"""HV Pre-charge Protection Circuit Diagram.

Output: docs/hardware/schematics/hv-precharge.svg
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "hv-precharge.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False) as d:
    d.config(unit=3)

    # Input supply
    d += elm.SourceV().up().label("12V\nSupply").reverse()
    d += elm.Line().right()

    # Input fuse
    d += elm.Fuse().right().label("F1\n(input)")

    # Boost converter
    d += elm.Line().right(1)
    d += elm.RBox(w=4, h=2).anchor("W").label("Boost Converter\n12V → 80–650V")
    d += elm.Line().right(1).at(d.elements[-1].E)

    # Junction for parallel protection
    junction = d.here
    d += elm.Dot()

    # Main path: output fuse → relay → battery
    d += elm.Fuse().right().label("F2\n(output)")
    d += elm.Switch().right().label("Precharge\nRelay")
    d += elm.Line().right(1)
    d += elm.RBox(w=3, h=2).anchor("W").label("Battery\nHV Terminals\n~370V")
    end_top = d.here

    # Return path
    d += elm.Line().down(2).at(end_top)
    d += elm.Ground()

    # Bias resistors (parallel across output)
    d += elm.Line().down(0.5).at(junction)
    d += elm.Resistor().down().label("4× 140kΩ\n(bias)", loc="right")
    d += elm.Ground()

    # MOV/TVS (parallel across output)
    d += elm.Line().right(1.5).at(junction)
    d += elm.Line().down(0.5)
    d += elm.Varistor().down().label("MOV/TVS\n~420V", loc="right")
    d += elm.Ground()

    # Input ground
    d += elm.Ground().at(d.elements[0].start)

print(f"Generated: {OUTPUT}")
