"""Digital Potentiometer Control Circuit Diagram.

Output: docs/hardware/schematics/digipot-control.svg
Compatible with schemdraw 0.23+

ESP32 controls X9C503S digital pot which sets boost converter output voltage.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements.intcircuits import Ic, IcPin
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "digipot-control.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False) as d:
    d.config(unit=4)

    # X9C503S IC
    ic = elm.Ic(
        size=(3, 4),
        pins=[
            IcPin(name='INC', side='left', slot='1/4', anchorname='inc'),
            IcPin(name='U/D', side='left', slot='2/4', anchorname='ud'),
            IcPin(name='CS', side='left', slot='3/4', anchorname='cs'),
            IcPin(name='VSS', side='left', slot='4/4', anchorname='vss'),
            IcPin(name='VCC', side='right', slot='1/4', anchorname='vcc'),
            IcPin(name='VH', side='right', slot='2/4', anchorname='vh'),
            IcPin(name='VW', side='right', slot='3/4', anchorname='vw'),
            IcPin(name='VL', side='right', slot='4/4', anchorname='vl'),
        ],
    ).at((6, 0)).label("X9C503S\n50k DigiPot", loc="top")

    # ESP32 GPIO connections (left side)
    elm.Line().at(ic.inc).left(3)
    elm.Dot(open=True).label("ESP32 GPIO (INC)", loc="left")

    elm.Line().at(ic.ud).left(3)
    elm.Dot(open=True).label("ESP32 GPIO (U/D)", loc="left")

    elm.Line().at(ic.cs).left(3)
    elm.Dot(open=True).label("ESP32 GPIO (CS)", loc="left")

    # VSS to ground
    elm.Line().at(ic.vss).left(2)
    elm.Ground()

    # VCC to 3.3V
    elm.Line().at(ic.vcc).right(2)
    elm.Dot(open=True).label("3.3V", loc="right")

    # VH (high terminal) to boost converter adj
    elm.Line().at(ic.vh).right(2)
    elm.Dot(open=True).label("Boost Adj (H)", loc="right")

    # VW (wiper) to boost converter adj
    elm.Line().at(ic.vw).right(2)
    elm.Dot(open=True).label("Boost Adj (W)", loc="right")

    # VL (low terminal) to ground
    elm.Line().at(ic.vl).right(2)
    elm.Ground()

print(f"Generated: {OUTPUT}")
