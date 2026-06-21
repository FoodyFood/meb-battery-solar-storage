# MEB Pre-charge Requirement

## Summary

The MEB battery has **NO internal pre-charge resistors**. It requires actual battery-level voltage to be present on the HV terminals before it will close contactors. This is fundamentally different from most EV packs.

In the car, the motor inverter generates this voltage from the 12V battery (boost). Outside the car, we need an **external high-voltage source**.

## Battery Pack (82 kWh)

- **Cells:** 96S (12 modules × 8s3p)
- **Nominal voltage:** ~370V
- **Max voltage:** ~403V (96 × 4.2V)
- **Min voltage:** ~288V (96 × 3.0V)
- **Module config:** 8s3p, ~33V per module

## What's Required

An external voltage source must put the **same voltage as the battery** (within a few volts) onto the HV terminals (motor inverter port). Only then will the BMS allow contactors to close via CAN command.

### Options for HV source:
- **Isolated boost converter** (e.g. HIA4V1) — boosts from low voltage to ~370V
- **Lab power supply** — capable of outputting 300–450V DC
- The Battery-Emulator project supports "automatic precharge" using a boost converter controlled by a relay

## Automatic Pre-charge in Battery-Emulator

Battery-Emulator has a built-in automatic precharge feature:
1. System activates a precharge relay that connects the HV boost converter to the battery terminals
2. Boost converter brings the external terminal voltage up to match pack voltage
3. BMS sees voltage within acceptable delta (few volts)
4. Battery-Emulator sends HVK_01 with contactor close request
5. BMS closes contactors
6. Precharge source can be disconnected (bus is now held by battery)

If precharge fails (cabling issue, etc.), BMS may log `P0C7800` (Precharge Time Too Long) which requires ODIS to clear.

## Important Notes

- The HV source connects to the **motor inverter port** (AC charger port is wired in parallel)
- The BMS measures voltage on its external terminals independently
- If the voltage delta is too large, contactors will NOT close — no error in ODIS, just won't work
- Once contactors are closed, the HV source sees near-zero current (battery holds the bus)

## Pilot Line Requirement

Pins **16** and **22** on Slot C must be connected (pilot line loop). Without this, contactors will not close.

> Note: Disconnecting pilot line while contactors are already closed only raises HVIL warning but does NOT open contactors. To emergency-stop, remove 12V from T30C (pin 5) instead.

## Hardware Needed

- HV boost converter (e.g. HIA4V1) capable of outputting pack voltage (~370V)
- Precharge relay (controlled by Battery-Emulator)
- HV wiring to motor inverter or AC charger port
- DC circuit breakers for safety

## Open Questions

- [ ] Source HIA4V1 or equivalent boost converter
- [ ] HV cable sizing (35–50mm² for inverter port, 6mm² for AC charger port)
- [ ] Emergency shutdown button design
- [ ] Confirm HIA4V1 controllability from Battery-Emulator relay output
