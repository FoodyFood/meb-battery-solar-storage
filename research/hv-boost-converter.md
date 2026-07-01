# HV Pre-charge Boost Converter

## Isolation Status

**The HIA4 module is NOT isolated** — confirmed. The onboard transformer is a coupled inductor, not an isolation barrier. Input ground and HV output ground are directly linked.

However, the Battery-Emulator community successfully uses the non-isolated HIA4V1 with MEB batteries on a shared ground. This works because the precharge voltage is applied *between* HV+ and HV- (the battery's own terminals), not between HV and chassis ground. The BMS isolation monitoring measures HV-to-chassis resistance, which remains intact.

**Our initially ordered (non-isolated) boost converter may work after all** — as long as:
- Output connects between the battery's HV+ and HV- terminals
- The converter's ground reference is the battery's HV- (which is also the system LV ground in this topology)

> ⚠️ This needs verification at the bench. If the BMS throws an isolation fault, we'll need to isolate the boost converter supply (e.g. dedicated battery pack for the boost converter, separate from the BMS 12V supply).

## Options (from Battery-Emulator community)

### Option A: TPS55288EVM-045 + XP Power G05 (Recommended)

The newer/safer approach, supported since Battery-Emulator firmware v10.11.0.

**Parts:**
- Texas Instruments TPS55288EVM-045 Evaluation Module
- XP Power (EMCO) G05 high voltage source
- Diode 1N4007
- Normally Closed contactor (decouples inverter during precharge)
- Fuse holder + 2A DC fuse (10×38)

### Option B: HIA4V1

Available on AliExpress. A 555-based oscillator driving a MOSFET + transformer.

> ⚠️ **CAUTION:** Multiple board versions exist with different output polarisation. People have **destroyed BMS units** due to overvoltage/wrong polarity. Test separately before connecting to battery.

**Critical requirements if using HIA4V1:**
- **Bias resistors:** 4× 140kΩ in series across HV output (prevents dangerously high voltage at no-load)
- **Verify polarity** before connecting to battery
- Use testmode in Battery-Emulator (no battery configured) to check output

The HIA4V1 can be directly controlled by the ESP32 via PWM (remove the 621 resistor, wire MOSFET gate to GPIO via 330Ω). Frequency controls output voltage:
- 23 kHz → ~370V
- 28 kHz → ~390V

## Overvoltage Protection

**TVS diodes (recommended by community):** 3× 5KP150A (150V) in series — clamps at ~470-480V. Unipolar versions also protect against reverse polarity.

> ⚠️ TVS diodes usually fail short and have 400A pulse rating. **Fuse protection is mandatory.**

**Alternative:** MOV rated for ~420V clamping. Simpler but less precise than TVS approach.

**Bias resistors:** 4× 140kΩ in series across HV output (prevents runaway voltage at no-load). Required for HIA4V1, good practice for any boost converter.

## Fusing

- **Input fuse (12V side):** Protects 12V supply and boost converter internals
- **Output fuse (HV side):** Protects relay and wiring if TVS/MOV fails short while relay is closed

Both are needed. The output fuse is especially important — even though current is low during normal precharge, a shorted protection device would see the full boost converter output through the relay.

## Digital Potentiometer Control (our addition)

- **X9C503S** (50kΩ, 100 steps, 3-wire interface)
- Replaces manual trim pot on boost converter
- ESP32 GPIO → X9C503S → controls output voltage

| Pin | Function | Notes |
|-----|----------|-------|
| INC | Increment | Pulse to step wiper position |
| U/D | Up/Down | HIGH = up, LOW = down |
| CS | Chip Select | LOW = active |

- 100 wiper positions, 500Ω per step
- Non-volatile — remembers last position on power loss

> Note: The digipot approach applies to the converter we ordered (resistor-controlled output). The HIA4V1 uses PWM frequency control instead, which Battery-Emulator can drive directly from GPIO.

## Control Strategy

1. Battery-Emulator reads pack voltage from BMS via CAN (BMS_20 frame)
2. Precharge voltage source adjusted to match pack voltage
3. Battery-Emulator activates precharge relay → HV source energises battery terminals
4. BMS sees external voltage ≈ pack voltage → allows contactor close
5. Precharge relay opens → HV source disconnected from bus

## Inverter Decoupling

During precharge, the inverter must be disconnected from the HV bus (otherwise it loads the precharge source and disrupts the sequence). This is done via a **Normally Closed HV contactor** (e.g. SEV100ADXL, 12V coil) that opens during precharge.

## Decision Needed

| Option | Pros | Cons |
|--------|------|------|
| TPS55288 + G05 | Newest, community supported, safer | More parts, higher cost |
| HIA4V1 | Single board, cheap, PWM controllable | Polarity risk, needs bias resistors, has destroyed BMS units |
| Our boost + X9C503S | Digitally controlled, fine resolution | Needs bench verification re: grounding |

## Open Questions

- [ ] Verify our boost converter works with shared ground (bench test before connecting to battery)
- [ ] If HIA4V1 route: verify polarity and add bias resistors before connecting to battery
- [ ] Confirm whether our X9C503S approach adds value over HIA4V1's PWM control
- [ ] Fuse rating for HV precharge circuit
- [ ] TVS diode / MOV selection and placement
