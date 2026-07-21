"""
PID Controller Tuning Guide

Theoretical and practical guide for tuning PID parameters.
"""

# PID Tuning Guide for Line Following

## Theory

PID control regulates a system by minimizing error between desired and actual state:

$$u(t) = K_p \cdot e(t) + K_i \int e(t)dt + K_d \frac{de(t)}{dt}$$

Where:
- **e(t)**: Current error (target - actual)
- **Kp**: Proportional gain (immediate response)
- **Ki**: Integral gain (steady-state correction)
- **Kd**: Derivative gain (damping/smoothing)

---

## Line Following Use Case

The robot uses PID to keep centered on a line using 8 IR sensors.

```
Sensor Reading: [L7 L6 L5 L4 | R4 R3 R2 R1]
                  Left      Center      Right
```

**Error Calculation**:
- Center = (L4 + R4) / 2 (ideal center value with all sensors on line)
- Error = Actual_center - Center
- Positive error = robot shifted right (steer left)
- Negative error = robot shifted left (steer right)

---

## Manual Tuning Procedure

### Step 1: Set Ki and Kd to Zero (P-only control)

```cpp
// Start Conservative
kp = 0.1;
ki = 0.0;
kd = 0.0;
```

**Test**: Run robot on line
- If oscillation: Decrease Kp (too aggressive)
- If too sluggish: Increase Kp (too weak)
- Target: Continuous small oscillations around center (±5mm)

### Step 2: Increase Kp Until Oscillation

```cpp
// Gradually increase
kp = 0.2;  // Test
kp = 0.3;  // Test
kp = 0.5;  // Start seeing oscillation
```

Once oscillation begins, back off 10%:
```cpp
kp = 0.45;  // Good starting point
```

### Step 3: Add Kd for Damping

Derivative term reduces overshoot:

```cpp
kd = kp / 10;  // Start with rule of thumb
kd = 0.045;
```

**Test and adjust**:
- Too much Kd: Robot becomes sluggish, won't following curves
- Too little Kd: Oscillation persists
- Goldilocks zone: Follows line smoothly with <2mm drift

### Step 4: Add Ki for Steady State

Integral term corrects steady-state bias:

```cpp
ki = kp / 100;  // Start conservative
ki = 0.004;
```

**Watch for**:
- Integral wind-up: Error accumulates too fast
- Solution: Cap integral term (anti-windup)

```cpp
integral_max = 50;  // Prevent unbounded growth
```

---

## Configuration File Locations

### Hardware-Specific Tuning

**File: `firmware/include/config.h`**

```cpp
// Line Following PID
#define LINE_FOLLOW_KP        0.5
#define LINE_FOLLOW_KI        0.004
#define LINE_FOLLOW_KD        0.20

// Speed Control PID
#define SPEED_CONTROL_KP      1.0
#define SPEED_CONTROL_KI      0.01
#define SPEED_CONTROL_KD      0.05

// Sensor Tuning
#define LINE_SENSOR_THRESHOLD 400   // 0-1023 ADC range
#define CENTER_WEIGHT         1.0   // Emphasis on center vs edges

// Safety Limits
#define MAX_STEERING_OUTPUT   100   // PWM units
#define MAX_MOTOR_SPEED       255   // 8-bit PWM
```

### Testing via Python

**File: `examples/pid_tuning.py`** (Example harness)

