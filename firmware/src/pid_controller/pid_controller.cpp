/**
 * @file pid_controller.cpp
 * @brief PID controller implementation
 */

#include "pid_controller.h"
#include <algorithm>

PIDController::PIDController(float kp, float ki, float kd,
                             float setpoint, uint16_t update_rate_hz)
    : kp(kp), ki(ki), kd(kd), setpoint(setpoint),
      dt(1.0f / update_rate_hz) {
}

float PIDController::update(float measured_value) {
    uint32_t now = millis();
    
    // Update time delta if needed (for variable update frequency)
    if (last_update > 0) {
        dt = (now - last_update) / 1000.0f;
    }
    last_update = now;
    
    // Calculate error
    error = setpoint - measured_value;
    
    // Proportional term
    p_term = kp * error;
    
    // Integral term with anti-windup
    i_term += ki * error * dt;
    i_term = std::max(-integral_max, std::min(integral_max, i_term));
    
    // Derivative term
    float derivative = (error - prev_error) / dt;
    d_term = kd * derivative;
    
    prev_error = error;
    
    // Calculate total output
    output = p_term + i_term + d_term;
    
    // Apply output limits
    output = std::max(min_output, std::min(max_output, output));
    
    return output;
}

void PIDController::setGains(float kp_new, float ki_new, float kd_new) {
    kp = kp_new;
    ki = ki_new;
    kd = kd_new;
}

void PIDController::setOutputLimits(float min_out, float max_out) {
    min_output = min_out;
    max_output = max_out;
    integral_max = max_out * 0.5f;  // Anti-windup limit
}

void PIDController::reset() {
    error = 0;
    prev_error = 0;
    p_term = 0;
    i_term = 0;
    d_term = 0;
    output = 0;
    last_update = 0;
}
