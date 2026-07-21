"""
Ultrasonic Distance Sensor Interface

HC-SR04 ultrasonic rangefinder for obstacle detection.
"""

#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <stdint.h>

/**
 * Ultrasonic Sensor Interface
 * 
 * HC-SR04 sensor for measuring distance to obstacles.
 * Range: 2cm to 4m
 * Accuracy: ±3mm
 */
class UltrasonicSensor {
private:
    // Pin configuration
    uint8_t trigger_pin;
    uint8_t echo_pin;
    
    // Sensor state
    float last_distance_cm;
    uint32_t last_measurement_time;
    
    // Calibration
    float speed_of_sound;  // 343 m/s at 20°C
    
public:
    /**
     * Initialize sensor
     * 
     * Args:
     *   trig_pin: GPIO for trigger
     *   echo_pin: GPIO for echo
     */
    void initialize(uint8_t trig_pin, uint8_t echo_pin);
    
    /**
     * Measure distance to nearest obstacle
     * 
     * Returns: Distance in centimeters, or -1 if timeout
     * 
     * Note: Blocking call, takes ~60ms
     */
    float measure_distance();
    
    /**
     * Measure distance with timeout
     * 
     * Args:
     *   timeout_us: Maximum time to wait (microseconds)
     * 
     * Returns: Distance in cm, or -1 if timeout/error
     */
    float measure_distance_timeout(uint32_t timeout_us);
    
    /**
     * Get last measured distance (non-blocking)
     * 
     * Returns: Last measurement in cm
     */
    float get_last_distance();
    
    /**
     * Check if obstacle detected within range
     * 
     * Args:
     *   range_cm: Minimum safe distance
     * 
     * Returns: true if obstacle within range
     */
    bool is_obstacle_near(float range_cm);
    
    /**
     * Get sensor reading in microseconds (raw echo time)
     * 
     * Useful for debugging or custom calibration
     */
    uint32_t get_raw_time_us();
    
private:
    /**
     * Convert echo time to distance
     * 
     * Formula: distance = (echo_time / 2) * speed_of_sound
     * Divided by 2 because sound travels to object and back
     */
    float time_to_distance(uint32_t echo_time_us);
};

#endif  // ULTRASONIC_H
