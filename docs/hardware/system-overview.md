# System Overview

```mermaid
graph TD
    %% ===== POWER SUPPLY =====
    BENCH["🔌 12V Bench Supply"]:::power

    %% ===== CONTROL SUBSYSTEM =====
    BUCK["Buck Converter<br/>12V → 5V"]:::power
    ESP["ESP32-DevKitC V1<br/>(3.3V onboard reg)"]:::controller
    OLED["128×64 OLED"]:::controller

    %% ===== CAN FD (BATTERY) =====
    MCP["MCP2518FD Breakout<br/>(SPI + onboard FD transceiver)<br/>120Ω terminated"]:::canfd

    %% ===== CAN CLASSIC (FUTURE INVERTER) =====
    SN65["SN65HVD230<br/>(Classic CAN transceiver)"]:::can

    %% ===== HV PRE-CHARGE =====
    FUSE_IN["Fuse<br/>(12V input)"]:::safety
    DIGIPOT["X9C503S<br/>Digital Pot (50kΩ)"]:::precharge
    BOOST["DC-DC Boost Converter<br/>12V → 80–650V"]:::precharge
    BIAS["Bias Resistors<br/>(4× 140kΩ series)"]:::safety
    MOV["MOV / TVS<br/>(clamp ~420V)"]:::safety
    FUSE_OUT["Fuse<br/>(HV output)"]:::safety
    RELAY["Precharge Relay<br/>(GPIO 17)"]:::precharge

    %% ===== BATTERY =====
    SLOTC["Slot C Connector<br/>(2×11 dupont)"]:::battery
    PILOT["Pilot Line<br/>(Pin 16 ↔ 22 shorted)"]:::battery
    BMS["MEB Battery Pack<br/>82 kWh / 96S / ~370V"]:::battery
    HVCONN["HV Terminals<br/>(Motor inverter port)"]:::battery

    %% ===== FUTURE =====
    INV["Future Inverter<br/>(TBD)"]:::future

    %% ===== POWER CONNECTIONS =====
    BENCH -->|"12V"| BUCK
    BENCH -->|"12V"| FUSE_IN
    BENCH -->|"12V (Pin 3 + Pin 5)"| SLOTC
    BUCK -->|"5V VIN"| ESP
    FUSE_IN --> BOOST

    %% ===== SPI BUS =====
    ESP -->|"SPI: GPIO 32/33/35/25/34"| MCP

    %% ===== CAN FD BUS =====
    MCP -->|"CAN-H / CAN-L"| SLOTC

    %% ===== CAN CLASSIC =====
    ESP -->|"GPIO 26/27"| SN65
    SN65 -.->|"CAN-H / CAN-L<br/>(future)"| INV

    %% ===== DIGIPOT CONTROL =====
    ESP -->|"3× GPIO<br/>(INC, U/D, CS)"| DIGIPOT
    DIGIPOT -->|"Wiper out"| BOOST

    %% ===== PRECHARGE HV PATH =====
    BOOST --> BIAS
    BOOST --> MOV
    BOOST --> FUSE_OUT
    FUSE_OUT --> RELAY
    RELAY -->|"HV out"| HVCONN

    %% ===== BATTERY INTERNALS =====
    SLOTC --> BMS
    PILOT --- SLOTC
    BMS --- HVCONN

    %% ===== DISPLAY =====
    ESP -->|"I2C"| OLED

    %% ===== STYLES =====
    classDef power fill:#ff6b6b,stroke:#333,color:#fff
    classDef controller fill:#4ecdc4,stroke:#333,color:#fff
    classDef canfd fill:#5b7fff,stroke:#333,color:#fff
    classDef can fill:#2ecc71,stroke:#333,color:#fff
    classDef precharge fill:#f39c12,stroke:#333,color:#fff
    classDef battery fill:#9b59b6,stroke:#333,color:#fff
    classDef future fill:#95a5a6,stroke:#333,color:#fff,stroke-dasharray: 5 5
    classDef safety fill:#e74c3c,stroke:#333,color:#fff
```

## HV Pre-charge Circuit

The pre-charge protection circuit safely brings the battery's HV terminals to pack voltage before contactors close. Includes input/output fusing, bias resistors to prevent no-load voltage runaway, and a TVS diode to clamp overvoltage. The relay is controlled by Battery-Emulator (GPIO 17) and only energises the HV bus during the pre-charge sequence.

![HV Pre-charge Circuit](schematics/hv-precharge.svg)

**Safety components:**
- **Input fuse** — protects 12V supply and boost converter internals
- **Bias resistors** (4× 140kΩ in series across output) — prevents runaway voltage at no-load
- **MOV/TVS** (clamp ~420V) — caps output in case of digipot failure or control error
- **Output fuse** — protects relay and wiring if MOV/TVS fails short

## Colour Key

| Colour | Subsystem |
|--------|-----------|
| 🔴 Red | Power supply |
| 🟢 Teal | Controller (ESP32, display) |
| 🔵 Blue | CAN FD (battery comms) |
| 🟢 Green | Classic CAN (future inverter) |
| 🟠 Orange | Pre-charge HV control |
| 🟣 Purple | Battery / BMS |
| ⚪ Grey dashed | Future / TBD |
| 🔴 Dark Red | Safety (fuses, protection) |

## DSO Test Points

| Point | Signal | Where to probe |
|-------|--------|----------------|
| TP1 | CAN-H / CAN-L (FD) | Between MCP2518FD H/L and Slot C pins 17/11 |
| TP2 | SPI bus | GPIO 32 (MOSI), 35 (MISO), 33 (SCK) |
| TP3 | HV bus | Boost converter output / relay output |
| TP4 | Classic CAN | SN65HVD230 H/L (when inverter connected) |

## CAN FD Bus Connection

Physical layer wiring between the MCP2518FD breakout board and the MEB battery's Slot C connector. Shows CAN-H, CAN-L, and GND as separate signal lines with the 120 ohm termination resistor (onboard the MCP2518FD). This is where you probe with a DSO to verify bus integrity.

![CAN FD Bus](schematics/can-fd-bus.svg)

## Digital Potentiometer Control

The ESP32 drives an X9C503S digital potentiometer via 3 GPIO pins to set the boost converter's output voltage. This replaces the manual trim pot, enabling closed-loop voltage control — the ESP32 reads pack voltage from the BMS over CAN and adjusts the boost output to match before pre-charge.

![Digipot Control](schematics/digipot-control.svg)

## Startup & Contactor Close Sequence

```mermaid
sequenceDiagram
    participant ESP as ESP32 / Battery-Emulator
    participant BMS as MEB BMS
    participant BOOST as Boost Converter

    ESP->>BMS: Apply 12V (Pin 3 + Pin 5)
    ESP->>BMS: Start CAN FD messages (all intervals)
    BMS-->>ESP: BMS_20: Mode=7 (Init)
    BMS-->>ESP: BMS_20: Mode=0 (Standby), reports pack voltage
    ESP->>BOOST: Set digipot → target voltage
    ESP->>BOOST: Close precharge relay
    BOOST->>BMS: ~370V on HV terminals
    BMS-->>ESP: BMS_20: intermediate voltage rising
    Note over ESP,BMS: Delta < 20V
    ESP->>BMS: HVK_01: target=AC_CHARGING
    BMS-->>ESP: BMS_20: Mode=1 (HV Active)
    ESP->>BOOST: Open precharge relay
```
