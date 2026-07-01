# MEB Battery Solar Storage

Second-life integration of Volkswagen MEB battery packs (ID.3/ID.4/ID.5/ID.Buzz) for solar/home energy storage.

Inspired by [Battery-Emulator](https://github.com/dalathegreat/Battery-Emulator/) by dala.

## Why MEB?

- 82 kWh usable capacity from a single pack
- 96S NMC chemistry, ~370V nominal
- Well-documented CAN FD protocol (thanks to the Battery-Emulator community)
- Standard 2.54mm dupont connector for data/LV — no proprietary harness needed
- Quirks (external pre-charge, CAN FD requirement) deter casual buyers — making packs cheaper on the secondhand market

Most EV batteries have internal pre-charge resistors — you apply 12V, send the right CAN messages, and contactors close. MEB packs don't. They require actual pack-level voltage (~370V) on the HV terminals before the BMS will engage. This likely scares off some of the secondhand market, but it's a solvable problem with a boost converter and the right control logic.

## System Architecture

```mermaid
graph LR
    PSU["12V Supply"]:::power
    ESP["ESP32"]:::controller
    MCP["MCP2518FD<br/>(CAN FD)"]:::canfd
    BOOST["Boost Converter<br/>12V → ~370V"]:::precharge
    BAT["MEB Battery<br/>82 kWh"]:::battery
    INV["Inverter<br/>(TBD)"]:::future

    PSU --> ESP
    PSU --> BOOST
    PSU -->|"Pin 3+5"| BAT
    ESP -->|"SPI"| MCP
    MCP -->|"CAN FD"| BAT
    BOOST -->|"HV precharge"| BAT
    BAT -.->|"HV bus"| INV

    classDef power fill:#ff6b6b,stroke:#333,color:#fff
    classDef controller fill:#4ecdc4,stroke:#333,color:#fff
    classDef canfd fill:#5b7fff,stroke:#333,color:#fff
    classDef precharge fill:#f39c12,stroke:#333,color:#fff
    classDef battery fill:#9b59b6,stroke:#333,color:#fff
    classDef future fill:#95a5a6,stroke:#333,color:#fff,stroke-dasharray: 5 5
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full phase breakdown from POC to commercial product.

## Repository Structure

```
product/             # Commercial product — roadmap, certification, commissioning
hardware/            # Wiring diagrams, schematics, component specs
research/            # MEB CAN protocol, BMS behaviour, component research
design/              # Technical design decisions
simulator/           # Arduino BMS emulator for testing without a real battery
firmware/            # ESP32 / Battery-Emulator code
tools/               # Dev utilities (schematic rendering)
tests/               # Automated tests
```

## Hardware Stack

| Component | Role |
|-----------|------|
| ESP32-DevKitC V1 | Main controller (runs Battery-Emulator) |
| MCP2518FD breakout | CAN FD interface to battery (SPI, onboard transceiver) |
| SN65HVD230 | Classic CAN for future inverter |
| DC-DC boost converter | Pre-charge HV bus to ~370V |
| X9C503S digital pot | Digitally controls boost converter output voltage |
| 12V bench supply | Powers BMS, ESP32, boost converter |

## Documentation

### Product
- [Roadmap](ROADMAP.md) — Phase breakdown from POC to commercial installation
- [product/](product/) — Certification, commissioning, battery assessment

### Hardware
- [System Overview](hardware/system-overview.md) — Wiring diagrams and schematics

### Research
- [Slot C Connector](research/slot-c-connector.md) — Data/LV connector (2x11 dupont)
- [Pre-charge Requirement](research/precharge-requirement.md) — Contactor enable conditions
- [MCP2518FD](research/mcp2518fd.md) — SPI to CAN FD controller
- [MEB CAN Protocol](research/meb-can-protocol.md) — Full protocol reference (IDs, timing, CRC, startup sequence)
- [HV Boost Converter](research/hv-boost-converter.md) — Pre-charge voltage source (digitally controlled)

### Design
- [Design Decisions](design/design-decisions.md) — Key choices and rationale

### Simulator
- [BMS Simulator](simulator/README.md) — Arduino test harness for pre-battery testing

## Status

🚧 **Research & planning complete** — waiting on hardware delivery.

- [x] MEB CAN FD protocol fully documented (IDs, timing, CRC, contactor sequence)
- [x] Slot C pinout mapped
- [x] Pre-charge requirement understood (external HV source needed)
- [x] Hardware selected and ordered
- [x] Wiring diagram and schematics created
- [x] BMS simulator planned
- [ ] Flash Battery-Emulator onto ESP32
- [ ] First power-on with battery
- [ ] Contactor close achieved
- [ ] Inverter integration
