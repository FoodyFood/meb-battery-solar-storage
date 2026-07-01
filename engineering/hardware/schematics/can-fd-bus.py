"""CAN FD Bus Connection Diagram.

Output: docs/hardware/schematics/can-fd-bus.svg
Compatible with schemdraw 0.23+
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "can-fd-bus.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False, transparent=False) as d:
    d.config(unit=4)

    # === CAN-H line (top) ===
    elm.Dot(open=True).label("MCP2518FD\nH", loc="left")
    elm.Line().right(5).label("CAN-H", loc="top")
    canh_mid = d.here
    elm.Line().right(5)
    elm.Dot(open=True).label("Slot C\nPin 17", loc="right")

    # === CAN-L line (bottom, parallel) ===
    elm.Dot(open=True).at((0, -3)).label("MCP2518FD\nL", loc="left")
    elm.Line().right(5).label("CAN-L", loc="bottom")
    canl_mid = d.here
    elm.Line().right(5)
    elm.Dot(open=True).label("Slot C\nPin 11", loc="right")

    # === 120 ohm termination (MCP2518FD end, onboard) ===
    elm.Resistor().at(canh_mid).down(3).label("120 ohm\n(onboard)", loc="right")

    # === GND line ===
    elm.Dot(open=True).at((0, -6)).label("MCP2518FD\nG", loc="left")
    elm.Line().right(10)
    elm.Dot(open=True).label("Slot C\nPin 1", loc="right")

print(f"Generated: {OUTPUT}")
