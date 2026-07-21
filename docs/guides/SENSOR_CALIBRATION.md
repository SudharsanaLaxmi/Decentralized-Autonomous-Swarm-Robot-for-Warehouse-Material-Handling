"""
Sensor Calibration Guide

Step-by-step procedures for calibrating all robot sensors.
"""

# Sensor Calibration Guide

Proper sensor calibration is essential for reliable robot operation.

## Table of Contents

1. [Line Following Sensors](#line-following-sensors)
2. [Ultrasonic Rangefinder](#ultrasonic-rangefinder)
3. [Battery Voltage Monitor](#battery-voltage-monitor)
4. [Optional: IMU Calibration](#optional-imu-calibration)

---

## Line Following Sensors

**Hardware**: QTR-8RC 8-channel IR reflectance array

### Calibration Procedure

**Time Required**: 5 minutes

**Prerequisites**:
- Robot on charged battery (>7V)
- Black line (minimum 1cm wide)
- White surface (reflective paper or painted floor)
- Serial monitor open (115200 baud)

### Step 1: Prepare Robot

1. Place robot on flat surface
2. Center over white surface (away from line)
3. Open serial monitor to watch calibration

### Step 2: White Calibration

```
1. Launch firmware
2. Robot will read white surface
3. Watch serial output for values
4. Move robot across different white areas
5. Calibration completes automatically
```

**Expected output**:
```
[INFO] White calibration complete
[INFO] Max readings: [950 960 955 950 945 955 960 950]
```

### Step 3: Black Calibration

```
1. Place robot centered on black line
2. Move slowly back and forth along line
3. Let sensor scan entire line length (~20cm)
4. Robot learns black surface characteristics
```

**Expected output**:
```
[INFO] Black calibration complete
[INFO] Min readings: [100 95 105 100 90 100 95 100]
```

### Step 4: Verify Calibration

```
1. Place robot partially on line
2. Watch serial error output
3. Error should be ~0 when centered
4. Error should increase when shifted left/right
```

**Sample output**:
```
Line position: -5 (centered slightly left - normal)
Line position: 0 (perfectly centered)
Line position: +4 (slightly right)
```

### Troubleshooting

**Problem**: All sensors read similar values

**Solution**: Check line contrast
- Increase lighting (overhead lamp)
- Use darker marker/line (permanent marker on white paper)
- Ensure sensors are clean

**Problem**: Sensors drift during operation

**Solution**: Temperature compensation
- Let robot warm up 5 minutes before operation
- Avoid rapid temperature changes
- Re-calibrate if environment changes significantly

---

## Ultrasonic Rangefinder

**Hardware**: HC-SR04 ultrasonic distance sensor

### Calibration Procedure

**Time Required**: 10 minutes

**Prerequisites**:
- Measuring ruler or meter stick
- Flat wall or reflective surface
- Open area (minimum 2m × 1m)

### Step 1: Distance Accuracy Check

```cpp
// Test code to output distance readings
void test_ultrasonic() {
    for (int distance = 20; distance <= 200; distance += 20) {
        // Place object at known distance
        float measured = read_ultrasonic();
        float error = abs(measured - distance);
        printf("%3d cm: %.1f cm (error: %.1f%%)\n", 
               distance, measured, (error/distance)*100);
        delay(1000);
    }
}
```

### Step 2: Measure at Multiple Distances

**Procedure**:
1. Place object at 20cm
2. Read sensor value
3. Increase distance by 20cm
4. Repeat up to 2m (200cm)

**Expected accuracy**: ±3% at any distance

### Step 3: Temperature Compensation

If errors drift:
```cpp
// Speed of sound compensation
float speed_of_sound = 331.5 + (0.6 * temperature_celsius);
// Default 343 m/s assumes 20°C
```

### Step 4: Obstacle Thresholds

Set collision avoidance distance:
```cpp
#define COLLISION_THRESHOLD_CM  30  // Stop if object <30cm
#define WARNING_THRESHOLD_CM    50  // Slow down if <50cm
```

---

## Battery Voltage Monitor

**Hardware**: Analog input on ESP32 GPIO35

### Calibration Procedure

**Time Required**: 5 minutes

**Prerequisites**:
- Multimeter (or voltmeter)
- Charged 2S LiPo battery
- Variable power supply (optional, for precision)

### Step 1: Measure Reference Voltage

```
1. Connect battery to robot
2. Measure voltage with multimeter at battery connector
3. Record exact voltage: _____ V
```

### Step 2: Read ADC Value

```cpp
// Read and log raw ADC value
void calibrate_battery() {
    int raw = analogRead(BATTERY_SENSE_PIN);
    float voltage = raw * (3.3 / 4095.0) * VOLTAGE_DIVIDER_RATIO;
    printf("Raw ADC: %d, Voltage: %.2f V\n", raw, voltage);
}
```

### Step 3: Calculate Divider Ratio

If multimeter shows 7.4V but ADC calculates 3.7V:

```cpp
#define VOLTAGE_DIVIDER_RATIO (7.4 / 3.7)  // 2.0
```

### Step 4: Test Across Voltage Range

**Discharge battery slightly**:
1. Start: 8.4V (fully charged 2S LiPo)
2. Mid: 7.4V (nominal)
3. End: 6.0V (cutoff to protect battery)

Record ADC readings at each point.

### Step 5: Set Battery Thresholds

```cpp
#define BATTERY_CRITICAL  6.0   // Stop immediately
#define BATTERY_LOW       6.5   // Reduce speed, seek charging
#define BATTERY_NOMINAL   7.4   // Full operation
```

---

## Optional: IMU Calibration

**Hardware**: MPU-6050 6-axis IMU (gyro + accelerometer)

### Accelerometer Calibration

**Procedure**:
1. Place robot on flat surface
2. Capture 100 samples at rest
3. Calculate zero-g bias for each axis
4. Log biases to firmware

### Gyroscope Calibration

**Procedure**:
1. Keep robot perfectly still
2. Read gyro for 10 seconds
3. Calculate bias (systematic error)
4. Subtract from all future readings

```cpp
// Calibration code
struct IMU_Calibration {
    float accel_bias[3];
    float gyro_bias[3];
    float mag_bias[3];
};

void calibrate_imu(IMU_Calibration &cal) {
    const int SAMPLES = 1000;
    float sum_accel[3] = {0, 0, 0};
    float sum_gyro[3] = {0, 0, 0};
    
    for (int i = 0; i < SAMPLES; i++) {
        // Read IMU
        // Accumulate readings
    }
    
    // Average
    for (int i = 0; i < 3; i++) {
        cal.accel_bias[i] = sum_accel[i] / SAMPLES;
        cal.gyro_bias[i] = sum_gyro[i] / SAMPLES;
    }
}
```

---

## Verification Checklist

After all calibrations:

- [ ] Line sensors detect line within ±10mm error
- [ ] Ultrasonic measures distances within ±3% accuracy
- [ ] Battery voltage reads correct on multimeter
- [ ] Robot moves straight on flat surface (no drift)
- [ ] Robot follows line without excessive oscillation
- [ ] Collision avoidance triggers at correct distance

---

## Recalibration Schedule

| Sensor | Recalibration Frequency |
|--------|------------------------|
| Line sensors | Weekly or when surface changes |
| Ultrasonic | Monthly (if environmental conditions stable) |
| Battery monitor | Once per battery or every 6 months |
| IMU | After physical impacts or every 3 months |

---

## Saving Calibration Data

```cpp
// Store in EEPROM
void save_calibration_to_eeprom() {
    EEPROM.put(ADDR_CALIBRATION, calibration_data);
    EEPROM.commit();
}

// Load on startup
void load_calibration_from_eeprom() {
    EEPROM.get(ADDR_CALIBRATION, calibration_data);
}
```

---

## See Also

- [Hardware Assembly Guide](../../hardware/README.md)
- [PID Tuning Guide](PID_TUNING.md)
- [Installation Guide](INSTALLATION.md)
