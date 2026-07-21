"""
Line Following Sensor Interface

8-channel IR reflectance sensor (QTR-8RC) abstraction.
"""

#ifndef LINE_FOLLOWER_H
#define LINE_FOLLOWER_H

#include <stdint.h>
#include <vector>

/**
 * Line Following Sensor Interface
 * 
 * Reads 8-channel IR reflectance array (QTR-8RC)
 * and computes line center error for PID control.
 */
class LineFollower {
private:
    // Pin configuration (from config.h)
    static const uint8_t SENSOR_PIN = 35;  // ADC pin for multiplexed reading
    static const uint8_t NUM_SENSORS = 8;
    static const uint16_t CALIBRATION_SAMPLES = 100;
    
    // Sensor data
    uint16_t raw_readings[NUM_SENSORS];
    uint16_t calibrated_readings[NUM_SENSORS];
    
    // Calibration data
    uint16_t white_values[NUM_SENSORS];  // Reflective surfaces
    uint16_t black_values[NUM_SENSORS];  // Absorbent surfaces
    bool is_calibrated;
    
public:
    /**
     * Initialize line follower
     */
    void initialize();
    
    /**
     * Calibrate sensor on white surface
     * 
     * Call robot on white paper away from line
     */
    void calibrate_white();
    
    /**
     * Calibrate sensor on black surface
     * 
     * Call robot on black line
     */
    void calibrate_black();
    
    /**
     * Read raw sensor values
     */
    void read_raw();
    
    /**
     * Compute line center error
     * 
     * Returns:
     *   Negative: Line to the left (steer left)
     *   Zero: Line centered
     *   Positive: Line to the right (steer right)
     */
    int16_t compute_error();
    
    /**
     * Get array of calibrated readings (0-1000)
     * 
     * 0 = Black (on line)
     * 1000 = White (off line)
     */
    std::vector<uint16_t> get_calibrated();
    
    /**
     * Get raw ADC readings
     */
    std::vector<uint16_t> get_raw();
    
    /**
     * Check if sensor can detect line
     * 
     * Returns true if center sensors detect line
     */
    bool is_on_line();
    
private:
    /**
     * Read single sensor (ADC via multiplexer)
     */
    uint16_t read_sensor(uint8_t index);
    
    /**
     * Convert raw to 0-1000 scale
     */
    uint16_t calibrate_value(uint16_t raw, uint8_t index);
};

#endif  // LINE_FOLLOWER_H
