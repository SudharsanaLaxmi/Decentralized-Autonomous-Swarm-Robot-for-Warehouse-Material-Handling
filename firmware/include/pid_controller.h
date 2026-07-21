/**
 * @file pid_controller.h
 * @brief PID feedback control loop implementation
 *
 * Generic PID controller for line following,
 * motor speed regulation, and other feedback loops.
 */

#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

#include <stdint.h>
#include <Arduino.h>

/**
 * @class PIDController
 * @brief Classic PID control loop
 *
 * Implements proportional-integral-derivative feedback
 * control with antiwindup and output limiting.
 */
class PIDController {
public:
    /**
     * @brief Constructor
     * @param kp Proportional gain
     * @param ki Integral gain
     * @param kd Derivative gain
     * @param setpoint Target value
     * @param update_rate_hz Control loop frequency (Hz)
     */
    PIDController(float kp = 1.0, float ki = 0.0, float kd = 0.0,
                  float setpoint = 0.0, uint16_t update_rate_hz = 50);
    
    /**
     * @brief Update PID controller
     * @param measured_value Current measured value
     * @return Control output
     */
    float update(float measured_value);
    
    /**
     * @brief Set target setpoint
     * @param sp Target setpoint
     */
    void setSetpoint(float sp) { setpoint = sp; }
    
    /**
     * @brief Get current error
     * @return Last calculated error
     */
    float getError() const { return error; }
    
    /**
     * @brief Set PID gains
     * @param kp Proportional gain
     * @param ki Integral gain
     * @param kd Derivative gain
     */
    void setGains(float kp, float ki, float kd);
    
    /**
     * @brief Set output limits
     * @param min_output Minimum output value
     * @param max_output Maximum output value
     */
    void setOutputLimits(float min_output, float max_output);
    
    /**
     * @brief Reset controller state
     * Clears integral and derivative terms
     */
    void reset();
    
    /**
     * @brief Get PID components
     * @return Proportional term
     */
    float getProportionalTerm() const { return p_term; }
    
    /**
     * @brief Get integral term
     * @return Integral term
     */
    float getIntegralTerm() const { return i_term; }
    
    /**
     * @brief Get derivative term
     * @return Derivative term
     */
    float getDerivativeTerm() const { return d_term; }
    
    /**
     * @brief Get total output
     * @return Total PID output
     */
    float getOutput() const { return output; }

private:
    // Control parameters
    float kp, ki, kd;           // PID gains
    float setpoint;             // Target value
    float error;                // Current error
    
    // PID terms
    float p_term = 0;           // Proportional
    float i_term = 0;           // Integral
    float d_term = 0;           // Derivative
    float output = 0;           // Total output
    
    // Previous state for derivative calculation
    float prev_error = 0;
    uint32_t last_update = 0;
    float dt = 0.02;            // Time step (seconds)
    
    // Output limiting
    float min_output = -255;
    float max_output = 255;
    
    // Anti-windup
    float integral_max = 100;
};

#endif // PID_CONTROLLER_H
