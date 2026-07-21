/**
 * @file config.h
 * @brief Central configuration for ESP32 robot platform
 *
 * Contains all hardware pin assignments, tuning parameters,
 * and feature flags for the autonomous warehouse robot.
 *
 * @author Robotics Team
 * @date 2024
 */

#ifndef SWARMBOT_CONFIG_H
#define SWARMBOT_CONFIG_H

#include <stdint.h>

// ============================================================
// DEBUG CONFIGURATION
// ============================================================
#define DEBUG_LEVEL 2  // 0=Production, 1=Warning, 2=Debug, 3=Verbose

#if DEBUG_LEVEL > 0
#define DEBUG_PRINT(fmt, ...) Serial.printf("[DEBUG] " fmt "\n", ##__VA_ARGS__)
#else
#define DEBUG_PRINT(fmt, ...)
#endif

#define INFO_PRINT(fmt, ...) Serial.printf("[INFO] " fmt "\n", ##__VA_ARGS__)
#define ERROR_PRINT(fmt, ...) Serial.printf("[ERROR] " fmt "\n", ##__VA_ARGS__)

// ============================================================
// ROBOT IDENTIFICATION
// ============================================================
#define ROBOT_ID 0x01              // Unique robot identifier (1-255)
#define ROBOT_NAME "SWARMBot-01"   // Human-readable name
#define FIRMWARE_VERSION "1.0.0"   // Semantic versioning

// ============================================================
// HARDWARE - GPIO PIN ASSIGNMENTS
// ============================================================

// Motor Control (TB6612FNG)
#define MOTOR_LEFT_IN1 GPIO_NUM_14     // Motor A direction 1
#define MOTOR_LEFT_IN2 GPIO_NUM_12     // Motor A direction 2
#define MOTOR_LEFT_PWM GPIO_NUM_25     // Motor A speed (PWM)
#define MOTOR_LEFT_PWM_CH 0            // PWM channel

#define MOTOR_RIGHT_IN3 GPIO_NUM_27    // Motor B direction 1
#define MOTOR_RIGHT_IN4 GPIO_NUM_26    // Motor B direction 2
#define MOTOR_RIGHT_PWM GPIO_NUM_33    // Motor B speed (PWM)
#define MOTOR_RIGHT_PWM_CH 1           // PWM channel

// Sensor - Line Following (IR Array)
#define IR_SENSOR_PIN GPIO_NUM_35      // Analog input for QTR-8RC
#define IR_SENSOR_ADC_CH ADC1_CHANNEL_7

// Sensor - Obstacle Detection (Ultrasonic)
#define ULTRASONIC_ECHO GPIO_NUM_34    // Echo pin (input)
#define ULTRASONIC_TRIG GPIO_NUM_32    // Trigger pin (output)

// Servo - Gripper Control
#define SERVO_GRIPPER_PIN GPIO_NUM_19  // PWM for servo
#define SERVO_GRIPPER_CH 2             // PWM channel

// Communication
#define UART_TX GPIO_NUM_1             // UART1 TX
#define UART_RX GPIO_NUM_3             // UART1 RX
#define UART_BAUD 115200               // Serial baud rate

// I2C (Optional IMU)
#define I2C_SDA GPIO_NUM_21            // I2C Data
#define I2C_SCL GPIO_NUM_22            // I2C Clock
#define I2C_FREQ 400000                // I2C frequency (Hz)

// ============================================================
// MOTOR CONTROL PARAMETERS
// ============================================================
#define MOTOR_PWM_FREQUENCY 20000      // 20 kHz (TB6612FNG max)
#define MOTOR_PWM_RESOLUTION 8         // 8-bit (0-255)

#define MOTOR_MAX_PWM 255              // Maximum PWM value
#define MOTOR_MIN_PWM 50               // Minimum PWM to overcome friction
#define MOTOR_DEADZONE 0               // Controller deadzone (PWM units)

#define MOTOR_RAMP_ENABLED 1           // Enable acceleration ramping
#define MOTOR_RAMP_TIME_MS 500         // Time to reach target speed (ms)

// ============================================================
// PID CONTROLLER TUNING
// ============================================================
// Line Following PID
#define PID_LINE_KP 0.5                // Proportional gain
#define PID_LINE_KI 0.0                // Integral gain
#define PID_LINE_KD 0.2                // Derivative gain
#define PID_LINE_SETPOINT 0            // Target line position (center=0)
#define PID_LINE_MAX_ERROR 4           // Maximum error magnitude
#define PID_LINE_UPDATE_RATE_HZ 50     // Control loop frequency

// Motor Speed Regulation PID
#define PID_SPEED_KP 0.8               // Proportional gain
#define PID_SPEED_KI 0.1               // Integral gain
#define PID_SPEED_KD 0.05              // Derivative gain
#define PID_SPEED_UPDATE_RATE_HZ 100   // Control loop frequency

// ============================================================
// SENSOR CONFIGURATION
// ============================================================

// IR Line Sensor Array (QTR-8RC)
#define IR_SENSOR_COUNT 8              // Number of IR sensors
#define IR_SENSOR_MAX_VALUE 1023       // ADC maximum (10-bit)
#define IR_THRESHOLD 500               // Black/white threshold
#define IR_CALIBRATION_SAMPLES 50      // Samples for calibration
#define IR_READ_INTERVAL_MS 20         // 50 Hz sampling

// Ultrasonic Sensor (HC-SR04)
#define ULTRASONIC_TIMEOUT_US 100000   // Max echo wait time (100ms)
#define ULTRASONIC_MAX_DISTANCE_CM 400 // Maximum measurable distance
#define ULTRASONIC_TRIGGER_US 10       // Trigger pulse width
#define ULTRASONIC_READ_INTERVAL_MS 50 // 20 Hz sampling
#define OBSTACLE_DISTANCE_THRESHOLD_CM 20  // Obstacle warning threshold

