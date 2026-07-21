/**
 * @file main.cpp
 * @brief Main entry point and control loop for ESP32 robot
 *
 * Initializes all subsystems, manages task scheduling,
 * and coordinates robot behavior.
 *
 * @author Robotics Team
 * @date 2024
 */

#include <Arduino.h>
#include "config.h"

// Forward declarations
void setup_gpio();
void setup_communication();
void setup_tasks();

volatile uint32_t loop_counter = 0;
volatile uint32_t last_heartbeat = 0;

/**
 * @brief System initialization
 *
 * Configures GPIO, communication interfaces, sensors,
 * and launches FreeRTOS tasks.
 */
void setup() {
    // Serial communication for debugging
    Serial.begin(UART_BAUD);
    delay(500);  // Wait for serial stabilization
    
    INFO_PRINT("===========================================");
    INFO_PRINT("SWARMBot Autonomous Robot - v%s", FIRMWARE_VERSION);
    INFO_PRINT("Robot ID: %d (%s)", ROBOT_ID, ROBOT_NAME);
    INFO_PRINT("===========================================");
    
    // Initialize GPIO pins
    setup_gpio();
    INFO_PRINT("GPIO initialized");
    
    // Initialize communication interfaces
    setup_communication();
    INFO_PRINT("Communication initialized");
    
    // Initialize sensors
    DEBUG_PRINT("Initializing sensors...");
    // Motor controller initialization (in separate module)
    // IR sensor initialization (in separate module)
    // Ultrasonic initialization (in separate module)
    // Servo initialization (in separate module)
    
    // Create FreeRTOS tasks
    setup_tasks();
    INFO_PRINT("System ready. Starting main control loop.");
}

/**
 * @brief Main control loop
 *
 * Runs at 100 Hz (configurable via MAIN_LOOP_RATE_HZ).
 * Coordinates sensor reading, control algorithms,
 * and communication.
 */
void loop() {
    static uint32_t last_loop_time = 0;
    uint32_t current_time = millis();
    uint32_t dt = current_time - last_loop_time;
    
    if (dt < MAIN_LOOP_PERIOD_MS) {
        delay(MAIN_LOOP_PERIOD_MS - dt);  // Maintain loop frequency
        return;
    }
    
    last_loop_time = current_time;
    loop_counter++;
    
    // ===== SAFETY CHECKS =====
    // Check watchdog timer
    // Check battery voltage
    // Check temperature
    
    // ===== SENSOR READING =====
    // Read IR sensor array
    // Read ultrasonic sensor
    // Read IMU (if enabled)
    
    // ===== CONTROL ALGORITHMS =====
    // Update PID controllers
    // Calculate motor commands
    // Handle obstacle avoidance
    
    // ===== ACTUATOR OUTPUT =====
    // Update motor PWM
    // Update servo position
    // Send telemetry
    
    // Periodic logging
    if (loop_counter % 100 == 0) {
        DEBUG_PRINT("Loop %lu, dt=%lu ms", loop_counter, dt);
    }
}

/**
 * @brief Initialize GPIO pins
 *
 * Configures all GPIO pins for motors, sensors,
 * communication, and control lines.
 */
void setup_gpio() {
    // Motor control pins
    pinMode(MOTOR_LEFT_IN1, OUTPUT);
    pinMode(MOTOR_LEFT_IN2, OUTPUT);
    pinMode(MOTOR_LEFT_PWM, OUTPUT);
    pinMode(MOTOR_RIGHT_IN3, OUTPUT);
    pinMode(MOTOR_RIGHT_IN4, OUTPUT);
    pinMode(MOTOR_RIGHT_PWM, OUTPUT);
    
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN3, LOW);
    digitalWrite(MOTOR_RIGHT_IN4, LOW);
    
    // Sensor pins
    pinMode(ULTRASONIC_TRIG, OUTPUT);
    pinMode(ULTRASONIC_ECHO, INPUT);
    digitalWrite(ULTRASONIC_TRIG, LOW);
    
    // Servo pin
    pinMode(SERVO_GRIPPER_PIN, OUTPUT);
    
    // ADC configuration
    analogReadResolution(10);  // 10-bit ADC
    analogSetAttenuation(ADC_0db);  // ADC attenuation
    
    DEBUG_PRINT("GPIO configured");
}

/**
 * @brief Initialize communication interfaces
 *
 * Sets up UART, SPI, I2C, and wireless communication
 * protocol handlers.
 */
void setup_communication() {
    // UART already initialized in Serial.begin()
    
    // I2C initialization (if IMU enabled)
    #if ENABLE_IMU
    Wire.begin(I2C_SDA, I2C_SCL);
    Wire.setClock(I2C_FREQ);
    DEBUG_PRINT("I2C configured at %d Hz", I2C_FREQ);
    #endif
    
    // ESP-NOW initialization
    #if ENABLE_ESP_NOW
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    if (esp_now_init() != ESP_OK) {
        ERROR_PRINT("ESP-NOW initialization failed");
    }
    DEBUG_PRINT("ESP-NOW initialized");
    #endif
    
    // UDP Gateway initialization
    #if ENABLE_UDP_GATEWAY
    WiFi.begin();  // Connect to WiFi
    DEBUG_PRINT("WiFi connection initiated");
    #endif
}

/**
 * @brief Create FreeRTOS tasks
 *
 * Launches background tasks for motor control,
 * sensor reading, and communication.
 */
void setup_tasks() {
    // Create motor control task
    // xTaskCreate(motor_control_task, "MotorCtrl", TASK_STACK_SIZE, 
    //             NULL, TASK_PRIORITY_MOTOR, NULL);
    
    // Create sensor reading task
    // xTaskCreate(sensor_read_task, "SensorRead", TASK_STACK_SIZE,
    //             NULL, TASK_PRIORITY_SENSOR, NULL);
    
    // Create communication task
    // xTaskCreate(communication_task, "CommTask", TASK_STACK_SIZE,
    //             NULL, TASK_PRIORITY_COMM, NULL);
    
    DEBUG_PRINT("FreeRTOS tasks created");
}

/**
 * @brief Hardware watchdog callback
 *
 * Called periodically to verify system health
 * and trigger software resets if needed.
 */
void watchdog_task() {
    static uint32_t last_check = 0;
    uint32_t current_time = millis();
    
    if (current_time - last_check > SAFETY_TIMEOUT_MS) {
        if (current_time - last_heartbeat > MESSAGE_TIMEOUT_MS) {
            ERROR_PRINT("Communication timeout - attempting recovery");
            // Trigger reset or recovery routine
        }
        last_check = current_time;
    }
}

/**
 * @brief Performance monitoring
 *
 * Prints system statistics and performance metrics
 * for debugging and optimization.
 */
void print_system_stats() {
    uint32_t heap_free = ESP.getFreeHeap();
    uint32_t heap_total = ESP.getHeapSize();
    uint8_t heap_percent = (100 * (heap_total - heap_free)) / heap_total;
    
    INFO_PRINT("Memory: %lu/%lu bytes (%d%% used)",
        heap_total - heap_free, heap_total, heap_percent);
    INFO_PRINT("Uptime: %lu seconds", millis() / 1000);
    INFO_PRINT("Loop counter: %lu", loop_counter);
}
