# MCP2518FD - CAN FD Controller

## Selected Hardware

**MCP2518FD breakout board (complete with onboard CAN FD transceiver):**
- 40mm x 20mm x 12mm PCB
- 4x M2 mounting holes
- Handles both CAN FD and CAN 2.0B
- Arbitration up to 1 Mbps, data up to 8 Mbps
- 31 configurable FIFOs + TX queue
- ISO 11898-1:2015 compliant
- Outputs: H (CAN-H), L (CAN-L), G (GND) — connects directly to Slot C
- 120Ω termination resistor onboard

**CAN Transceiver (separate, for future inverter classic CAN):** SN65HVD230 (3.3V, 1 Mbps max)

> ✅ **Confirmed:** The MCP2518FD breakout has an onboard CAN FD transceiver (outputs H/L/G directly). The SN65HVD230 is NOT needed for the battery — it's reserved for future inverter classic CAN.

## SPI Pin Assignments (ESP32-DevKitC V1)

| Function | ESP32 GPIO | MCP2518FD Board Pin |
|----------|-----------|--------------------|
| SCK | 33 | SCK |
| MOSI | 32 | SDI |
| MISO | 35 | SDO |
| CS | 25 | CS |
| INT | 34 | INT |

## Connection

ESP32 → SPI (GPIOs 32/33/35/25/34) → MCP2518FD board → H/L/G → Slot C (Pin 17 CAN-H, Pin 11 CAN-L, Pin 1 GND)

Future inverter: ESP32 native CAN (GPIO 26 RX, GPIO 27 TX) → SN65HVD230 → Inverter CAN bus

## Open Questions

- [x] ~~Confirm MEB CAN FD data phase baud rate~~ — **Confirmed: 500kbps arb / 2Mbps data**
- [x] ~~SPI pin assignments on ESP32-DevKitC V1~~ — **Confirmed from hw_devkit.h**
- [x] ~~Does the MCP2518FD board include an onboard transceiver?~~ — **Yes, outputs H/L/G directly**
- [x] ~~Source a CAN FD transceiver~~ — **Not needed, onboard**
