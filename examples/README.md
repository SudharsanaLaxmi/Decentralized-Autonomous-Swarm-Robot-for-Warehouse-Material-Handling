# Examples

## Overview

Practical code examples demonstrating core robot functionality. Each example is self-contained and progressively demonstrates more complex behaviors.

## Examples Structure

### 1. Basic Movement (`basic_movement/`)

**Goal**: Control robot locomotion

**Code**: `main.cpp`

**Demonstrates**:
- Motor initialization
- Speed control
- Direction control
- Emergency stop

### 2. Line Following (`line_following/`)

**Goal**: Autonomous line-following task

**Code**: `main.cpp`

**Demonstrates**:
- IR sensor array reading
- PID feedback control
- Real-time parameter tuning
- Sensor calibration

### 3. Pick-Place Operation (`pick_place/`)

**Goal**: Autonomous object pickup and placement

**Code**: `main.cpp`

**Demonstrates**:
- Gripper actuation
- Obstacle avoidance
- Position-based navigation
- Error recovery

## Running Examples

### Example 1: Basic Movement

1. **Upload firmware**:
   ```bash
   cd examples/basic_movement
   platformio run -t upload
   ```

2. **Serial monitor**:
   ```bash
   platformio device monitor --baud 115200
   ```

3. **Expected output**:
   ```
   [INFO] Motors initialized
   [INFO] Moving forward at 200/255 PWM
   [INFO] Rotating right at 150 RPM
   [INFO] Stop signal received
   ```

### Example 2: Line Following

1. **Prepare test track**: Black line on white background

2. **Upload and calibrate**:
   ```bash
   cd examples/line_following
   platformio run -t upload
   # Wait for calibration prompt
   # Place robot over white line
   # Press button to record baseline
   # Place robot over black line
   # Press button to record target
   ```

3. **Run test**:
   - Robot will follow the line autonomously
   - Monitor PID performance via serial

### Example 3: Pick-Place

1. **Setup environment**:
   - ArUco marker at pickup location
   - ArUco marker at dropoff location
   - Visual calibration reference

2. **Upload**:
   ```bash
   cd examples/pick_place
   platformio run -t upload
   ```

3. **Execute task**:
   - Robot navigates to pickup
   - Lowers gripper and closes
   - Navigates to dropoff
   - Opens gripper

## Dashboard Integration

### Visualizing Examples

Connect robot to dashboard for real-time telemetry:

```python
from vision.src.dashboard import WarehousesDashboard

dashboard = WarehouseDashboard(port=8888)
dashboard.start()
```

Navigate to `http://localhost:5000` for live view.

## Benchmark Reference

### Movement Performance

```
Speed: 0-200 RPM
Acceleration ramp: Configurable (100ms-1s)
Turning radius: 15cm (tunable)
Power consumption: 0.5-2A dependent on speed
```

### Line Following Performance

```
Max trackable speed: 1 m/s
Line width tolerance: 1-5cm
Sensor refresh rate: 100Hz
PID update rate: 50Hz
```

### Pick-Place Cycle Time

```
Navigate to pickup: 5-10s
Lower and grip: 1s
Navigate to dropoff: 5-10s
Lower and release: 1s
Total cycle time: 12-22s
```

## Customizing Examples

### Modify Motor Speeds

**File**: `examples/basic_movement/config.h`

```cpp
#define MAX_PWM 255
#define MIN_PWM 50
#define SPEED_STEP 10  // Increment speed by 10% each step
```

### Tune PID Parameters

**File**: `examples/line_following/config.h`

```cpp
#define PID_KP 0.5
#define PID_KI 0.0
#define PID_KD 0.2
#define PID_SETPOINT 0  // Center of array
```

### Adjust Gripper Servo

**File**: `examples/pick_place/gripper.cpp`

```cpp
constexpr int GRIP_POSITION = 40;    // Servo angle (degrees)
constexpr int RELEASE_POSITION = 0;
constexpr int GRIP_TIME_MS = 800;    // Hold time
```

## Troubleshooting

### Robot doesn't move

✓ Check power and connections
✓ Verify motor GPIO assignments
✓ Test motor driver with multimeter
✓ Check battery charge level

### Line following oscillates

✓ Reduce PID_KP (less aggressive)
✓ Increase PID_KD (more damping)
✓ Lower sensor polling rate
✓ Increase line width

### Gripper doesn't close

✓ Verify servo PWM pin
✓ Check servo power supply
✓ Adjust grip servo position
✓ Verify servo range limits

## Creating New Examples

Template for new example:

```cpp
#include <Arduino.h>
#include "../include/config.h"
#include "../src/motors/motor_controller.h"
#include "../src/communication/esp_now.h"

// Global objects
MotorController motors;
ESPNowClient espnow(ROBOT_ID);

void setup() {
    Serial.begin(115200);
    motors.initialize();
    espnow.initialize();
    Serial.println("[INFO] Setup complete");
}

void loop() {
    // Your example logic here
    delay(100);
}
```

## Performance Metrics

All examples include timing instrumentation:

```cpp
unsigned long start_time = micros();
// Operation
unsigned long duration = micros() - start_time;
Serial.printf("Operation took %lu µs\n", duration);
```

## Next Steps

- Explore individual modules in `firmware/src/`
- Examine vision module in `vision/src/`
- Review communication protocol in `communication/protocol/`
