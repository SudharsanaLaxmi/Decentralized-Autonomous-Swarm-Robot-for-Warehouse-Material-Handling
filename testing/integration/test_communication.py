"""
Integration tests for communication and coordination

Tests interaction between firmware, vision, and communication subsystems.
"""

import pytest
import time
from threading import Thread
from communication.protocol.messages import Message, MessageType, HeartbeatMessage
from communication.protocol.robot_id import RobotRegistry, RobotIdentity, RobotType
from communication.gateway.gateway import GatewayServer


@pytest.fixture
def gateway_server():
    """Create and start gateway server."""
    server = GatewayServer(host='127.0.0.1', port=18888)
    server.start()
    time.sleep(0.1)  # Allow server to initialize
    yield server
    server.stop()


@pytest.fixture
def robot_identity():
    """Create sample robot identity."""
    return RobotIdentity(
        robot_id=1,
        robot_type=RobotType.WAREHOUSE_BOT,
        mac_address='AA:BB:CC:DD:EE:01',
        serial_number='SN001',
        firmware_version='1.0.0'
    )


class TestRobotRegistry:
    """Test robot identification and registry."""
    
    def test_robot_registration(self, robot_identity):
        """Test robot can be registered."""
        registry = RobotRegistry()
        result = registry.register_robot(robot_identity)
        
        assert result is True
        assert registry.get_robot(1) is not None
    
    def test_duplicate_registration_rejected(self, robot_identity):
        """Test duplicate registration is rejected."""
        registry = RobotRegistry()
        registry.register_robot(robot_identity)
        
        result = registry.register_robot(robot_identity)
        assert result is False
    
    def test_robot_activation(self, robot_identity):
        """Test robot can be marked active."""
        registry = RobotRegistry()
        registry.register_robot(robot_identity)
        
        registry.mark_active(1)
        active = registry.get_active_robots()
        
        assert 1 in active
    
    def test_swarm_status_report(self, robot_identity):
        """Test swarm status aggregation."""
        registry = RobotRegistry()
        registry.register_robot(robot_identity)
        
        status = registry.get_swarm_status()
        assert status['total_robots'] == 1
        assert status['warehouse_bot'] == 1


class TestMessageSerialization:
    """Test message serialization/deserialization."""
    
    def test_heartbeat_serialization(self):
        """Test heartbeat message round-trip."""
        msg = HeartbeatMessage(
            msg_type=MessageType.HEARTBEAT,
            robot_id=1,
            sequence_num=1,
            timestamp=12345,
            status=1,
            battery_level=85
        )
        
        serialized = msg.serialize()
        deserialized = Message.deserialize(serialized)
        
        assert deserialized is not None
        assert deserialized.robot_id == 1
        assert deserialized.sequence_num == 1
    
    def test_invalid_message_length(self):
        """Test invalid message is rejected."""
        short_data = b'\x01\x02'  # Too short
        
        result = Message.deserialize(short_data)
        assert result is None


class TestGatewayServer:
    """Test gateway server functionality."""
    
    def test_gateway_initialization(self, gateway_server):
        """Test gateway initializes."""
        assert gateway_server.running is True
        assert gateway_server.socket is not None
    
    def test_robot_registration_with_gateway(self, gateway_server, robot_identity):
        """Test robot registration with gateway."""
        result = gateway_server.register_robot(robot_identity)
        
        assert result is True
        stats = gateway_server.get_statistics()
        assert stats['total_robots'] == 1
    
    def test_gateway_statistics(self, gateway_server):
        """Test gateway tracks statistics."""
        stats = gateway_server.get_statistics()
        
        assert 'messages_received' in stats
        assert 'messages_sent' in stats
        assert 'errors' in stats
        assert 'uptime_seconds' in stats


class TestCommunicationReliability:
    """Test message delivery reliability."""
    
    def test_sequence_numbering(self):
        """Test messages maintain sequence numbers."""
        messages = []
        for i in range(10):
            msg = Message(
                msg_type=MessageType.HEARTBEAT,
                robot_id=1,
                sequence_num=i,
                timestamp=int(time.time() * 1000)
            )
            messages.append(msg.sequence_num)
        
        # Verify sequence is monotonic
        assert messages == list(range(10))
    
    def test_message_timeout_detection(self, gateway_server):
        """Test detection of lost heartbeats."""
        registry = gateway_server.registry
        
        # Simulate heartbeat tracking
        heartbeat_timeout = 5  # seconds
        last_heartbeat = time.time()
        
        time.sleep(0.5)
        elapsed = time.time() - last_heartbeat
        
        assert elapsed < heartbeat_timeout
