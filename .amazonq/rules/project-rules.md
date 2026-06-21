# Solar MEB Battery - Project Rules

## Project Goal
Second-life integration of VW MEB battery packs for solar/home energy storage.

## Hardware Stack
- **Battery:** Volkswagen MEB 82 kWh pack (~400V nominal)
- **Controller:** ESP32-DevKitC V1 (dual-core, WiFi+BT)
- **CAN FD Interface:** MCP2518FD breakout (SPI)
- **CAN Transceiver:** SN65HVD230 (3.3V, classic CAN — may need FD upgrade)
- **Connector:** Slot C — standard 2x11 2.54mm dupont header
- **Display:** 128x64 OLED (included with ESP32 kit)

## Key Constraints
- MEB battery requires pre-charge voltage on HV bus before contactors will close
- CAN FD is required (not classic CAN)
- Safety is paramount — high voltage system

## Conventions
- Research discoveries go in `docs/research/` as individual focused markdown files
- Hardware diagrams use draw.io (`.drawio.svg`) or mermaid in markdown
- Update `README.md` table of contents when adding new documents
- Keep notes concise and actionable

## Strategy
- Use Battery-Emulator **unmodified** for initial bring-up — no custom firmware yet
- Happy to fork or open a PR to Battery-Emulator if our changes are useful to others
- Our firmware work (if any) comes later once we understand the system end-to-end
- Keep DSO test points accessible for real-world validation (CAN H/L, SPI bus, HV bus)
- Research docs capture protocol knowledge so we *could* build our own implementation if needed

## Reference
- [Battery-Emulator by dala](https://github.com/dalathegreat/Battery-Emulator/) — used as-is for initial bring-up
