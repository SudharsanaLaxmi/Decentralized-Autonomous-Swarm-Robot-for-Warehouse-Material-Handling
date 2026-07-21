"""
System Architecture Documentation

High-level overview of all subsystems and their interactions.
"""

# System Architecture Overview

The Decentralized Autonomous Swarm Robot system is organized into 5 major subsystems:

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│             Application Layer                    │
│   (Task Planning, Swarm Coordination, UI)       │
├─────────────────────────────────────────────────┤
│           Communication Layer                    │
│   (Message Protocol, Routing, Serialization)    │
├─────────────────────────────────────────────────┤
│         Control Layer                            │
│   (Firmware Loop, Motor Control, PID)           │
└─────────────────────────────────────────────────┘
         ↓              ↓              ↓
    ┌────────┐    ┌──────────┐    ┌────────┐
    │ Vision │    │Hardware  │    │Sensors │
    │System  │    │Interface │    │I/O     │
    └────────┘    └──────────┘    └────────┘
```

## Subsystem 1: Firmware (ESP32)

**Responsibility**: Real-time robot control

**Components**:
- `main.cpp`: Entry point and 100Hz control loop
- `motor_controller`: PWM and H-bridge control
- `pid_controller`: Feedback loop for line following
- `sensor_readers`: GPIO sampling (IR, ultrasonic, servo)
- `communication`: ESP-NOW transmitter, UDP socket

**Technology Stack**:
- MCU: ESP32 running FreeRTOS
- Language: C++17
- Framework: Arduino/PlatformIO
- Real-time guarantees: Hard real-time with task priorities

**Key Responsibilities**:
1. Sample sensors at 100 Hz
2. Execute PID line-following algorithm
3. Calculate motor commands
4. Apply PWM to motor drivers
5. Transmit telemetry to gateway
6. Receive and execute commands
7. Monitor power and safety

---

## Subsystem 2: Vision System (Python)

**Responsibility**: Environmental perception and localization

**Components**:
- `camera.py`: OpenCV camera interface
- `aruco_detector.py`: Marker detection pipeline
- `pose_estimator.py`: 6DOF pose from markers
- `homography.py`: World coordinate transformation
- `warehouse_map.py`: Environment model
- `digital_twin.py`: 3D visualization

**Technology Stack**:
- Language: Python 3.8+
- Framework: OpenCV 4.8+
- Dependencies: NumPy, SciPy, Matplotlib

**Key Responsibilities**:
1. Capture video frames from camera
2. Detect ArUco markers in frame
3. Estimate marker pose (position + orientation)
4. Transform to world coordinates via homography
5. Build and maintain warehouse map
6. Track robot position within environment
7. Detect obstacles and collision risks

**Data Flow**:
```
Camera → Frame Capture → Distortion Correction
             ↓
       ArUco Detection → Pose Estimation
             ↓
       Homography Transform
             ↓
       World Coordinates → Map Update
```

---

## Subsystem 3: Communication System

**Responsibility**: Inter-robot and robot-gateway messaging

**Components**:
- `protocol/messages.py`: Message schema and serialization
- `protocol/robot_id.py`: Identity and registry management
- `gateway/gateway.py`: Central hub server
- `esp_client/esp_now_client.c`: ESP32 client (firmware)

**Technology Stack**:
- Protocols: ESP-NOW (2.4GHz), UDP/WiFi
- Serialization: Binary struct packing
- Architecture: Hub-and-spoke (gateway central)

**Message Types**:
- HEARTBEAT: Robot health (status, battery)
- TELEMETRY: Position and state
- COMMAND: Instructions from gateway
- TASK: Objectives for swarm
- ACK: Acknowledgment
- ERROR: Fault reporting

**Key Responsibilities**:
1. Route messages between robots
2. Maintain robot registry and status
3. Serialize/deserialize binary messages
4. Handle connection timeouts and retries
5. Aggregate telemetry from swarm
6. Distribute commands to robots
7. Monitor communication health

---

## Subsystem 4: Hardware Interface

**Responsibility**: Physical component abstraction

**Components**:
- GPIO pin assignment mapping
- Motor driver (TB6612FNG) abstraction
- Sensor reading calibration
- Battery voltage monitoring
- Servo/gripper control

**Physical Devices**:
- 2x DC Motors (200 RPM, 0.8 Nm)
- Motor Driver (TB6612FNG)
- 8-channel IR array (QTR-8RC)
- Ultrasonic sensor (HC-SR04)
- Servo motor (SG90)
- Power: 2S LiPo 7.4V nominal
- Optional: IMU (MPU-6050)

**Electrical Characteristics**:
- Motor power: 6V nominal (battery provides 7.4V)
- Current per motor: 300-500mA during movement
- GPIO voltage: 3.3V (ESP32 standard)
- PWM frequency: 20 kHz for motor control
- ADC channels: 2 (battery, sensor calibration)

---

## Subsystem 5: Testing & Validation

**Responsibility**: Quality assurance across all layers

**Test Categories**:
- Unit tests: Individual module validation
- Integration tests: Subsystem interaction
- System tests: End-to-end scenarios
- Performance tests: Benchmarking
- Stress tests: Swarm scalability

**Test Framework**:
- Firmware: Custom C++ harness (MockArduino)
- Python: pytest with >85% coverage target
- Integration: Hardware-in-loop testing
- CI/CD: GitHub Actions automated validation

---

## Data Flow: Complete Cycle

### Example: Robot Moving to Target

```
1. Gateway sends COMMAND to Robot #1
   └─ Message: MoveTo(x=100, y=50)

