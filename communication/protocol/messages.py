"""
Communication Protocol - Message Schema and Serialization

Defines message formats for ESP-NOW and UDP communication
between robots and gateway.
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Optional
import struct
import logging

logger = logging.getLogger(__name__)


class MessageType(IntEnum):
    """Message type identifiers."""
    HEARTBEAT = 0x01
    TELEMETRY = 0x02
    COMMAND = 0x03
    TASK = 0x04
    ACK = 0x05
    ERROR = 0x06


class RobotStatus(IntEnum):
    """Robot operational status."""
    IDLE = 0
    MOVING = 1
    WORKING = 2
    ERROR = 3
    CHARGING = 4


@dataclass
class Message:
    """
    Base message class for robot communication.
    
    Defines common message structure and serialization.
    """
    msg_type: MessageType
    robot_id: int
    sequence_num: int
    timestamp: int  # milliseconds
    payload: bytes = field(default_factory=bytes)
    
    HEADER_SIZE = 12  # bytes
    
    def serialize(self) -> bytes:
        """
        Serialize message to bytes for transmission.
        
        Format: [msg_type(1) | robot_id(1) | seq(2) | timestamp(4) | payload(...)]
        
        Returns:
            Serialized message bytes
        """
        header = struct.pack('>BBHI', self.msg_type, self.robot_id,
                           self.sequence_num, self.timestamp)
        return header + self.payload
    
    @staticmethod
    def deserialize(data: bytes) -> Optional['Message']:
        """
        Deserialize bytes into Message object.
        
        Args:
            data: Raw message bytes
            
        Returns:
            Message object or None if invalid
        """
        if len(data) < Message.HEADER_SIZE:
            logger.warning(f"Message too short: {len(data)} bytes")
            return None
        
        try:
            msg_type, robot_id, seq_num, timestamp = struct.unpack('>BBHI', data[:12])
            payload = data[12:]
            
            return Message(
                msg_type=MessageType(msg_type),
                robot_id=robot_id,
                sequence_num=seq_num,
                timestamp=timestamp,
                payload=payload
            )
        except struct.error as e:
            logger.error(f"Failed to deserialize message: {e}")
            return None


@dataclass
class HeartbeatMessage(Message):
    """Robot heartbeat for health monitoring."""
    status: RobotStatus = RobotStatus.IDLE
    battery_level: int = 0  # 0-100 %
    
    def serialize(self) -> bytes:
        """Serialize heartbeat with status and battery."""
        self.payload = struct.pack('>BB', self.status, self.battery_level)
        return super().serialize()


@dataclass
class TelemetryMessage(Message):
    """Robot telemetry data."""
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0  # radians
    battery_voltage: float = 0.0  # volts
    
    def serialize(self) -> bytes:
        """Serialize telemetry position and state."""
        self.payload = struct.pack('>ffff', self.x, self.y, self.theta,
                                   self.battery_voltage)
        return super().serialize()
