# MEB CAN FD Protocol

## Bus Configuration

| Parameter | Value |
|-----------|-------|
| Protocol | CAN FD with Bit Rate Switch (BRS) |
| Arbitration rate | 500 kbps |
| Data rate | 2 Mbps (4x arbitration) |
| MCP2518FD crystal | 40 MHz (default in Battery-Emulator) |

> ⚠️ **The SN65HVD230 transceiver maxes out at 1 Mbps.** It will NOT work for the 2 Mbps data phase. We need a CAN FD capable transceiver (MCP2542FD, TCAN1042, ATA6563, etc.)

## CAN Library

Battery-Emulator uses the [pierremolinaro ACAN2517FD](https://github.com/pierremolinaro/acan2517FD) Arduino library for ESP32 ↔ MCP2518FD communication over SPI.

## Messages Required for Contactor Closing

The BMS needs to see ALL of these messages at their correct intervals before it will close contactors:

### 10ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0xFC | ESC_51_Auth | 48-byte FD frame, CRC + counter |

### 20ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0xFD | ESP_21 | CRC + counter |

### 40ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0x40 | Airbag_01 | Byte 5 must be 0x00 (no HV deactivate). CRC + counter |

### 50ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0xC0 | EM1_01 | 32-byte FD. Contains external voltage at inverter (bytes 7-8). CRC + counter |

### 100ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0x503 | HVK_01 | **THE key contactor control message.** Contains HV request and target mode. CRC + counter |
| 0x3C0 | Klemmen_Status_01 | Terminal/ignition status. Byte 2 bit signals KL15 ON. CRC + counter |
| 0x3BE | Motor_14 | CRC + counter |
| 0x14C | Motor_54 | 32-byte FD. CRC + counter |
| 0x272 | HVLM_14 | Bidirectional charging / DC fast charge control |

### 200ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0x5E1 | Klima_Sensor_02 | Static |
| 0x153 | MSG_HYB_30 | Static |
| 0x1B0000B9 | NMH_DCDC_NV | Extended ID, NOT FD |
| 0x1B000010 | NMH_Gateway | Extended ID, NOT FD |
| 0x1B000046 | NMH_Klima | Extended ID, NOT FD |

### 500ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0x16A954B4 | eTM_01 | Extended ID, cooling valves/pumps |
| 0x569 | HVEM_04 | Battery heating requests |
| 0x1A55552B | Klima_EV_06 | Extended ID |
| 0x1A555548 | ORU_01 | Extended ID, OTA update message |
| 0x16A954FB | Standklima_01 | Extended ID |

### 1000ms interval
| CAN ID | Name | Notes |
|--------|------|-------|
| 0x641 | Motor_Code_01 | CRC + counter |
| 0x6B2 | Diagnose_01 | Contains date/time + odometer |
| 0x5F5 | Reichweite_01 | Loading profile, static |
| 0x585 | Systeminfo_01 | Static |
| 0x1A5555A6 | Temperaturen_01 | Extended ID, outside temp |

## HVK_01 (0x503) — Contactor Control

This is the critical frame. Key byte values:

| Byte | Purpose |
|------|---------|
| 0 | CRC |
| 1 | Counter (low nibble) + flags (high nibble). Bit 7 = precharge active. |
| 3 | BMS target mode |
| 5 | Bordnetz status (0x82 = active, 0x80 = inactive) |
| 6 | Emergency shutdown request |

### BMS Target Modes (byte 3)
| Value | Mode |
|-------|------|
| 0 | HV_OFF |
| 1 | HV_ON |
| 3 | AC_CHARGING_EXT (HS + AC_2 contactors) |
| 4 | AC_CHARGING (HS + AC contactors) — **used by Battery-Emulator** |
| 6 | DC_CHARGING (HS + DC contactors) |
| 7 | INIT |

## Pre-charge Logic (from Battery-Emulator)

The MEB battery has **NO internal pre-charge resistors**. An external HV source (e.g. HIA4V1 boost converter) must bring the motor inverter terminals to pack voltage.

Contactors are requested when ALL conditions are met:
1. No equipment stop active
2. BMS not in FAULT state
3. Either already in BMS_ACTIVE, OR:
   - BMS is in STANDBY
   - Pack voltage > 20V
   - Intermediate circuit voltage > 0V (external HV source is energising terminals)
   - Difference between pack voltage and intermediate circuit voltage < 20V

**Key takeaway:** We need an external boost converter to generate ~370V on the battery's HV terminals. The BMS measures this independently. Only when external voltage ≈ pack voltage will contactors close.

## BMS States (from BMS_20 frame, 0xCF)

| Mode | Meaning |
|------|---------|
| 0 | Standby — gates open, communication active |
| 1 | HV active — main contactors closed, normal operation |
| 2 | Balancing / extended DC fast charging |
| 3 | External charging |
| 4 | AC charging |
| 5 | ERROR |
| 6 | DC charging |
| 7 | Init |

## CRC Algorithm

VAG/VW uses AUTOSAR E2E CRC-8 with polynomial 0x2F:
- **Polynomial:** 0x2F
- **Initial value:** 0xFF
- **XOR output:** 0xFF
- **Counter-dependent magic byte** per CAN ID (lookup table, 16 values per ID)

Each message has:
- Byte 0 = CRC
- Byte 1 low nibble = rolling counter (0-15)

## UDS Polling (Diagnostic Requests)

Battery-Emulator polls BMS data via UDS ReadDataByIdentifier (0x22) over ISO-TP on CAN FD:

| Parameter | Request ID | Response ID |
|-----------|-----------|-------------|
| Request (physical) | 0x1C40007B | 0x1C42007B |
| TesterPresent | 0x1C40007B | — |

### Key PIDs
| PID | Data |
|-----|------|
| 0x028C | SOC |
| 0x1E3B | Voltage |
| 0x1E3D | Current |
| 0x1E0E | Max temperature |
| 0x1E0F | Min temperature |
| 0x5171 | Max charge voltage |
| 0x5170 | Min discharge voltage |
| 0x1E32 | Energy counters (charge/discharge kWh) |
| 0x1E1B | Allowed charge power |
| 0x1E1C | Allowed discharge power |
| 0x1E40–0x1EAB | Cell voltages (cells 1–108) |
| 0x1EAE–0x1EBF | Temperature points (1–18) |

## Cell Count Detection

The 82 kWh pack has **96 cells in series** (96S). Battery-Emulator auto-detects by polling cell 85, 97, and 108 — if 0xFFE is returned, that cell doesn't exist.

| Pack | Cells | Voltage range |
|------|-------|---------------|
| 48 kWh (ID.3 Pure) | 84S | 252–352.8V |
| 82 kWh (ID.3/4/5 Pro) | 96S | 288–403.2V |
| ~90 kWh (ID.Buzz/future) | 108S | 324–453.6V |

## Broadcast Messages FROM BMS

| CAN ID | Name | Interval | Key data |
|--------|------|----------|----------|
| 0xCF | BMS_20 | 10ms | Contactor status, mode, current, voltage, intermediate voltage |
| 0x2AF | BMS_05 | 50ms | Actual battery voltage, energy regen/extracted |
| 0x12DD54D0 | BMS_21 | 100ms | Max discharge/charge power and current limits |
| 0x12DD54D1 | BMS_22 | 100ms | SOC, usable energy, HV line status |
| 0x12DD54D2 | BMS_23 | 100ms | Heating, cooling requests |
| 0x578 | BMS_DC_01 | 100ms | DC charging status, voltage at charge port |
| 0x5A2 | BMS_04 | 500ms | Service disconnect, pilot line, capacity, error status |
| 0x5CA | BMS_07 | 500ms | Balancing request, diagnostic, temperature warning |
| 0x1A555550 | BMS_24 | 500ms | Balancing active, charging active, isolation resistance |
| 0x1A555551 | BMS_25 | 500ms | Thermal management (pumps, valves, temps) |
| 0x1A5555B0 | BMS_26 | 1000ms | Duration power limits, min/max voltage |
| 0x1A5555B1 | BMS_28 | 1000ms | Realtime warnings, serial number |
| 0x16A954E8 | BMS_CMC_04 | 180ms | Cell temperatures + cell voltages (multiplexed) |
| 0x16A954A6 | BMS_11 | — | Isolation, cell min/max voltage, temperatures |
| 0x17F0007B | KN_Hybrid_01 | 500ms | Component protection, transport mode, wake reason |

## Startup Sequence (Summary)

1. Apply 12V to Slot C pin 3 (permanent) and pin 5 (ignition-switched) → BMS wakes up
2. Start sending ALL required CAN messages at correct intervals
3. BMS responds on bus (BMS_20 mode = 7/Init, then transitions to 0/Standby)
4. Wait for BMS to report intermediate circuit voltage (from BMS_20)
5. Pre-charge the HV bus to within 20V of pack voltage
6. Set HVK_01 byte 3 = 0x04 (AC_CHARGING) and byte 5 = 0x82 (Bordnetz active)
7. BMS transitions to mode 1 (HV_ACTIVE) or mode 3/4 (charging) → contactors are closed
8. Maintain all CAN messages — if traffic stops for >500ms, BMS goes to DISCONNECTED

## Network Management (NMH frames)

Three NMH (Network Management High) frames are sent at 200ms, using classic CAN (NOT FD), with extended IDs:
- 0x1B000010 — Gateway
- 0x1B000046 — Klima
- 0x1B0000B9 — DC/DC converter

These may contain sleep/wake commands for the network.
