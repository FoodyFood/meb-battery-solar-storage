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

## Closed-loop HV Testing

The simulator can also verify the precharge voltage control loop without a real battery:

1. ESP32 sets digipot → boost converter outputs target voltage
2. Arduino reads actual HV output via resistor divider (e.g. 1.3M + 10k → 130:1 ratio, maps 0-650V to 0-5V ADC)
3. Arduino reports the measured voltage over CAN FD as the BMS intermediate circuit voltage
4. Battery-Emulator sees voltage approaching "pack voltage" and requests contactor close
5. Arduino simulates contactor close (mode transition)

This tests the entire precharge loop end-to-end without a real 400V battery.

## Parametric Testing

With the closed-loop setup, automated test sweeps become possible:

- **Voltage calibration** — step digipot through all 100 positions, record ADC reading at each. Builds the lookup table.
- **SOC tracking** — simulator reports varying pack voltages, verify ESP32 adjusts boost output to match.
- **Precharge timing** — measure relay-close to voltage-at-target response curve.
- **Fault injection** — simulate failed boost (voltage not rising), verify timeout and error handling.
- **Boundary conditions** — test at min/max voltage, at the 20V delta threshold, at exact crossing.

All automated, repeatable, no real battery required.

## Status

🚧 **Planned** — waiting on hardware (Arduino + second MCP2518FD board).

## Future
- Fault injection (simulate BMS errors, isolation faults, welded contactors)
- Configurable parameters (SOC, voltage, temperature) via serial interface
- Could be contributed back to Battery-Emulator community as a test tool
