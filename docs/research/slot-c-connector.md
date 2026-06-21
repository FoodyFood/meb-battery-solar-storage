# MEB Slot C Connector

## Discovery

The Slot C connector (data/low voltage interface to the MEB battery) is a standard 2x11 2.54mm dupont header. No need to source an OEM loom or harvest from a donor vehicle — off-the-shelf dupont connectors work.

## Specs

- **Type:** 2x11 pin (22 pins total, but physical connector is 32-pin with some n.c.)
- **Pitch:** 2.54mm
- **Standard:** Generic dupont/header compatible

## Reference

![Slot C wiring](https://github.com/dalathegreat/Battery-Emulator/assets/166173233/36f68cae-005d-40f2-ab2d-bfe0b73af91b)

## Pinout

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | T31 | Ground (GND) |
| 2 | n.c. | Not connected |
| 3 | T30 | Permanent +12V |
| 4 | LVEP_VSent+5Vp_SUP | Voltage sense / 5V supply |
| 5 | T30c | Ignition-switched +12V |
| 6 | PVA_Valve2_COM | Valve 2 control |
| 7 | LVEP_HsdValve_SUP | Valve supply |
| 8 | PVA_CrashSignalIn_ANA | Crash signal input |
| 9 | n.c. | Not connected |
| 10 | PVA_CrashSignalOut_ANA | Crash signal output |
| 11 | PVA_EvCanL_COM | **CAN Low** |
| 12 | PVA_Ntc3_ANA | NTC temperature sensor 3 |
| 13 | n.c. | Not connected |
| 14 | PVA_PumpPwm_DIG | Coolant pump PWM |
| 15 | PVA_Ntc4_ANA | NTC temperature sensor 4 |
| 16 | PVA_PilotLineIn_ANA | Pilot line in |
| 17 | PVA_EvCanH_COM | **CAN High** |
| 18 | n.c. | Not connected |
| 19 | n.c. | Not connected |
| 20 | n.c. | Not connected |
| 21 | n.c. | Not connected |
| 22 | LVEP_PilotOut_ANA | Pilot line out |
| 23 | PVA_Ntc1_ANA | NTC temperature sensor 1 |
| 24 | n.c. | Not connected |
| 25 | n.c. | Not connected |
| 26 | PVA_Ntc2_ANA | NTC temperature sensor 2 |
| 27 | PVA_Valve1_COM | Valve 1 control |
| 28 | n.c. | Not connected |
| 29 | T31L_NTC_GND | Sensor ground |
| 30 | T31L_NTC_GND | Sensor ground |
| 31 | T31L_NTC_GND | Sensor ground |
| 32 | T31L_NTC_GND | Sensor ground |

## Key Pins for Our Use

- **Pin 1** — GND
- **Pin 3** — +12V permanent (powers BMS, ~21W draw)
- **Pin 5** — +12V ignition-switched / service-disconnect (KL30C — must be HIGH for operation, removing this opens contactors)
- **Pin 11** — CAN Low
- **Pin 17** — CAN High
- **Pin 16** — Pilot line IN — must be connected to pin 22
- **Pin 22** — Pilot line OUT — must be connected to pin 16

## Critical: Pilot Line

Pins 16 and 22 must be shorted together (pilot line loop). Without this connection, the BMS will NOT allow contactors to close.

## Wiring Notes (from dala wiki)

- AWG24 ethernet cable works well: one pair for CAN, one for pilot line, two pairs for 12V
- Two wires crimped together on pin 1 for GND
- 12V supply: 30W PSU sufficient (BMS draws ~21W)
- Single strand per signal works for cable runs **< 10m**. Longer runs cause voltage drop → contactors fail to close (no ODIS error, just silent failure)

## Connector Info

The original TE connector is restricted, but alternatives exist:
- **TE part:** `0-2315221-1` or `5-2315221-1`
- **VAG spare part:** `5Q0 973 733 A` (housing only, no pins)
- **Small pins** (0.5×0.4mm): `1-2177909-1`
- **Large pins** (1.2×0.6mm): `7-1452671-1`

Or just use standard 2.54mm dupont headers (our discovery).
