# Solar MEB Battery - Project Rules

## Project Goal
Second-life integration of VW MEB battery packs for solar/home energy storage, with a path to a commercial installation product.

## Hardware Stack

### Main System
- **Battery:** Volkswagen MEB 82 kWh pack (~370V nominal, 96S NMC)
- **Controller:** ESP32-DevKitC V1 (dual-core, WiFi+BT)
- **CAN FD Interface:** MCP2518FD breakout (SPI, onboard FD transceiver, 120Ω termination)
- **Classic CAN (future inverter):** SN65HVD230 (3.3V, 1 Mbps — classic CAN only, NOT for battery)
- **Connector:** Slot C — standard 2x11 2.54mm dupont header
- **Display:** 128x64 OLED (included with ESP32 kit)
- **Pre-charge:** DC-DC boost converter (12V → 80–650V) + X9C503S digital potentiometer (50kΩ)
- **Power:** 12V bench supply → buck converter → 5V → ESP32 onboard reg → 3.3V

### Simulator
- **Controller:** ESP32-DevKitC V1 (second unit, identical to main)
- **CAN FD Interface:** MCP2518FD breakout (second unit, identical to main)
- **HV sensing:** Resistor divider (1.3MΩ + 10kΩ) on ESP32 ADC for closed-loop HV testing

## Key Constraints
- MEB battery requires external HV pre-charge (no internal pre-charge resistors)
- CAN FD is required (not classic CAN) — 500kbps arbitration, 2Mbps data phase
- Safety is paramount — high voltage system
- Pilot line (Slot C pins 16 ↔ 22) must be shorted for contactors to close
- Emergency stop: remove 12V from Slot C pin 5 (T30C)
- Non-isolated boost converter — HV- shares ground with 12V supply (verified approach by community)

## Conventions
- Research discoveries go in `research/` as individual focused markdown files
- Hardware diagrams: Mermaid for block diagrams/sequences, schemdraw for circuit schematics
- Schematics source (.py) and output (.svg) live in `engineering/<subsystem>/schematics/`
- Tests live next to what they test: `engineering/<subsystem>/tests/`
- Update `README.md` table of contents when adding new documents
- Keep notes concise and actionable

## Strategy
- Use Battery-Emulator **unmodified** for initial bring-up — no custom firmware yet
- Happy to fork or open a PR to Battery-Emulator if our changes are useful to others
- Our firmware work (if any) comes later once we understand the system end-to-end
- Keep DSO test points accessible for real-world validation (CAN H/L, SPI bus, HV bus)
- Research docs capture protocol knowledge so we *could* build our own implementation if needed

## Design Principles
- Follow spec-driven design: document the approach before implementing
- Clear ownership and boundaries between subsystems (HV, CAN, control logic)
- Single responsibility: each module/script/circuit does one thing well
- Units should be atomic to allow easy testing
- Do not start implementation until the design/spec has been reviewed
- All decisions made should be reflected consistently throughout the documentation

## Quality Standards
- Never degrade quality to work around a limitation — fix the limitation instead
- Only sacrifice quality with explicit user approval
- If a tool or approach isn't working properly, investigate root cause before changing approach
- Always test code changes locally before committing (use WSL for Python/scripts)
- Use WSL (not Windows cmd) for running Python, scripts, and build tools
- Test each piece as you proceed — add tests where applicable
- At the end of each task, re-run all existing tests to ensure nothing was broken
- At the end of each task, git commit so we can roll back one task at a time
- At the end of each task, provide a command to inspect/verify the result
- Combine shell commands where sensible to reduce manual steps

## Schemdraw Rules
- Use ASCII only in labels (no Unicode: no →, –, ×, Ω, −). Schemdraw's SVG text parser chokes on them.
- Use correct element types for components (DiodeTVS for TVS/MOV, Inductor2 for boost converters, Fuse for fuses, Switch for relays)
- Never use a Resistor symbol to represent a non-resistor component
- Use open dots (Dot(open=True)) for external connection terminals/pins
- Use absolute positioning with .at() for parallel branches to avoid overlapping paths
- Keep unit size >= 3.5 and add spacing (Line().right(0.5)) between dense components to prevent label overlap
- Place labels on the side with more whitespace (loc="left" or loc="right") to avoid collisions with adjacent elements
- Always render locally in WSL before committing: `python tools/render_schematics.py`

## Reference
- [Battery-Emulator by dala](https://github.com/dalathegreat/Battery-Emulator/) — used as-is for initial bring-up
