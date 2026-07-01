# Design Decisions

## 1. Use Battery-Emulator unmodified for initial bring-up

**Decision:** Run dala's Battery-Emulator firmware as-is. No custom firmware until the system is proven end-to-end.

**Rationale:**
- Battle-tested by the community on MEB batteries
- Handles the complex CAN FD protocol (25+ messages, CRC, timing, contactor sequencing)
- Web interface for monitoring and configuration
- Reduces variables during first power-on — if something fails, it's hardware/wiring, not code

## 2. ESP32-DevKitC V1 as controller

**Decision:** Standard ESP32-DevKitC V1 (30-pin, dual-core).

**Rationale:**
- Directly supported by Battery-Emulator with known pin mapping (`hw_devkit.h`)
- Cheap and widely available
- Sufficient SPI, GPIO, and CAN peripherals for our needs
- Spare GPIO available for custom additions (digipot control, relays, sensors)
- Onboard 3.3V regulator powers the MCP2518FD and transceiver
- WiFi for Battery-Emulator web interface
- Full customisation potential — we can extend Battery-Emulator or write our own firmware later

## 3. MCP2518FD breakout with onboard transceiver

**Decision:** All-in-one MCP2518FD board (controller + CAN FD transceiver, outputs H/L/G).

**Rationale:**
- MEB requires CAN FD at 500kbps arbitration / 2Mbps data — classic CAN transceivers cannot do this
- Single board simplifies wiring — SPI in, CAN bus out
- 120Ω termination resistor included
- ISO 11898-1:2015 compliant
- 40MHz crystal matches Battery-Emulator default configuration

## 4. SN65HVD230 reserved for future inverter (not battery)

**Decision:** Keep SN65HVD230 for classic CAN to the inverter. Do not use it for the battery.

**Rationale:**
- SN65HVD230 maxes out at 1Mbps — incompatible with MEB's 2Mbps data phase
- Most inverters use classic CAN (not FD), so SN65HVD230 is perfect for that role
- Keeps the two CAN buses independent (separate physical interfaces)

## 5. Digitally controlled boost converter for pre-charge

**Decision:** DC-DC boost converter (12V → 80–650V) with X9C503S digital potentiometer replacing the manual trim pot.

**Rationale:**
- MEB battery has NO internal pre-charge — requires external pack-level voltage on HV terminals
- Manual pot requires physical adjustment each time (impractical)
- X9C503S gives 100-step digital control via 3 GPIO pins
- Enables future closed-loop voltage tracking (read pack voltage from BMS via CAN, adjust output to match)
- Non-volatile memory — remembers last position on power cycle
- 50kΩ matches the boost converter's onboard pot (confirmed from listing)

## 6. 12V single-rail power architecture

**Decision:** Single 12V bench supply as the primary input. Buck converter to 5V for ESP32, onboard regulator for 3.3V.

**Rationale:**
- BMS requires 12V on Slot C pins 3 and 5 (~21W)
- Boost converter takes 12V input
- Minimises power supplies to one unit
- ESP32 onboard AMS1117 3.3V regulator has sufficient current for MCP2518FD + transceiver
- Separate buck converter for 5V keeps the ESP32 VIN clean

## 7. Standard dupont connectors for Slot C

**Decision:** Use off-the-shelf 2.54mm dupont headers instead of sourcing the OEM TE connector.

**Rationale:**
- Slot C is physically a standard 2.54mm pitch header
- No need to buy expensive OEM connector or harvest from donor loom
- Dupont jumpers allow quick prototyping and easy reconfiguration
- Can upgrade to proper TE connector later if permanent installation requires it

## 8. Pilot line hardwired (Pin 16 <-> 22)

**Decision:** Permanently short pins 16 and 22 on the Slot C connector.

**Rationale:**
- BMS requires closed pilot line loop to allow contactor closure
- No reason to leave it open in our application
- Emergency stop is achieved by removing 12V from pin 5 (T30C), not by breaking pilot line

## 9. Non-isolated boost converter with shared ground

**Decision:** Use a non-isolated boost converter. HV- shares the same ground reference as the 12V supply.

**Rationale:**
- The HIA4V1 (used successfully by the Battery-Emulator community) is also non-isolated
- The precharge voltage is applied between HV+ and HV- (the battery's own terminals)
- BMS isolation monitoring measures HV-to-chassis resistance, which remains intact because we connect across the battery terminals, not HV-to-chassis
- Simpler and cheaper than sourcing a truly isolated converter
- Needs bench verification — if BMS throws an isolation fault, fallback is a dedicated 12V battery for the boost converter
