"""
Warehouse map representation

Represents warehouse layout, obstacles, and robot positions
for planning and visualization.
"""

import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class WarehouseMap:
    """
    Represents warehouse layout with obstacles and navigation waypoints.
    
    Maintains:
    - Room/warehouse boundaries
    - Static obstacles (shelves, walls)
    - Robot positions
    - Target locations
    """
    
    def __init__(self, width_m: float, height_m: float):
        """
        Initialize warehouse map.
        
        Args:
            width_m: Warehouse width in meters
            height_m: Warehouse height in meters
        """
        self.width = width_m
        self.height = height_m
        self.obstacles: List[Tuple[float, float, float, float]] = []  # x, y, w, h
        self.waypoints: List[Tuple[float, float]] = []  # navigation points
        self.robot_positions: dict = {}  # robot_id -> (x, y, theta)
    
    def add_obstacle(self, x: float, y: float, width: float, height: float):
        """
        Add rectangular obstacle to map.
        
        Args:
            x, y: Obstacle center position
            width, height: Obstacle dimensions
        """
        self.obstacles.append((x, y, width, height))
        logger.debug(f"Added obstacle at ({x}, {y}), size {width}x{height}")
    
    def add_waypoint(self, x: float, y: float):
        """
        Add navigation waypoint.
        
        Args:
            x, y: Waypoint position
        """
        if 0 <= x <= self.width and 0 <= y <= self.height:
            self.waypoints.append((x, y))
            logger.debug(f"Added waypoint at ({x}, {y})")
        else:
            logger.warning(f"Waypoint ({x}, {y}) outside map bounds")
    
    def set_robot_position(self, robot_id: int, x: float, y: float, theta: float = 0.0):
        """
        Update robot position on map.
        
        Args:
            robot_id: Unique robot identifier
            x, y: Position in meters
            theta: Orientation in radians
        """
        self.robot_positions[robot_id] = (x, y, theta)
    
    def get_robot_position(self, robot_id: int) -> Optional[Tuple[float, float, float]]:
        """
        Get robot position.
        
        Args:
            robot_id: Robot identifier
            
        Returns:
            (x, y, theta) or None if not found
        """
        return self.robot_positions.get(robot_id)
    
    def is_point_in_obstacle(self, x: float, y: float, margin: float = 0.1) -> bool:
        """
        Check if point is within any obstacle (with margin).
        
        Args:
            x, y: Point position
            margin: Safety margin around obstacles
            
        Returns:
            True if point is in obstacle
        """
        for obs_x, obs_y, obs_w, obs_h in self.obstacles:
            if (abs(x - obs_x) < obs_w/2 + margin and
                abs(y - obs_y) < obs_h/2 + margin):
                return True
        return False
    
    def clear(self):
        """Clear all obstacles and waypoints."""
        self.obstacles.clear()
        self.waypoints.clear()
        self.robot_positions.clear()
