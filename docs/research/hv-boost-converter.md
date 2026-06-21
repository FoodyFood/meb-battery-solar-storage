# HV Pre-charge Boost Converter

## Hardware

- **Boost converter:** DC-DC 12V/24V input → 80–650V output, linear adjustable
- **Digital potentiometer:** X9C503S (50kΩ, 100 steps, 3-wire interface)
- **Control:** ESP32 GPIO → X9C503S → replaces manual trim pot on boost converter

## X9C503S Interface

| Pin | Function | Notes |
|-----|----------|-------|
| INC | Increment | Pulse to step wiper position |
| U/D | Up/Down | HIGH = up (more resistance), LOW = down |
| CS | Chip Select | LOW = active |

- 100 wiper positions
- 50kΩ total → 500Ω per step
- Non-volatile — remembers last position on power loss

## Control Strategy

1. Battery-Emulator reads pack voltage from BMS via CAN (BMS_20 frame)
2. ESP32 adjusts X9C503S to set boost converter output ≈ pack voltage
3. Battery-Emulator activates precharge relay → boost converter energises HV bus
4. BMS sees external voltage ≈ pack voltage → allows contactor close
5. Precharge relay opens → boost converter disconnected from bus

## Calibration Needed

- [ ] Measure boost converter output voltage vs. potentiometer resistance
- [ ] Build lookup table: pack voltage → wiper position
- [ ] Determine if relationship is linear or needs curve fitting
- [ ] Verify digipot resistance range matches the boost converter's adjustment range

## Safety Notes

- Boost converter is only energised via relay — not always live
- Once contactors close, boost converter is disconnected (zero current through it)
- ESP32 must NOT adjust digipot while boost converter is live under load
- HV side is fully isolated from LV control side (isolated boost topology)

## Open Questions

- [ ] What resistance range does the boost converter's trim pot use? (Need to verify 50kΩ digipot is correct match)
- [ ] Input voltage selection: 12V or 24V? (12V keeps power supply simple)
- [ ] Maximum bus capacitance the boost converter needs to charge (determines inrush current / startup time)
