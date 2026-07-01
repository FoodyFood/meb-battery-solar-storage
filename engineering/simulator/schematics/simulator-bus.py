"""Simulator CAN FD Bus Connection Diagram.

Shows the two ESP32 + MCP2518FD boards connected on the same CAN FD bus.

Output: engineering/simulator/schematics/simulator-bus.svg
Compatible with schemdraw 0.23+
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "simulator-bus.svg"

with schemdraw.Drawing(file=str(OUTPUT), show=False) as d:
    d.config(unit=4)

    # Main ESP32 (left)
    main_ic = elm.Ic(
        size=(3, 3),
        pins=[
            elm.IcPin(name='SPI', side='right', slot='1/3', anchorname='spi_main'),
            elm.IcPin(name='GPIO17', side='right', slot='2/3', anchorname='relay_main'),
            elm.IcPin(name='ADC', side='right', slot='3/3', anchorname='adc_main'),
        ],
    ).at((0, 0)).label("Main ESP32\n(Battery-Emulator)", loc="top")

    # Main MCP2518FD
    elm.Line().at(main_ic.spi_main).right(1.5)
    main_mcp = elm.Ic(
        size=(2, 2),
        pins=[
            elm.IcPin(name='SPI', side='left', slot='1/2', anchorname='spi_in'),
            elm.IcPin(name='H', side='right', slot='1/2', anchorname='canh'),
            elm.IcPin(name='L', side='right', slot='2/2', anchorname='canl'),
        ],
    ).label("MCP2518FD", loc="top")

    # CAN bus lines
    elm.Line().at(main_mcp.canh).right(2).label("CAN-H", loc="top")
    canh_mid = d.here
    elm.Line().right(2)
    canh_right = d.here

    elm.Line().at(main_mcp.canl).right(2).label("CAN-L", loc="bottom")
    canl_mid = d.here
    elm.Line().right(2)
    canl_right = d.here

    # Simulator MCP2518FD (right side)
    sim_mcp = elm.Ic(
        size=(2, 2),
        pins=[
            elm.IcPin(name='H', side='left', slot='1/2', anchorname='canh_s'),
            elm.IcPin(name='L', side='left', slot='2/2', anchorname='canl_s'),
            elm.IcPin(name='SPI', side='right', slot='1/2', anchorname='spi_out'),
        ],
    ).at(canh_right).label("MCP2518FD", loc="top")

    # Simulator ESP32 (far right)
    elm.Line().at(sim_mcp.spi_out).right(1.5)
    sim_ic = elm.Ic(
        size=(3, 3),
        pins=[
            elm.IcPin(name='SPI', side='left', slot='1/3', anchorname='spi_sim'),
            elm.IcPin(name='ADC', side='left', slot='2/3', anchorname='adc_sim'),
            elm.IcPin(name='WiFi', side='right', slot='1/3', anchorname='wifi'),
        ],
    ).label("Simulator ESP32\n(BMS Emulator)", loc="top")

    # ADC voltage divider annotation
    elm.Line().at(sim_ic.adc_sim).down(1)
    elm.Dot(open=True).label("HV divider\n(1.3M + 10k)", loc="right")

    # WiFi annotation
    elm.Line().at(sim_ic.wifi).right(1)
    elm.Dot(open=True).label("Web UI", loc="right")

print(f"Generated: {OUTPUT}")
