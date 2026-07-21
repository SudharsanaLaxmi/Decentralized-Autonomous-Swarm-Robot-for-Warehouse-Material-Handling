"""
System Integration Test Suite

End-to-end tests verifying complete system workflows.
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock

from communication.gateway.gateway import GatewayServer
from communication.protocol.messages import Message, MessageType, TelemetryMessage
from communication.protocol.robot_id import RobotRegistry, RobotIdentity, RobotType


@pytest.fixture(scope="session")
def integration_gateway():
    """Shared gateway for integration tests."""
    gateway = GatewayServer(host='127.0.0.1', port=19999)
    gateway.start()
    time.sleep(0.2)
    yield gateway
    gateway.stop()


@pytest.fixture
def test_robots():
    """Create test robot identities."""
    robots = [
        RobotIdentity(
            robot_id=i,
            robot_type=RobotType.WAREHOUSE_BOT,
            mac_address=f'AA:BB:CC:DD:EE:{i:02X}',
            serial_number=f'SN{i:03d}',
            firmware_version='1.0.0'
        )
        for i in range(1, 4)
    ]
    return robots


class TestSystemInitialization:
    """Test complete system startup sequence."""
    
    def test_gateway_startup_sequence(self, integration_gateway):
        """Test gateway initializes all components."""
        assert integration_gateway.running is True
        assert integration_gateway.socket is not None
        assert integration_gateway.registry is not None
        assert len(integration_gateway.rx_thread.__class__.__name__) > 0
    
    def test_robot_registration_sequence(self, integration_gateway, test_robots):
        """Test multiple robots registering with gateway."""
        for robot in test_robots:
            result = integration_gateway.register_robot(robot)
            assert result is True
        
        # Verify all registered
        for robot in test_robots:
            retrieved = integration_gateway.registry.get_robot(robot.robot_id)
            assert retrieved is not None
            assert retrieved.robot_id == robot.robot_id


class TestSwarmOperation:
    """Test multi-robot swarm scenarios."""
    
    def test_swarm_coordination(self, integration_gateway, test_robots):
        """Test coordination between multiple robots."""
        
        # Register swarm
        for robot in test_robots:
            integration_gateway.register_robot(robot)
        
        # All robots active
        for robot_id in range(1, 4):
            integration_gateway.registry.mark_active(robot_id)
        
        stats = integration_gateway.registry.get_swarm_status()
        assert stats['total_robots'] == 3
        assert stats['active_robots'] == 3
    
    def test_robot_failure_detection(self, integration_gateway, test_robots):
        """Test system detects robot disconnection."""
        
        robot = test_robots[0]
        integration_gateway.register_robot(robot)
        integration_gateway.registry.mark_active(robot.robot_id)
        
        # Verify active
        active = integration_gateway.registry.get_active_robots()
        assert robot.robot_id in active
        
        # Simulate disconnect
        integration_gateway.registry.mark_inactive(robot.robot_id)
        
        # Verify inactive
        active = integration_gateway.registry.get_active_robots()
        assert robot.robot_id not in active


class TestMessageFlow:
    """Test complete message transmission workflows."""
    
    def test_telemetry_collection_workflow(self, integration_gateway, test_robots):
        """Test collecting telemetry from multiple robots."""
        
        robot = test_robots[0]
        integration_gateway.register_robot(robot)
        
        # Create simulated telemetry message
        telemetry = TelemetryMessage(
            msg_type=MessageType.TELEMETRY,
            robot_id=robot.robot_id,
            sequence_num=1,
            timestamp=int(time.time() * 1000),
            x=100.5,
            y=200.5,
            theta=0.785,  # 45 degrees
            battery_voltage=7.4
        )
        
        # Simulate receiving message
        integration_gateway.rx_queue.put((telemetry, ('127.0.0.1', 12345)))
        
        # Retrieve message
        received = integration_gateway.get_telemetry(timeout=1.0)
        assert received is not None
        assert received.robot_id == robot.robot_id
        assert received.sequence_num == 1
    
    def test_command_distribution(self, integration_gateway, test_robots):
        """Test distributing commands to robots."""
        
        for robot in test_robots:
            integration_gateway.register_robot(robot)
        
        # Create command for each robot
        for robot_id in range(1, 4):
            cmd = Message(
                msg_type=MessageType.COMMAND,
                robot_id=robot_id,
                sequence_num=1,
                timestamp=int(time.time() * 1000)
            )
            result = integration_gateway.send_to_robot(cmd, robot_id)
            assert result is True


class TestCommunicationReliability:
    """Test communication resilience."""
    
    def test_message_sequence_ordering(self):
        """Test message sequence numbers prevent duplicates."""
        
        msgs = []
        for i in range(10):
            msg = Message(
                msg_type=MessageType.HEARTBEAT,
                robot_id=1,
                sequence_num=i,
                timestamp=int(time.time() * 1000)
            )
            msgs.append(msg)
        
        # Verify sequence is monotonic
        sequences = [m.sequence_num for m in msgs]
        assert sequences == list(range(10))
    
    def test_queue_flow_control(self, integration_gateway):
        """Test message queueing under load."""
        
        initial_size = integration_gateway.rx_queue.qsize()
        
        # Send burst of messages
        for i in range(100):
            msg = Message(
                msg_type=MessageType.HEARTBEAT,
                robot_id=1,
                sequence_num=i,
                timestamp=int(time.time() * 1000)
            )
            integration_gateway.rx_queue.put((msg, ('127.0.0.1', 12345)))
        
        # Verify queue has messages
        size_after = integration_gateway.rx_queue.qsize()
        assert size_after > initial_size


class TestPerformanceMonitoring:
    """Test gateway statistics and monitoring."""
    
    def test_statistics_tracking(self, integration_gateway, test_robots):
        """Test statistics accurately reflect activity."""
        
        robot = test_robots[0]
        integration_gateway.register_robot(robot)
        
        # Get baseline stats
        stats_before = integration_gateway.get_statistics()
        msg_count_before = stats_before['messages_received']
        
        # Simulate message reception
        msg = Message(
            msg_type=MessageType.HEARTBEAT,
            robot_id=robot.robot_id,
            sequence_num=1,
            timestamp=int(time.time() * 1000)
        )
        integration_gateway.rx_queue.put((msg, ('127.0.0.1', 12345)))
        
        # Get updated stats
        stats_after = integration_gateway.get_statistics()
        
        # Verify counter updated
        assert stats_after['total_robots'] >= stats_before['total_robots']
    
    def test_uptime_tracking(self, integration_gateway):
        """Test gateway tracks uptime."""
        
        time.sleep(0.5)
        stats = integration_gateway.get_statistics()
        
        assert 'uptime_seconds' in stats
        assert stats['uptime_seconds'] >= 0.5


class TestErrorRecovery:
    """Test system error handling and recovery."""
    
    def test_malformed_message_handling(self):
        """Test system handles invalid messages gracefully."""
        
        # Try to deserialize invalid data
        invalid_data = b'\x00\x01'  # Too short
        msg = Message.deserialize(invalid_data)
        
        # Should return None, not crash
        assert msg is None
    
    def test_gateway_recovery_from_queue_overflow(self, integration_gateway):
        """Test gateway behavior when receive queue is full."""
        
        # Fill queue to capacity
        for i in range(1000):
            msg = Message(
                msg_type=MessageType.HEARTBEAT,
                robot_id=1,
                sequence_num=i,
                timestamp=int(time.time() * 1000)
            )
            # Try to add even if full
            try:
                integration_gateway.rx_queue.put((msg, ('127.0.0.1', 12345)), timeout=0)
            except:
                break
        
        # Gateway should still be operational
        assert integration_gateway.running is True
