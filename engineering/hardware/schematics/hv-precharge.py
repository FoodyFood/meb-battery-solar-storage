"""HV Pre-charge Protection Circuit Diagram.

Output: docs/hardware/schematics/hv-precharge.svg
Compatible with schemdraw 0.23+

Note: HV- and 12V ground are common (non-isolated boost converter).
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "hv-precharge.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False, transparent=False) as d:
    d.config(unit=3.5)

    # Input supply with ground
    elm.Ground()
    elm.SourceV().up().label("12V\nSupply")
    elm.Line().right()

    # Input fuse
    elm.Fuse().right().label("F1 (input)", loc="top")
    elm.Line().right(0.5)

    # Boost converter as inductor symbol
    elm.Inductor2().right().label("Boost Converter\n12V to 80-650V\n(non-isolated)\n[controlled by X9C503S]", loc="top")
    elm.Line().right(0.5)

    # Junction for parallel protection
    J = elm.Dot()
    junction = J.end

    # Main path: relay -> fuse (fuse after relay protects it) -> HV+
    elm.Line().right(0.5)
    elm.Switch(action='open').right().label("Precharge\nRelay", loc="top")
    elm.Line().right(0.5)
    elm.Fuse().right().label("F2 (output)", loc="top")
    elm.Line().right(1)
    elm.Dot(open=True).label("HV+", loc="right")

    # Common return rail (bottom) - connected to input ground
    elm.Line().at(junction).down(3.5)
    elm.Line().right(7.5)
    elm.Dot(open=True).label("HV-", loc="right")

    # Ground connection on return rail (same node as input ground)
    elm.Line().at(junction).down(3.5)
    elm.Line().left(4)
    elm.Ground()

    # Bias resistors (from junction down to return rail)
    elm.Line().at(junction).down(0.5)
    elm.Resistor().down(2.5).label("4x 140k\n(bias)", loc="left")

    # TVS diode (offset right, down to return rail)
    elm.Line().at(junction).right(3)
    elm.Line().down(0.5)
    elm.DiodeTVS().down(2.5).label("TVS\n420V clamp", loc="left")

print(f"Generated: {OUTPUT}")
