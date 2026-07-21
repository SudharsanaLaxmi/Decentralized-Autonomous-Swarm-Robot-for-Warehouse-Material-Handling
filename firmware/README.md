# Firmware

## Overview

The firmware directory contains all embedded C++ code for the ESP32-based autonomous warehouse robot. This includes motor control, sensor interfacing, navigation algorithms, and communication protocols.

## Structure

```
firmware/
├── src/                      # Source code
│   ├── main.cpp              # Entry point
│   ├── config.h              # Configuration macros
│   ├── motor_controller/     # PWM-based motor control
│   ├── pid_controller/       # PID feedback control loops
│   ├── sensors/              # IR, ultrasonic sensor drivers
│   ├── navigation/           # Navigation and movement control
│   ├── servo/                # Gripper servo controller
│   ├── communication/        # ESP-NOW and UDP communication
│   └── utils/                # Logging, CRC, timing utilities
└── include/                  # Header files
```

## Building

### Prerequisites

- PlatformIO IDE or CLI
- Arduino core for ESP32
- Required libraries specified in `platformio.ini`

### Compile

```bash
platformio run
```

### Upload to ESP32

```bash
platformio run -t upload
```

### Serial Monitor

```bash
platformio device monitor --baud 115200
```

## Architecture

### Module Overview

| Module | Purpose | Interface |
|--------|---------|-----------|
| **MotorController** | PWM-driven differential drive | `setSpeed(left, right)` |
| **PIDController** | Feedback-based speed regulation | `update(target, actual)` |
| **Sensors** | IR line detection, ultrasonic ranging | Event callbacks |
| **Navigation** | Autonomous movement patterns | `moveForward()`, `avoidObstacle()` |
| **ServoController** | Gripper actuation | `grip()`, `release()` |
| **Communication** | ESP-NOW and UDP messaging | `sendMessage()`, `receive()` |

## Coding Standards

- **Language**: Modern C++ (C++17)
- **Style**: 2-space indentation
- **Documentation**: Doxygen-compatible comments
- **Testing**: Unit tests in separate mock environment

## Memory Management

- No dynamic allocation for real-time paths (use stack)
- Fixed-size buffers for communication
- RTOS task management via FreeRTOS (built-in to ESP32 Arduino)

## Configuration

Modify `firmware/src/config.h` for:
- GPIO pin assignments
- PID tuning parameters
- Motor speed limits
- Communication timeouts

## Debugging

Debug levels controlled via `DEBUG_LEVEL` macro:

- **0**: Production (minimal output)
- **1**: Warning level
- **2**: Standard debug
- **3**: Verbose (testing only)

## Future Enhancements

- [ ] Secure boot integration
- [ ] OTA firmware update mechanism
- [ ] Advanced RTOS task scheduling
- [ ] IMU-based stabilization
- [ ] Encrypted ESP-NOW messages
