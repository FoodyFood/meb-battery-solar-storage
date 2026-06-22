"""CAN FD Bus Connection Diagram.

Output: docs/hardware/schematics/can-fd-bus.svg
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "can-fd-bus.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False) as d:
    d.config(unit=3)

    # ESP32
    d += elm.RBox(w=3, h=2).label("ESP32\nDevKitC V1")
    esp_out = d.elements[-1].E

    # SPI bus
    d += elm.Line().right(1.5).at(esp_out)
    d += elm.RBox(w=4, h=2).anchor("W").label("MCP2518FD\n(Controller +\nFD Transceiver)")
    mcp_out = d.elements[-1].E

    # SPI label
    d += elm.Label().at(esp_out).right(0.75).label("SPI", loc="top")

    # CAN H line
    d += elm.Line().right(1).at(mcp_out)
    canh_start = d.here
    d += elm.Line().right(3).label("CAN-H (Pin 17)", loc="top")
    canh_end = d.here

    # Slot C
    d += elm.RBox(w=3, h=2).anchor("W").label("Slot C\n→ BMS")

    # CAN L line (below)
    d += elm.Line().down(1.5).at(canh_start)
    canl_start = d.here
    d += elm.Line().right(3).label("CAN-L (Pin 11)", loc="bottom")
    canl_end = d.here
    d += elm.Line().up(1.5)

    # 120Ω termination (on MCP2518FD board)
    d += elm.Resistor().down().at(canh_start).label("120Ω\n(onboard)", loc="right")

print(f"Generated: {OUTPUT}")
