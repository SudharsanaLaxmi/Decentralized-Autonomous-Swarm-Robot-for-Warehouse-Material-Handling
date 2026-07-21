"""
Hardware Electrical Configuration

Detailed electrical schematic and GPIO mapping reference.
"""

# Hardware Electrical Configuration

Complete electrical reference for the Autonomous Warehouse Robot.

## System Overview

```
┌─────────────────────────────────────────────────┐
│               ESP32 DevKit-C v4                 │
│            (240 MHz dual-core MCU)              │
│                                                 │
│  Power: 5V USB or 5-7V external              │
│  Pins: 38 GPIO (11 ADC, 8 DAC, etc.)          │
└────┬────────────────────────────────────────┬───┘
     │                                        │
     ├──Motor Driver (TB6612FNG)              │
     │  ├── PWM control                       │
     │  └── Direction control                 │
     │                                        │
     ├──Sensor Multiplexer (HC4051)           │
     │  └── Line sensor signal routing        │
     │                                        │
     ├──Servo Controller (PWM direct)         │
     │                                        │
     └──ADC Inputs                            │
        ├── Battery voltage (GPIO35)          │
        └── Temperature sensor (GPIO34)       │
```

---

## GPIO Pin Mapping

### Motor Control

| Function | GPIO | Mode | Purpose |
|----------|------|------|---------|
| LEFT_PWM | 22 | Output | Motor A PWM (20kHz) |
| LEFT_DIR | 23 | Output | Motor A direction |
| RIGHT_PWM | 19 | Output | Motor B PWM (20kHz) |
| RIGHT_DIR | 21 | Output | Motor B direction |
| ENABLE | 25 | Output | Motor driver enable |

```
                      TB6612FNG
       ┌──────────────────┬──────────────────┐
GPIO22 │AIN1              │             VCC  │─── +5V
GPIO23 │AIN2              │             GND  │─── GND
GPIO19 │BIN1              │          STBY    │─── GPIO25
GPIO21 │BIN2              │                  │
       │                  │          PWMA    │─── GPIO22
       │                  │          PWMB    │─── GPIO19
       └──────────────────┴──────────────────┘
            ↓
     Motor A: [-----]  Motor B: [-----]
```

### Sensor Inputs

| Function | GPIO | ADC Ch | Purpose |
|----------|------|--------|---------|
| LINE_SENSOR | 35 | 7 | 8-channel multiplexed input |
| ULTRASONIC_TRIG | 2 | - | HC-SR04 trigger |
| ULTRASONIC_ECHO | 15 | - | HC-SR04 echo |
| SERVO_PWM | 32 | - | SG90 servo control |

### Optional Pins

| Function | GPIO | Purpose |
|----------|------|---------|
| MPU_SDA | 21 | I2C data (IMU) |
| MPU_SCL | 22 | I2C clock (IMU) |
| STATUS_LED | 2 | Debug indicator |

---

## Voltage Levels

### Main Power Rails

```
Battery (7.4V nominal)
    ↓
┌───────────────────────┐
│   Power Distribution  │
├───────────────────────┤
│ 5V Supply (USB/Ext)   │─→ ESP32, Sensors
│ 6V Supply (Motors)    │─→ Motor Driver VCC
│ 3.3V (Internal Reg)   │─→ GPIO Logic
└───────────────────────┘
```

### Current Requirements

| Device | Voltage | Current | Duration |
|--------|---------|---------|----------|
| ESP32 | 5V | 150mA avg | Continuous |
| Motor A | 6V | 300mA idle, 700mA peak | Variable |
| Motor B | 6V | 300mA idle, 700mA peak | Variable |
| Servo | 5V | 10mA idle, 100mA peak | On demand |
| Sensors | 5V, 3.3V | 50mA total | Continuous |
| **Total Peak** | - | **1.6A** | Movement |

### Voltage Divider for Battery Monitoring

GPIO35 measures battery voltage via voltage divider:

```
    Battery (0-8.4V)
        │
        ├─────[R1 100kΩ]─────┬─────── GND
        │                     │
        └─────[R2 100kΩ]─────┴─── GPIO35 (ADC)

Calibration: V_out = V_battery × (R2 / (R1 + R2))
          = V_battery × (100k / 200k)
          = V_battery × 0.5
```

**Configuration**:
```cpp
#define BATTERY_ADC_PIN 35
#define VOLTAGE_DIVIDER 2.0        // 100k + 100k divider
#define ADC_MAX_READING 4095
#define ADC_REF_VOLTAGE 3.3
#define CALIBRATION_OFFSET 0.0     // Adjust if needed
```

---

## PWM Configuration

### Motor PWM

```cpp
// PWM Parameters (from config.h)
#define PWM_FREQUENCY   20000  // 20 kHz (inaudible)
#define PWM_RESOLUTION  8      // 0-255 range
#define PWM_DUTY_MIN    0      // Min duty cycle
#define PWM_DUTY_MAX    255    // Max duty cycle

// ESP32 PWM Channel Mapping
// Motor Left (GPIO22):  ledcChannel(0, 20000, 8)
// Motor Right (GPIO19): ledcChannel(1, 20000, 8)
```

