"""
Example: Basic Robot Movement

Demonstrates fundamental robot control patterns:
- Initialize robot
- Move forward
- Execute turns
- Monitor sensors
"""

#!/usr/bin/env python3

import sys
import time
sys.path.insert(0, '/path/to/repo')

from communication.protocol.messages import Message, TelemetryMessage, MessageType
from communication.protocol.robot_id import RobotIdentity, RobotType
from communication.gateway.gateway import GatewayServer


def example_basic_movement():
    """
    Basic example showing how to:
    1. Initialize gateway
    2. Connect robot
    3. Send movement commands
    4. Receive telemetry
    """
    
    # Initialize gateway
    gateway = GatewayServer(host='0.0.0.0', port=8888)
    gateway.start()
    print("Gateway started on port 8888")
    
    # Register robot
    robot = RobotIdentity(
        robot_id=1,
        robot_type=RobotType.WAREHOUSE_BOT,
        mac_address='AA:BB:CC:DD:EE:01',
        serial_number='SN001',
        firmware_version='1.0.0'
    )
    gateway.register_robot(robot)
    print(f"Registered robot {robot.robot_id}")
    
    # Simulate incoming telemetry
    print("\nWaiting for robot telemetry...")
    telemetry_count = 0
    
    start_time = time.time()
    while time.time() - start_time < 10:  # Run for 10 seconds
        
        # Check for incoming messages
        msg = gateway.get_telemetry(timeout=0.5)
        if msg:
            telemetry_count += 1
            print(f"[{telemetry_count}] RX from Robot {msg.robot_id}: "
                  f"seq={msg.sequence_num}, type={msg.msg_type}")
        
        # Send command every 2 seconds
        if telemetry_count % 4 == 0 and telemetry_count > 0:
            cmd = Message(
                msg_type=MessageType.COMMAND,
                robot_id=1,
                sequence_num=telemetry_count,
                timestamp=int(time.time() * 1000)
            )
            gateway.send_to_robot(cmd, robot_id=1)
            print(f"[SEND] Command to Robot 1")
        
        time.sleep(0.5)
    
    # Print statistics
    stats = gateway.get_statistics()
    print(f"\nGateway Statistics:")
    print(f"  Messages received: {stats['messages_received']}")
    print(f"  Messages sent: {stats['messages_sent']}")
    print(f"  Total robots: {stats['total_robots']}")
    print(f"  Active robots: {stats['active_robots']}")
    print(f"  Uptime: {stats['uptime_seconds']:.1f}s")
    
    gateway.stop()


def example_vision_detection():
    """
    Example showing ArUco marker detection workflow:
    1. Capture video frame
    2. Detect markers
    3. Estimate poses
    4. Update map
    """
    
    from vision.src.camera import Camera
    from vision.src.aruco_detector import ArucoDetector
    from vision.src.pose_estimator import PoseEstimator
    from vision.src.warehouse_map import WarehouseMap
    
    # Initialize components
    camera = Camera(device_id=0, width=1280, height=720)
    detector = ArucoDetector(marker_size_mm=100)
    warehouse = WarehouseMap(width_mm=2000, height_mm=3000)
    
    print("Vision Detection Example")
    print("-" * 40)
    
    try:
        with camera as cam:
            for frame_num in range(100):  # Process 100 frames
                
                # Capture frame
                frame = cam.read()
                if frame is None:
                    break
                
                # Detect markers
                markers = detector.detect(frame)
                
                if markers:
                    print(f"Frame {frame_num}: Detected {len(markers)} markers")
                    
                    for marker in markers:
                        print(f"  - Marker ID {marker.id} at {marker.position}")
                        warehouse.set_robot_position(marker.id, marker.position)
                
                # Limit to 10 frames for example
                if frame_num >= 10:
                    break
        
        # Print detection statistics
        stats = detector.get_detection_stats()
        print(f"\nDetection Statistics:")
        print(f"  Frames processed: {stats['frame_count']}")
        print(f"  Total markers detected: {stats['markers_detected']}")
        print(f"  Average detections: {stats['markers_detected']/max(stats['frame_count'], 1):.2f} per frame")
    
    finally:
        print("\nVision processing complete")


def example_motor_control():
    """
    Example showing motor control patterns:
    1. Initialize motor controller
    2. Ramp speed
    3. Apply directions
    4. Monitor current
    
    Note: This is a simulation example (no real hardware)
    """
    
    print("Motor Control Example (Simulated)")
    print("-" * 40)
    
    from firmware.pid_controller import PIDController
    
    # Create PID controller for speed regulation
    speed_pid = PIDController(
        kp=1.0,
        ki=0.01,
        kd=0.05,
        setpoint=100,  # Target speed (PWM units)
        update_rate_hz=50
    )
    
    print(f"PID Controller initialized:")
    print(f"  Kp={speed_pid.getProportionalTerm()}")
    print(f"  Ki={speed_pid.getIntegralTerm()}")
    print(f"  Kd={speed_pid.getDerivativeTerm()}")
    
    # Simulate speed control loop
    actual_speed = 0  # Start from rest
    
    for timestep in range(100):
        
        # Simulate acceleration with friction
        control_output = speed_pid.update(actual_speed)
        actual_speed += control_output * 0.5  # Proportional to control signal
        actual_speed *= 0.98  # Friction/drag
        
        if timestep % 10 == 0:
            print(f"Step {timestep:3d}: Target=100, Actual={actual_speed:6.1f}, "
                  f"Output={control_output:7.2f}")
    
    print(f"\nFinal speed: {actual_speed:.1f} PWM units")
    print(f"Settling time: ~{speed_pid.getDerivativeTerm():.0f} steps")


if __name__ == '__main__':
    
    print("=" * 50)
    print("Swarm Robot Examples")
    print("=" * 50)
    
    # Run examples
    # Uncomment to run specific examples:
    
    # example_basic_movement()
    # example_vision_detection()
    # example_motor_control()
    
    print("\nAvailable examples:")
    print("  1. example_basic_movement() - Gateway and communication")
    print("  2. example_vision_detection() - Camera and ArUco detection")
    print("  3. example_motor_control() - Speed regulation with PID")
    print("\nUncomment desired example in main() to run")