```python
#!/usr/bin/env python3
"""Interactive PID tuning tool."""

from serial import Serial
from time import sleep
import struct

class RobotTuner:
    def __init__(self, port, baud=115200):
        self.serial = Serial(port, baud, timeout=1)
        sleep(2)  # Wait for connection
    
    def send_gains(self, kp, ki, kd):
        """Upload new PID gains to robot."""
        # Protocol: [0xFF, kp(float), ki(float), kd(float)]
        msg = bytes([0xFF]) + struct.pack('<fff', kp, ki, kd)
        self.serial.write(msg)
        print(f"Sent: Kp={kp:.3f}, Ki={ki:.4f}, Kd={kd:.3f}")
    
    def read_telemetry(self):
        """Read position and error from robot."""
        if self.serial.in_waiting >= 8:
            data = self.serial.read(8)
            position, error = struct.unpack('<ff', data)
            return position, error
        return None, None

# Interactive tuning
if __name__ == '__main__':
    tuner = RobotTuner('/dev/ttyUSB0')
    
    kp = 0.5
    while True:
        tuner.send_gains(kp, 0.004, 0.20)
        
        pos, err = tuner.read_telemetry()
        if pos is not None:
            print(f"Position: {pos:6.2f}mm, Error: {err:6.2f}mm")
        
        cmd = input("Adjust Kp (u/d/q)? ")
        if cmd == 'u':
            kp += 0.05
        elif cmd == 'd':
            kp -= 0.05
        elif cmd == 'q':
            break
```

---

## Characteristic Response Patterns

### Under-damped (Kp too high, Kd too low)
```
   Target ╭────────────
            │    ╱╲╱╲  
            │   ╱  ╲  ╲ 
   Actual ──┼──╱────╰──
            │
   Problem: Overshoot and oscillation
   Solution: Increase Kd or decrease Kp
```

### Over-damped (Kd too high, Kp too low)
```
   Target ├────────────
           │   ╱────── 
           │  ╱
   Actual ─┼─────────
           │
   Problem: Slow response, sluggish following
   Solution: Decrease Kd or increase Kp
```

### Optimal Tuning
```
   Target ├────────────
           │  ╱───────
           │ ╱
   Actual ─┼────────────
           │
   Problem: None - smooth tracking
   Solution: Use as reference
```

---

## Drift vs Speed Trade-off

Higher speeds require different tuning:

**Low Speed (50% PWM)**:
```cpp
kp = 0.5, ki = 0.004, kd = 0.20
// More responsive, aggressive steering acceptable
```

**High Speed (100% PWM)**:
```cpp
kp = 0.3, ki = 0.002, kd = 0.10
// Must be conservative, slower steering to prevent overshoot
```

Speed-dependent tuning formula:
```cpp
float speed_factor = current_speed / max_speed;  // 0.0-1.0
float adjusted_kp = base_kp * (1.0 - speed_factor * 0.4);
```

---

## Anti-Windup Implementation

```cpp
class PIDController {
private:
    float integral_term = 0;
    float integral_max = 50;  // Clamp value
    
public:
    float update(float error) {
        // Proportional
        float p_term = kp * error;
        
        // Integral with anti-windup
        integral_term += ki * error * dt;
        if (integral_term > integral_max) 
            integral_term = integral_max;
        if (integral_term < -integral_max) 
            integral_term = -integral_max;
        
        // Derivative
        float d_term = kd * (error - last_error) / dt;
        last_error = error;
        
        return p_term + integral_term + d_term;
    }
};
```

---

## Diagnostic Tests

### Test 1: Step Response
**Procedure**:
1. Robot on line at center
2. Manually shift robot 50mm to right
3. Release and measure return behavior
4. Record oscillations and settling time

**Expected**: Return to center in <500ms with <2 overshoots

### Test 2: Ramp Response
**Procedure**:
1. Slowly move line left (simulate curve) at 10mm/sec
2. Measure lag between line and robot center
3. Repeat at different speeds

**Expected**: <50mm lag at normal speeds

### Test 3: High-Frequency Input
**Procedure**:
1. Place line with sharp zigzag pattern
2. Run robot over zigzag at normal speed
3. Measure if robot follows or cuts corners

**Expected**: Robot smoothly follows with <20mm deviation

---

## Tuning Checklists

- [ ] Start with P-only control (Ki=Kd=0)
- [ ] Find Kp that causes periodic oscillation
- [ ] Add Kd to damp oscillation (reduces overshoot)
- [ ] Add Ki only if steady-state error exists
- [ ] Implement anti-windup for Ki term
- [ ] Test at multiple speeds (50%, 75%, 100%)
- [ ] Test on different colored surfaces
- [ ] Test on curved paths
- [ ] Document final gains in config.h
- [ ] Commit tuned parameters to version control

