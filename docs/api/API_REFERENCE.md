"""
API Documentation Index

Complete API reference for all subsystems.
"""

# API Documentation

## Quick Navigation

- [Firmware API](#firmware-api)
- [Vision API](#vision-api)
- [Communication API](#communication-api)
- [Python Hardware Interface](#python-hardware-interface)

---

## Firmware API

### Core Modules

**MotorController**
- `initialize()` - Setup PWM and GPIO
- `setSpeed(left, right)` - Set speed for both motors
- `setSpeedRamped(left, right, duration_ms)` - Smooth acceleration
- `moveForward()` - Move forward
- `moveBackward()` - Move backward
- `rotateClockwise()` - Spin right
- `rotateCounterClockwise()` - Spin left
- `emergencyStop()` - Hard stop
- `getLeftSpeed()`, `getRightSpeed()` - Read current speeds

**PIDController**
- `update(error)` → float - Calculate control output
- `setGains(kp, ki, kd)` - Update PID coefficients
- `setOutputLimits(min, max)` - Clamp output range
- `setSetpoint(target)` - Set desired value
- `reset()` - Clear integrator and derivative history
- `getError()` - Current error value
- `getOutput()` - Last calculated output

**GPIO Configuration**
```cpp
// Motor pins (see config.h)
#define MOTOR_LEFT_PWM    PIO
#define MOTOR_LEFT_DIR    PIO
#define MOTOR_RIGHT_PWM   PIO
#define MOTOR_RIGHT_DIR   PIO

// Sensor pins
#define LINE_SENSOR_A0    IO
#define ULTRASONIC_TRIG   IO
#define ULTRASONIC_ECHO   IO
#define SERVO_PWM         IO
```

### Communication API

**ESP-NOW Functions**
```c
int esp_now_init()                           // Initialize
int esp_now_add_peer(mac_addr, channel)     // Add peer
int esp_now_send_msg(mac_addr, data, len)   // Send
int esp_now_recv_msg(msg, timeout_ms)       // Receive
uint32_t esp_now_get_queue_depth()          // Queue status
```

---

## Vision API

### Camera Module

```python
from vision.src.camera import Camera

camera = Camera(device_id=0, width=1280, height=720)

# Usage
with camera as cam:
    frame = cam.read()                    # Get frame
    frame = cam.read(undistort=True)      # With correction
    info = cam.get_frame_info()           # Get resolution
    
camera.calibrate_from_file('calibration.yaml')
camera.save_calibration('new_calib.yaml')
```

### ArUco Detection

```python
from vision.src.aruco_detector import ArucoDetector

detector = ArucoDetector(marker_size_mm=100)

markers = detector.detect(frame)            # → List[ArucoMarker]
for marker in markers:
    print(marker.id, marker.position)       # Access detection

detector.draw_markers(frame)                # Draw on frame
detector.reset_stats()                      # Clear statistics
stats = detector.get_detection_stats()      # Get metrics
```

### Pose Estimation

```python
from vision.src.pose_estimator import PoseEstimator

estimator = PoseEstimator(camera_matrix, dist_coeffs, marker_size)

rvec, tvec = estimator.estimate_single_marker_pose(marker)
position = estimator.get_robot_position(marker)     # (x, y, z)
euler = estimator.get_robot_orientation_euler(marker)  # (roll, pitch, yaw)
```

### Homography Transform

```python
from vision.src.homography import Homography

homo = Homography()
homo.compute_from_points(src_points, dst_points)

world_pt = homo.image_to_world(image_pt)           # Transform
image_pt = homo.world_to_image(world_pt)           # Inverse
world_pts = homo.batch_transform(image_pts)        # Vectorized
```

### Warehouse Map

```python
from vision.src.warehouse_map import WarehouseMap

warehouse = WarehouseMap(width_mm=2000, height_mm=3000)

warehouse.add_obstacle(x, y, width, height, margin)
warehouse.add_waypoint(x, y)
warehouse.set_robot_position(robot_id, (x, y))
is_safe = warehouse.is_point_in_obstacle(x, y)
status = warehouse.get_swarm_status()
```

---

## Communication API

### Message Schema

```python
from communication.protocol.messages import Message, MessageType

msg = Message(
    msg_type=MessageType.HEARTBEAT,
    robot_id=1,
    sequence_num=seq,
    timestamp=time_ms,
    payload=data
)

serialized = msg.serialize()                # → bytes
msg2 = Message.deserialize(serialized)     # → Message
```

### Robot Registry

```python
from communication.protocol.robot_id import RobotRegistry, RobotIdentity, RobotType

registry = RobotRegistry()

identity = RobotIdentity(
    robot_id=1,
    robot_type=RobotType.WAREHOUSE_BOT,
    mac_address='AA:BB:CC:DD:EE:01',
    serial_number='SN001',
    firmware_version='1.0.0'
)

registry.register_robot(identity)
registry.mark_active(1)
robots = registry.get_active_robots()       # → [1, 2, 3, ...]
status = registry.get_swarm_status()        # → dict
```

### Gateway Server

```python
from communication.gateway.gateway import GatewayServer

gateway = GatewayServer(host='0.0.0.0', port=8888)
gateway.start()

gateway.register_robot(identity)
gateway.send_to_robot(message, robot_id)
received_msg = gateway.get_telemetry(timeout=1.0)
stats = gateway.get_statistics()

gateway.stop()
```

---

## Python Hardware Interface

### Configuration

Access all hardware configuration via:

```python
from firmware.config import (
    GPIO_PIN_MAPPING,
    MOTOR_PWM_FREQ,
    PID_TUNING,
    SENSOR_CALIBRATION,
    SAFETY_LIMITS
)
```

### Sensor Reading

```python
# IR Line Sensor (8-channel)
readings = read_line_sensors()              # → [adc0, adc1, ..., adc7]
center_error = calculate_line_error()       # → float

# Ultrasonic Sensor
distance_cm = read_ultrasonic()             # → float (cm)

# Battery Voltage
voltage = read_battery_voltage()            # → float (volts)
```

---

## Type Hints and Contracts

All API functions use type hints:

```python
def detect(frame: np.ndarray) → List[ArucoMarker]:
    """Detect markers in frame."""

def send_to_robot(message: Message, robot_id: int) → bool:
    """Send message to robot, returns success."""
```

---

## Error Handling

### Common Exceptions

**Firmware**: No exceptions (embedded C++), returns error codes
**Python**:
- `ValueError`: Invalid parameters
- `IOError`: Communication/hardware errors
- `TimeoutError`: No response from device

### Example Error Handling

```python
try:
    with camera as cam:
        frame = cam.read()
except IOError as e:
    logger.error(f"Camera error: {e}")
```

---

## Performance Considerations

**Firmware**:
- All functions must complete in <10ms (100 Hz loop)
- ISRs disabled during critical sections
- Watchdog timer resets if loop stalls

**Vision**:
- ArUco detection: <33ms per 1280x720 frame (30 FPS target)
- Homography transform: <1ms per point

**Communication**:
- Message send: Non-blocking, returns immediately
- Receive timeout: Default 100ms, configurable
- Queue depth: Monitor to detect saturation

---

## See Also

- [System Architecture](architecture/SystemArchitecture.md)
- [Performance Targets](PERFORMANCE.md)
- [Installation Guide](guides/INSTALLATION.md)
- [Examples](../examples/)
