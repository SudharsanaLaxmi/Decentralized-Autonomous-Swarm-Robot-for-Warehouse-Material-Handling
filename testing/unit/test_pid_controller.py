"""
Unit tests for PID controller

Tests feedback control loop implementation.
"""

import pytest
from firmware.pid_controller import PIDController


@pytest.fixture
def pid_controller():
    """Create PID controller instance."""
    return PIDController(kp=1.0, ki=0.0, kd=0.1, setpoint=0.0, update_rate_hz=50)


class TestPIDController:
    """Tests for PID feedback control."""
    
    def test_pid_initialization(self, pid_controller):
        """Test PID controller initializes correctly."""
        assert pid_controller.getSetpoint() == 0.0
        assert pid_controller.getError() == 0.0
        assert pid_controller.getOutput() == 0.0
    
    def test_pid_proportional_response(self, pid_controller):
        """Test proportional term response."""
        output = pid_controller.update(1.0)  # Error = -1.0
        
        # Should be negative (error in negative direction)
        assert output < 0
    
    def test_pid_reset(self, pid_controller):
        """Test PID state reset."""
        pid_controller.update(5.0)
        pid_controller.reset()
        
        assert pid_controller.getError() == 0.0
        assert pid_controller.getOutput() == 0.0
    
    def test_pid_gain_adjustment(self, pid_controller):
        """Test PID gains can be adjusted."""
        pid_controller.setGains(2.0, 0.1, 0.2)
        output1 = pid_controller.update(1.0)
        
        pid_controller.reset()
        pid_controller.setGains(1.0, 0.0, 0.0)
        output2 = pid_controller.update(1.0)
        
        # Different gains should produce different outputs
        assert abs(output1 - output2) > 0.1
    
    def test_output_limiting(self, pid_controller):
        """Test output limiting prevents saturation."""
        pid_controller.setOutputLimits(-100, 100)
        output = pid_controller.update(1000.0)  # Large error
        
        assert output <= 100
        assert output >= -100
