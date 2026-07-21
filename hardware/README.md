# Hardware

## Overview

Documentation and specifications for the physical robot platform, including electronics, mechanical design, sensors, and assembly guides.

## Hardware Stack

### Main Controller
- **ESP32 DevKit-C v4/v1/v2**: Dual-core 240MHz processor, WiFi + BLE
- **RAM**: 520 KB internal, 4MB PSRAM (optional)
- **Flash**: 4MB or 16MB (depends on variant)
- **Power Input**: 5V USB or 4.2-5.5V direct

### Motor Driver
- **TB6612FNG**: Dual H-bridge motor driver
- **Rated Current**: 1.2A per channel max
- **Max PWM Frequency**: 100kHz
- **Voltage Range**: 2.2V to 13.5V

### Motors
- **Type**: 6V DC gear motors
- **Speed**: ~200 RPM (nominal)
- **Torque**: 0.8 Nm
- **Quantity**: 2 (one per wheel)

### Sensors

#### Line Following (IR Reflectance)
- **Sensor**: QTR-8RC reflectance sensor array
- **Channels**: 8
- **Range**: 3-6mm optimal
- **Frequency**: ADC at 500Hz

#### Obstacle Detection (Ultrasonic)
- **Sensor**: HC-SR04
- **Range**: 2cm - 4m
- **Accuracy**: ±3cm
- **Operating Frequency**: 40kHz

#### IMU (Optional)
- **Sensor**: MPU-6050
- **Accelerometer**: ±16g range
- **Gyroscope**: ±2000°/s range
- **I2C Interface**: 400kHz

### Servo
- **Type**: SG90 micro servo
- **Operating Voltage**: 4.8-6V
- **Torque**: 1.6kg@4.8V, 2kg@6V
- **Speed**: 0.12sec/60° at 5V
- **Purpose**: Gripper actuation

### Power Management
- **Battery**: 2S LiPo (7.4V nominal, 8.4V max)
- **Capacity**: 2200mAh recommended
- **BMS**: Integrated protection circuit
- **Charging**: USB via TP4056 module

### Communication
- **ESP-NOW**: Integrated in ESP32 WiFi
- **UDP**: Via WiFi module
- **GPIO-based**: UART debug interface

## Wiring Diagram

```
ESP32 DevKit-C
├── GPIO 14 → TB6612FNG IN1 (Motor A)
├── GPIO 12 → TB6612FNG IN2 (Motor A)
├── GPIO 27 → TB6612FNG IN3 (Motor B)
├── GPIO 26 → TB6612FNG IN4 (Motor B)
├── GPIO 25 → TB6612FNG PWM A
├── GPIO 33 → TB6612FNG PWM B
├── GND → TB6612FNG GND
├── VIN → TB6612FNG VM (Motor power)
├── GPIO 35 → QTR-8RC Analog (multiplexed)
├── GPIO 34 → HC-SR04 Echo
├── GPIO 32 → HC-SR04 Trigger
├── GPIO 19 → SG90 PWM
├── SDA (GPIO 21) → MPU-6050 SDA
└── SCL (GPIO 22) → MPU-6050 SCL

TB6612FNG
├── OUT1, OUT2 → Left Motor
├── OUT3, OUT4 → Right Motor
└── GND → Common ground (battery negative)

Battery (2S LiPo)
├── Positive → TP4056 IN / TB6612FNG VM
└── Negative → GND (common with ESP32)
```

## Bill of Materials (BOM)

| Component | Quantity | Unit Cost | Total | Notes |
|-----------|----------|-----------|-------|-------|
| ESP32 DevKit-C | 1 | $12 | $12 | Main controller |
| TB6612FNG | 1 | $3 | $3 | Motor driver |
| 6V DC Motor (200RPM) | 2 | $8 | $16 | With gearbox |
| SG90 Servo | 1 | $4 | $4 | Gripper actuator |
| HC-SR04 Ultrasonic | 1 | $2 | $2 | Obstacle detection |
| QTR-8RC Array | 1 | $15 | $15 | Line sensing |
| 2S LiPo Battery | 1 | $20 | $20 | 2200mAh recommended |
| TP4056 Charger | 1 | $2 | $2 | Battery charging |
| Jumper wires | 1 pack | $5 | $5 | Connectivity |
| PCB (perforated) | 1 | $3 | $3 | Component mounting |
| **Total** | | | **$82** | Per-unit cost |

## Assembly Guide

### Stage 1: Base Assembly
1. Mount motors to chassis using brackets
2. Attach wheels to motor shafts
3. Install casters for stability
4. Mount battery holder

### Stage 2: Electronics
1. Solder TB6612FNG to PCB
2. Install header pins for ESP32
3. Wire motor connections
4. Test motor control
5. Install servo on gripper fork

### Stage 3: Sensors
1. Mount QTR-8RC on underside
2. Mount HC-SR04 on front
3. Calibrate sensor thresholds
4. Test sensor readings

### Stage 4: Integration
1. Mount PCB on chassis
2. Connect battery
3. Upload firmware
4. Verify all systems

### Stage 5: Calibration
1. Perform motor speed calibration
2. Tune PID parameters
3. Calibrate IR sensor baseline
4. Test obstacle detection range

## Testing Procedures

See [Calibration Guide](../docs/guides/CALIBRATION.md) for detailed testing procedures.

## Mechanical Design Files

CAD files available in `cad/`: - `chassis.step` - Robot chassis
- `gripper_assembly.step` - Pick-place gripper
- `sensor_mounts.step` - Sensor mounting brackets

## Revision History

- **v1.0**: Initial hardware configuration (ESP32, TB6612FNG, SG90)
- **v1.1**: Added MPU-6050 IMU support
- **v2.0**: Planned: Upgraded motor to 12V variants

## Notes

- Ensure proper heatsinking of TB6612FNG at high duty cycles
- Use shielded cable for motor power lines (EMI reduction)
- Add 1µF bypass capacitors near all IC power pins
- Calibrate sensors after assembly
