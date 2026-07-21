# Testing

## Overview

Comprehensive testing framework including unit tests, integration tests, system-level validation, and performance benchmarks.

## Test Structure

```
testing/
├── unit/                       # Single component tests
│   ├── test_pid_controller.py  # PID algorithm validation
│   ├── test_motors.py          # Motor driver tests
│   ├── test_sensors.py         # Sensor interface tests
│   └── test_communication.py   # Message protocol tests
├── integration/                # Component interaction tests
│   ├── test_navigation.py      # Movement coordination
│   ├── test_autopilot.py       # Autonomous behavior
│   └── test_gripper.py         # Pick-place operations
├── system/                     # End-to-end tests
│   ├── test_warehouse_task.py  # Full task execution
│   ├── test_swarm.py           # Multi-robot coordination
│   └── test_resilience.py      # Failure scenarios
└── README.md                   # This file
```

## Test Execution

### Run All Tests

```bash
pytest testing/ -v
```

### Run by Category

```bash
# Unit tests only
pytest testing/unit/ -v

# Integration tests only
pytest testing/integration/ -v -m integration

# System tests (slow, requires hardware)
pytest testing/system/ -v -m system --hardware
```

### Code Coverage

```bash
pytest testing/ --cov=vision --cov-report=html
```

## Test Categories

### Unit Tests

**Scope**: Individual functions/classes in isolation

**Examples**:
- PID controller step response
- Motor PWM calculation
- Message serialization
- Sensor data parsing

**Framework**: pytest with mocking

**Target Coverage**: >90% line coverage

### Integration Tests

**Scope**: Multiple components working together

**Examples**:
- Line following (IR sensors + PID + motors)
- Navigation and obstacle avoidance
- Pick-place sequence coordination

**Framework**: pytest with fixture-based integration

**Target Coverage**: >80% path coverage

### System Tests

**Scope**: End-to-end scenarios

**Examples**:
- Autonomous warehouse pickup task
- Multi-robot coordination
- Failure detection and recovery

**Framework**: pytest with hardware simulation or actual robots

**Target Coverage**: Critical path scenarios

## Performance Benchmarks

### Motor Control

```
Test: PID controller step response
Expected: Settle within 200ms
Tolerance: ±20%
```

### Vision Processing

```
Test: ArUco detection latency
Expected: <5ms per 30MP image
Hardware: Intel i7, NVIDIA GTX1050
```

### Communication

```
Test: ESP-NOW round-trip time
Expected: 10ms average, 20ms max
Environment: 10m line-of-sight
```

## Continuous Integration

CI pipeline runs on every commit:

```yaml
- Lint (flake8 + pylint)
- Format check (black)
- Type check (mypy)
- Unit tests (pytest)
- Coverage report
```

See `.github/workflows/` for CI configuration.

## Hardware Testing

### Prerequisites for Hardware Tests

- Physical robot assembly
- Calibrated sensors
- Charged battery
- Safe test environment

### Test Environment Setup

```
+---+---+---+
|   |   |   |  Warehouse simulation
+---+---+---+  10m x 10m test area
|   |R  |   |  with obstacles
+---+---+---+
```

### Safety Procedures

1. Always have manual override
2. Start with low motor speeds
3. Use barriers around test area
4. Record all failures
5. Check battery voltage before testing

## Failure Modes Testing

| Failure Mode | Test Procedure | Recovery Validation |
|---|---|---|
| Motor jam | Block wheel, verify timeout | Timeout and rollback |
| Sensor failure | Unplug sensor, test graceful degradation | Operate on remaining sensors |
| Communication loss | Drop packets, verify heartbeat | Automatic retry and reconnect |
| Low battery |  Drain battery to threshold | Graceful shutdown warning |
| Servo jam | Block gripper | Position feedback and release |

## Benchmark Results (Reference)

Measured on Dell XPS 13, Intel i7, 16GB RAM:

| Test | Metric | Result | Status |
|------|--------|--------|--------|
| PID step | Settle time | 180ms | ✓ PASS |
| Motor acceleration | 0-200 RPM | 150ms | ✓ PASS |
| Line detection | Array to output | 2ms | ✓ PASS |
| ArUco detection | 1280x720p30 | 3.2ms | ✓ PASS |
| UDP latency | Round-trip | 12ms | ✓ PASS |

## Future Testing Infrastructure

- [ ] Simulation environment (Gazebo/ROS2)
- [ ] Hardware-in-the-loop (HIL) testing
- [ ] Stress testing framework
- [ ] Automated hardware test rig