### Servo PWM

```cpp
// Servo requires ~50Hz (20ms period), 1-2ms pulse width
#define SERVO_PWM_FREQ  50     // 50 Hz
#define SERVO_PWM_MIN   1000   // 1ms (full reverse)
#define SERVO_PWM_MID   1500   // 1.5ms (center)
#define SERVO_PWM_MAX   2000   // 2ms (full forward)
```

---

## Communication Interfaces

### UART (Serial Debug)

```cpp
GPIO1 (TX) ──┐
GPIO3 (RX) ──┼─── RS232/USB Adapter
GND ─────────┘

Settings: 115200 baud, 8N1
Used for: Debug output, calibration, configuration
```

### I2C (Optional IMU)

```cpp
GPIO21 (SDA) ──┬─── MPU-6050
GPIO22 (SCL) ──┤
GND ───────────┴─── Common ground

Frequency: 400kHz (standard mode)
Pullups: 4.7kΩ to 3.3V (built-in)
```

### ESP-NOW (Wireless)

```cpp
// No external connections needed
// 2.4 GHz radio built into ESP32
// Range: 200-300m line-of-sight
// Latency: <50ms average
```

---

## Protection & Safety

### Motor Driver Protection

```
TB6612FNG features:
├─ Built-in overcurrent protection
├─ Thermal shutdown (>150°C)
└─ Low voltage cutoff (< 2.0V)

Recommended:
├─ 0.1µF decoupling cap on VCC
├─ Freewheel diodes on motor outputs (if needed)
└─ Series resistor on PWM (100Ω)
```

### Power Supply Protection

```
ESP32 accepts 5V from USB or external adapter.

Protection features:
├─ 500mA self-resetting fuse on USB
├─ Built-in 3.3V regulator (~600mA capacity)
└─ Reverse polarity protection NOT included

Warning: Be careful with power connections!
 - Reversed polarity → Permanent damage
 - Overvoltage (>7V on motors) → May damage motor driver
 - Overcurrent spike → May brown out ESP32
```

---

## Wiring Checklist

Complete this checklist when assembling:

### Power Distribution
- [ ] Battery connector soldered securely
- [ ] 5V USB regulated supply connected
- [ ] GND common to all modules
- [ ] No voltage spikes on scope (if available)

### Motor Control
- [ ] Motor A PWM on GPIO22
- [ ] Motor A DIR on GPIO23
- [ ] Motor B PWM on GPIO19
- [ ] Motor B DIR on GPIO21
- [ ] Motor driver VCC on 5-6V supply
- [ ] Motor driver GND common

### Sensor Inputs
- [ ] Line sensor ADC on GPIO35
- [ ] Ultrasonic trigger on GPIO2
- [ ] Ultrasonic echo on GPIO15
- [ ] Servo PWM on GPIO32
- [ ] All sensor GND connected

### Communication
- [ ] USB cable connected to ESP32 (optional for debug)
- [ ] Serial adapter configured for 115200 baud
- [ ] I2C pullups (if IMU installed)

### Safety
- [ ] No exposed wire leads
- [ ] All connections soldered (not twisted)
- [ ] Proper strain relief on power cables
- [ ] Battery disconnected when not in use

---

## Troubleshooting Electrical Issues

### Motor Won't Move

**Check list**:
1. [ ] Battery voltage above 6.5V
2. [ ] Motor enable pin (GPIO25) is HIGH
3. [ ] PWM signal present on GPIO22/19
4. [ ] Motor driver IC is cool (not hot)
5. [ ] No shorts between connector and GND

### Motors Spin Wrong Direction

**Solution**:
```cpp
// Swap direction GPIO lines
// Or invert in firmware:
#define INVERT_LEFT_MOTOR false
#define INVERT_RIGHT_MOTOR true
```

### ADC Reading Unstable

**Potential causes**:
- Loose sensor connections
- High impedance line (poor solder joint)
- Noise from PWM switching
- Solution: Add 0.1µF capacitor to ADC input

### ESP32 Resets Unexpectedly

**Check**:
- Power supply providing stable 5V
- Motor current spike not causing brown-out
- No shorts on GPIO lines
- Update firmware to latest version

---

## Design Files

- **Schematic**: See `hardware/electronics/schematic.pdf`
- **PCB Layout**: See `hardware/electronics/pcb-layout.kicad_pcb`
- **CAD Model**: See `cad/robot-chassis-v1.step`

---

## Further Reading

- [TB6612FNG Datasheet](https://www.sparkfun.com/datasheets/Components/TB6612FNG.pdf)
- [ESP32 Pinout Reference](https://github.com/espressif/esp-idf)
- [HC-SR04 Sensor Guide](https://www.electroschematics.com/hc-sr04-datasheet/)
- [PWM Motor Control Guide](../../docs/guides/PID_TUNING.md)