2. Robot #1 receives command
   └─ Firmware: Parse, store target

3. Vision system localizes robot
   └─ Capture frame
   └─ Detect ArUco marker
   └─ Estimate pose → World coords

4. Control loop executes
   └─ Calculate error: target - current
   └─ PID control → Speed commands
   └─ Motor controller → PWM output

5. Motors move robot forward
   └─ Line sensors provide feedback
   └─ PID corrects heading

6. Robot transmits TELEMETRY
   └─ Position, status, battery
   └─ Gateway receives and logs

7. Gateway sends ACK back
   └─ Confirms successful reception
```

---

## Timing and Synchronization

**Critical Timing Requirements**:
- Firmware loop: 100 Hz (10ms period)
- Motor PID update: 50 Hz (20ms period)
- Vision processing: 30 Hz minimum (33ms per frame)
- Communication interval: 1 Hz heartbeat (1000ms)
- Sensor sampling: 100 Hz for closed-loop control

**Synchronization Strategy**:
- No global clock (decentralized)
- Relative timing within robot (local timestamps)
- Gateway time for correlation (message timestamps)
- Timeout-based fault detection (5-10 second windows)

---

## Scalability Considerations

### Single Robot
- CPU: ESP32 dual-core 240 MHz sufficient
- Memory: 520 KB available, ~200 KB used
- Power: 400-600 mA during movement

### Swarm Scale (10-100 robots)
- Communication: ESP-NOW handles peer-to-peer
- Gateway: Single server handles 100+ concurrent connections
- Message rate: Mix of heartbeat (1Hz) + telemetry (10Hz) per robot
- Total bandwidth: ~50 KB/s at full swarm capacity

### Network Topology
```
                ┌─── Robot 1 ───┐
                │    (WiFi UDP)  │
         ┌──────┴────────────────┴──────┐
    Gateway                          Robot 2
  (Central Hub)                    (WiFi UDP)
         └──────┬────────────────┬──────┐
                │                │      │
              Robot 3          Robot 4  Robot...
           (ESP-NOW)        (ESP-NOW)
```

---

## Fault Tolerance Mechanisms

**Single Robot Failure**:
- Heartbeat timeout → Mark robot inactive
- Other robots continue operating
- Gateway redistributes tasks

**Communication Loss**:
- Robot timeout from gateway: 5 seconds
- Local autonomy: Continue line following
- Retry with exponential backoff

**Sensor Failure**:
- Line sensor lost → Drift until correction
- IMU failure → Use dead reckoning
- Camera failure → Use local sensors only

**Motor Failure**:
- Asymmetric power loss → Firmware detects speed mismatch
- Alert sent to gateway
- Robot moves in circle toward service area

---

## Future Extensibility

**Planned Additions**:
1. ROS2 middleware bridge
2. Advanced SLAM for mapping
3. Obstacle avoidance algorithms
4. Collaborative task assignment
5. Battery management optimization
6. Machine learning for behavior

**Extension Points**:
- Message protocol supports custom payload types
- Firmware task architecture allows new controllers
- Vision pipeline integrates additional detectors
- Gateway design supports load balancing