// ============================================================
// SERVO GRIPPER CONFIGURATION
// ============================================================
#define SERVO_MIN_ANGLE 0              // Fully open
#define SERVO_MAX_ANGLE 90             // Fully closed
#define SERVO_CENTER_ANGLE 45
#define SERVO_PWM_MIN 500              // PWM pulse min (µs)
#define SERVO_PWM_MAX 2500             // PWM pulse max (µs)
#define SERVO_PWM_FREQ 50              // 50 Hz for servo

#define GRIPPER_OPEN_ANGLE 10          // Gripper open position
#define GRIPPER_CLOSED_ANGLE 80        // Gripper closed position
#define GRIPPER_HOLD_TIME_MS 500       // Hold time after gripping

// ============================================================
// NAVIGATION PARAMETERS
// ============================================================
#define MAX_FORWARD_SPEED 200          // PWM units (0-255)
#define MAX_REVERSE_SPEED 180
#define MAX_TURN_SPEED 150
#define ACCELERATION_STEP 5            // PWM units per step

#define WHEEL_DIAMETER_CM 6.5          // Wheel diameter
#define WHEEL_BASE_CM 12.0             // Distance between wheels
#define WHEELS_PER_REVOLUTION 20       // Pulses per revolution (if encoder used)

// ============================================================
// COMMUNICATION CONFIGURATION
// ============================================================

// ESP-NOW Settings
#define ESPNOW_CHANNEL 1               // WiFi channel for ESP-NOW
#define ESPNOW_ENCRYPTION 0            // 0=unencrypted, 1=encrypted (future)

// UDP Gateway Communication
#define UDP_GATEWAY_IP "192.168.1.100" // Gateway server IP
#define UDP_GATEWAY_PORT 8888          // Gateway UDP port
#define UDP_LOCAL_PORT 9999            // Local UDP port
#define UDP_HEARTBEAT_INTERVAL_MS 1000 // Heartbeat frequency

// Message Timeouts
#define MESSAGE_TIMEOUT_MS 5000        // Max time without communication
#define HEARTBEAT_TIMEOUT_MS 10000     // Max time without heartbeat

// ============================================================
// POWER MANAGEMENT
// ============================================================
#define BATTERY_MIN_VOLTAGE 6.8        // Minimum operating voltage (2S LiPo)
#define BATTERY_MAX_VOLTAGE 8.4        // Maximum voltage
#define BATTERY_ADC_PIN GPIO_NUM_36    // Battery voltage sense (ADC0)
#define BATTERY_VOLTAGE_DIVIDER 3.3    // Voltage divider ratio
#define BATTERY_CHECK_INTERVAL_MS 5000 // Battery voltage check frequency

// ============================================================
// TIMING & SCHEDULING
// ============================================================
#define MAIN_LOOP_RATE_HZ 100          // Main control loop frequency
#define MAIN_LOOP_PERIOD_MS (1000 / MAIN_LOOP_RATE_HZ)

#define TASK_STACK_SIZE 4096           // FreeRTOS task stack size
#define TASK_PRIORITY_MOTOR 3          // Motor control task priority
#define TASK_PRIORITY_SENSOR 2         // Sensor reading task priority
#define TASK_PRIORITY_COMM 2           // Communication task priority

// ============================================================
// SAFETY LIMITS
// ============================================================
#define SAFETY_TIMEOUT_MS 5000         // Watchdog timeout for safety
#define MAX_CONTINUOUS_RUN_TIME_MS 600000  // 10 minutes max continuous
#define THERMAL_SHUTDOWN_TEMP_C 80    // Temperature cutoff

// ============================================================
// FEATURE FLAGS
// ============================================================
#define ENABLE_LINE_FOLLOWING 1        // Enable IR-based line following
#define ENABLE_OBSTACLE_AVOIDANCE 1    // Enable ultrasonic-based avoidance
#define ENABLE_GRIPPER_CONTROL 1       // Enable servo gripper
#define ENABLE_ESP_NOW 1               // Enable ESP-NOW communication
#define ENABLE_UDP_GATEWAY 0           // Enable UDP communication (requires WiFi)
#define ENABLE_IMU 0                   // Enable IMU sensor
#define ENABLE_BATTERY_MONITORING 1    // Enable battery voltage monitoring
#define ENABLE_DEBUG_OUTPUT 1          // Enable serial debug output

// ============================================================
// CALIBRATION DATA (to be loaded from EEPROM)
// ============================================================
#define EEPROM_SIZE 512
#define EEPROM_CALIBRATION_BASE 0

// These should be read from persistent storage, not hardcoded:
// uint16_t ir_min_value[IR_SENSOR_COUNT];  // Calibration white baseline
// uint16_t ir_max_value[IR_SENSOR_COUNT];  // Calibration black baseline
// float pid_gains[3];  // Loaded from EEPROM

// ============================================================
// CONSTANTS
// ============================================================
#define PI 3.14159265359
#define DEG_TO_RAD(x) ((x) * PI / 180.0)
#define RAD_TO_DEG(x) ((x) * 180.0 / PI)

// ============================================================
// UTILITY MACROS
// ============================================================
#define CONSTRAIN(x, min_val, max_val) \
    ((x) < (min_val) ? (min_val) : ((x) > (max_val) ? (max_val) : (x)))

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

#define ABS(x) ((x) < 0 ? -(x) : (x))

#endif  // SWARMBOT_CONFIG_H
