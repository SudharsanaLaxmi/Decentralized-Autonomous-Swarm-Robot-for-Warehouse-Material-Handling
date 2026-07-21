/**
 * @file motor_controller.cpp
 * @brief Implementation of motor controller
 */

#include "motor_controller.h"
#include "config.h"
#include <Arduino.h>
#include <algorithm>

void MotorController::initialize(uint8_t left_pwm, uint8_t left_in1, uint8_t left_in2,
                                 uint8_t right_pwm, uint8_t right_in3, uint8_t right_in4,
                                 uint32_t frequency, uint8_t resolution) {
    this->left_pwm_pin = left_pwm;
    this->left_in1 = left_in1;
    this->left_in2 = left_in2;
    this->right_pwm_pin = right_pwm;
    this->right_in3 = right_in3;
    this->right_in4 = right_in4;
    
    // Configure PWM channels
    ledcSetup(0, frequency, resolution);  // Left motor PWM
    ledcSetup(1, frequency, resolution);  // Right motor PWM
    
    ledcAttachPin(left_pwm, 0);
    ledcAttachPin(right_pwm, 1);
    
    // Configure direction pins
    pinMode(left_in1, OUTPUT);
    pinMode(left_in2, OUTPUT);
    pinMode(right_in3, OUTPUT);
    pinMode(right_in4, OUTPUT);
    
    // Initial state: stopped
    stop();
}

void MotorController::setSpeed(int16_t left_speed, int16_t right_speed) {
    // Constrain speeds to valid range
    target_left_speed = CONSTRAIN(left_speed, -255, 255);
    target_right_speed = CONSTRAIN(right_speed, -255, 255);
    
    if (!ramping_enabled) {
        current_left_speed = target_left_speed;
        current_right_speed = target_right_speed;
        applyPWM(ABS(current_left_speed), ABS(current_right_speed));
        setDirection(current_left_speed >= 0, current_right_speed >= 0);
    }
}

void MotorController::setSpeedRamped(int16_t left_speed, int16_t right_speed,
                                     uint32_t ramp_time_ms) {
    target_left_speed = CONSTRAIN(left_speed, -255, 255);
    target_right_speed = CONSTRAIN(right_speed, -255, 255);
    ramp_duration_ms = ramp_time_ms;
    ramp_start_time = millis();
    ramping_enabled = true;
}

void MotorController::moveForward(uint8_t speed) {
    setSpeed(speed, speed);
}

void MotorController::moveBackward(uint8_t speed) {
    setSpeed(-speed, -speed);
}

void MotorController::rotateClockwise(uint8_t speed) {
    setSpeed(speed, -speed);
}

void MotorController::rotateCounterClockwise(uint8_t speed) {
    setSpeed(-speed, speed);
}

void MotorController::stop() {
    target_left_speed = 0;
    target_right_speed = 0;
    current_left_speed = 0;
    current_right_speed = 0;
    applyPWM(0, 0);
}

void MotorController::emergencyStop() {
    stop();
    DEBUG_PRINT("Emergency stop triggered");
}

void MotorController::update() {
    if (!ramping_enabled) return;
    
    uint32_t elapsed = millis() - ramp_start_time;
    
    if (elapsed >= ramp_duration_ms) {
        // Ramping complete
        current_left_speed = target_left_speed;
        current_right_speed = target_right_speed;
        ramping_enabled = false;
    } else {
        // Linear interpolation during ramp
        float progress = (float)elapsed / ramp_duration_ms;
        current_left_speed = (int16_t)(target_left_speed * progress);
        current_right_speed = (int16_t)(target_right_speed * progress);
    }
    
    // Apply the calculated speeds
    applyPWM(ABS(current_left_speed), ABS(current_right_speed));
    setDirection(current_left_speed >= 0, current_right_speed >= 0);
}

void MotorController::setDirection(bool left_forward, bool right_forward) {
    // Set left motor direction
    if (left_forward) {
        digitalWrite(left_in1, HIGH);
        digitalWrite(left_in2, LOW);
    } else {
        digitalWrite(left_in1, LOW);
        digitalWrite(left_in2, HIGH);
    }
    
    // Set right motor direction
    if (right_forward) {
        digitalWrite(right_in3, HIGH);
        digitalWrite(right_in4, LOW);
    } else {
        digitalWrite(right_in3, LOW);
        digitalWrite(right_in4, HIGH);
    }
}

void MotorController::applyPWM(uint8_t left_pwm, uint8_t right_pwm) {
    // Constrain to speed limits
    left_pwm = CONSTRAIN(left_pwm, 0, max_speed);
    right_pwm = CONSTRAIN(right_pwm, 0, max_speed);
    
    // Apply deadzone if needed
    if (left_pwm > 0 && left_pwm < min_pwm) left_pwm = min_pwm;
    if (right_pwm > 0 && right_pwm < min_pwm) right_pwm = min_pwm;
    
    // Write to PWM channels
    ledcWrite(0, left_pwm);
    ledcWrite(1, right_pwm);
}
