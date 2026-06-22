# MEB BMS Simulator

An Arduino-based test harness that emulates the MEB battery's CAN FD responses, allowing full system testing without a real battery pack.

## Purpose

- Verify ESP32 + MCP2518FD SPI communication
- Confirm CAN FD bus electrical integrity (DSO probing)
- Test Battery-Emulator firmware configuration
- Validate the full contactor close sequence logic
- Test digipot voltage tracking behaviour
- De-risk integration before connecting to a real 400V battery

## Hardware

| Component | Role |
|-----------|------|
| Arduino (Uno/Nano/Mega) | Host controller |
| MCP2518FD breakout | CAN FD interface (same board as main system) |

Wiring: Arduino SPI → MCP2518FD → CAN-H/CAN-L ↔ ESP32's MCP2518FD

## What It Emulates

The simulator responds as if it were the MEB BMS:

### Broadcast frames (sent cyclically)
- `0xCF` (BMS_20, 10ms) — mode, contactor status, voltage, current, intermediate voltage
- `0x5A2` (BMS_04, 500ms) — capacity, pilot line status, error status
- `0x12DD54D1` (BMS_22, 100ms) — SOC, usable energy
- `0x12DD54D0` (BMS_21, 100ms) — charge/discharge power limits
- `0x17F0007B` (KN_Hybrid_01, 500ms) — wake status

### UDS responses
- Responds to polling on `0x1C42007B` with simulated cell voltages, temperatures, SOC

### Contactor sequence simulation
1. Start in mode 7 (Init)
2. Transition to mode 0 (Standby) after receiving valid CAN traffic
3. Report intermediate voltage rising (simulating precharge)
4. Transition to mode 1 (HV Active) when HVK_01 requests AC_CHARGING and voltage delta is acceptable

## Status

🚧 **Planned** — waiting on hardware (Arduino + second MCP2518FD board).

## Future
- Fault injection (simulate BMS errors, isolation faults, welded contactors)
- Configurable parameters (SOC, voltage, temperature) via serial interface
- Could be contributed back to Battery-Emulator community as a test tool
