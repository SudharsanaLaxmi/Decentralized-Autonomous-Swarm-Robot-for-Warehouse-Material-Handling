"""
Robot Identification System

Manages unique robot IDs in the swarm and network addressing.
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Dict, Set
import logging

logger = logging.getLogger(__name__)


class RobotType(IntEnum):
    """Robot hardware type identifiers."""
    WAREHOUSE_BOT = 0x10
    CARRIER_BOT = 0x11
    SCOUT_BOT = 0x12
    LEADER_BOT = 0x13


@dataclass
class RobotIdentity:
    """
    Unique identification for each robot in swarm.
    
    Attributes:
        robot_id: Unique identifier (0-254, 255 reserved for broadcast)
        robot_type: Robot hardware type
        mac_address: ESP32 MAC address for ESP-NOW
        serial_number: Hardware serial number
        firmware_version: Currently running firmware version
    """
    robot_id: int
    robot_type: RobotType
    mac_address: str
    serial_number: str
    firmware_version: str
    
    def __post_init__(self):
        """Validate identity parameters."""
        if not (0 <= self.robot_id < 255):
            raise ValueError(f"robot_id must be 0-254, got {self.robot_id}")
        
        if not self._validate_mac(self.mac_address):
            raise ValueError(f"Invalid MAC address: {self.mac_address}")
    
    @staticmethod
    def _validate_mac(mac: str) -> bool:
        """Validate MAC address format."""
        parts = mac.split(':')
        return len(parts) == 6 and all(len(p) == 2 for p in parts)
    
    def to_bytes(self) -> bytes:
        """Serialize identity to bytes."""
        # Simplified representation: ID (1) + Type (1) + MAC (6)
        mac_bytes = bytes.fromhex(self.mac_address.replace(':', ''))
        return bytes([self.robot_id, self.robot_type]) + mac_bytes


class RobotRegistry:
    """
    Central registry for managing all robots in swarm.
    
    Tracks active robots, their status, and network connectivity.
    """
    
    BROADCAST_ID = 0xFF
    MAX_ROBOTS = 254
    
    def __init__(self):
        """Initialize empty registry."""
        self.robots: Dict[int, RobotIdentity] = {}
        self.active_robots: Set[int] = set()
        self.logger = logging.getLogger(__name__)
    
    def register_robot(self, identity: RobotIdentity) -> bool:
        """
        Register a new robot in the network.
        
        Args:
            identity: RobotIdentity object
            
        Returns:
            True if registration successful, False if ID already exists
        """
        if identity.robot_id in self.robots:
            self.logger.warning(f"Robot {identity.robot_id} already registered")
            return False
        
        if len(self.robots) >= self.MAX_ROBOTS:
            self.logger.error("Maximum robot limit reached")
            return False
        
        self.robots[identity.robot_id] = identity
        self.logger.info(f"Registered robot {identity.robot_id} ({identity.robot_type})")
        return True
    
    def mark_active(self, robot_id: int) -> bool:
        """Mark robot as active (connected)."""
        if robot_id not in self.robots:
            self.logger.warning(f"Unknown robot {robot_id}")
            return False
        
        self.active_robots.add(robot_id)
        return True
    
    def mark_inactive(self, robot_id: int) -> bool:
        """Mark robot as inactive (disconnected)."""
        self.active_robots.discard(robot_id)
        return True
    
    def get_robot(self, robot_id: int) -> Optional[RobotIdentity]:
        """Get robot identity by ID."""
        return self.robots.get(robot_id)
    
    def get_active_robots(self) -> list:
        """Get all active robot IDs."""
        return sorted(list(self.active_robots))
    
    def get_robots_by_type(self, robot_type: RobotType) -> list:
        """Get all robots of specific type."""
        return [rid for rid, identity in self.robots.items()
                if identity.robot_type == robot_type]
    
    def get_swarm_status(self) -> Dict:
        """Get current swarm status."""
        return {
            'total_robots': len(self.robots),
            'active_robots': len(self.active_robots),
            'by_type': {
                'warehouse_bot': len(self.get_robots_by_type(RobotType.WAREHOUSE_BOT)),
                'carrier_bot': len(self.get_robots_by_type(RobotType.CARRIER_BOT)),
                'scout_bot': len(self.get_robots_by_type(RobotType.SCOUT_BOT)),
                'leader_bot': len(self.get_robots_by_type(RobotType.LEADER_BOT)),
            }
        }
