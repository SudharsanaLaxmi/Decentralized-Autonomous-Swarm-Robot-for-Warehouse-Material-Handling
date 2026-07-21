/**
 * @file motor_controller.h
 * @brief Motor control interface for ESP32 robot
 *
 * Provides abstraction for DC motor control via PWM
 * and H-bridge driver (TB6612FNG).
 */

#ifndef MOTOR_CONTROLLER_H
#define MOTOR_CONTROLLER_H

#include <stdint.h>

/**
 * @class MotorController
 * @brief Manages differential drive motor control
 *
 * Handles PWM generation, direction control, and
 * motor ramping for smooth acceleration.
 */
class MotorController {
public:
    /**
     * @brief Initialize motor controller
     * @param left_pwm_pin ESP32 GPIO for left motor PWM
     * @param left_in1 GPIO for left motor direction 1
     * @param left_in2 GPIO for left motor direction 2
     * @param right_pwm_pin GPIO for right motor PWM
     * @param right_in3 GPIO for right motor direction 1
     * @param right_in4 GPIO for right motor direction 2
     * @param frequency PWM frequency in Hz
     * @param resolution PWM resolution (bits)
     */
    void initialize(uint8_t left_pwm_pin, uint8_t left_in1, uint8_t left_in2,
                   uint8_t right_pwm_pin, uint8_t right_in3, uint8_t right_in4,
                   uint32_t frequency = 20000, uint8_t resolution = 8);
    
    /**
     * @brief Set motor speeds
     * @param left_speed Left motor speed (-255 to 255)
     *                   Negative = reverse, positive = forward
     * @param right_speed Right motor speed (-255 to 255)
     */
    void setSpeed(int16_t left_speed, int16_t right_speed);
    
    /**
     * @brief Set motor speeds with ramping
     * @param left_speed Target left speed
     * @param right_speed Target right speed
     * @param ramp_time_ms Time to reach target (ms)
     */
    void setSpeedRamped(int16_t left_speed, int16_t right_speed, 
                        uint32_t ramp_time_ms);
    
    /**
     * @brief Move forward
     * @param speed Speed (0-255)
     */
    void moveForward(uint8_t speed);
    
    /**
     * @brief Move backward
     * @param speed Speed (0-255)
     */
    void moveBackward(uint8_t speed);
    
    /**
     * @brief Rotate clockwise
     * @param speed Rotation speed (0-255)
     */
    void rotateClockwise(uint8_t speed);
    
    /**
     * @brief Rotate counterclockwise
     * @param speed Rotation speed (0-255)
     */
    void rotateCounterClockwise(uint8_t speed);
    
    /**
     * @brief Stop all motors
     */
    void stop();
    
    /**
     * @brief Emergency stop
     * Immediately halts all motion
     */
    void emergencyStop();
    
    /**
     * @brief Get current left motor speed
     * @return Current PWM value (-255 to 255)
     */
    int16_t getLeftSpeed() const { return current_left_speed; }
    
    /**
     * @brief Get current right motor speed
     * @return Current PWM value (-255 to 255)
     */
    int16_t getRightSpeed() const { return current_right_speed; }
    
    /**
     * @brief Enable motor ramping
     * @param enable True to enable ramping
     */
    void setRampingEnabled(bool enable) { ramping_enabled = enable; }
    
    /**
     * @brief Set maximum speed limit
     * @param max_pwm Maximum PWM value (0-255)
     */
    void setMaxSpeed(uint8_t max_pwm) { max_speed = max_pwm; }
    
    /**
     * @brief Update ramping state
     * Called periodically to handle acceleration ramping
     */
    void update();

private:
    // Hardware configuration
    uint8_t left_pwm_pin, left_in1, left_in2;
    uint8_t right_pwm_pin, right_in3, right_in4;
    uint8_t left_pwm_channel, right_pwm_channel;
    
    // Current state
    int16_t current_left_speed = 0;
    int16_t current_right_speed = 0;
    int16_t target_left_speed = 0;
    int16_t target_right_speed = 0;
    
    // Ramping configuration
    bool ramping_enabled = true;
    uint32_t ramp_start_time = 0;
    uint32_t ramp_duration_ms = 500;
    
    // Safety limits
    uint8_t max_speed = 255;
    uint8_t min_pwm = 50;  // Deadzone to overcome friction
    
    /**
     * @brief Helper to set motor direction
     */
    void setDirection(bool left_forward, bool right_forward);
    
    /**
     * @brief Apply PWM to motors
     */
    void applyPWM(uint8_t left_pwm, uint8_t right_pwm);
};

#endif // MOTOR_CONTROLLER_H
