"""
Homography-based coordinate transformation

Projects world coordinates to image coordinates and vice versa
using perspective transformation matrices.
"""

import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)


class Homography:
    """
    Computes and applies homography transformations between
    world and image coordinate frames.
    
    Useful for:
    - Converting pixel coordinates to warehouse coordinates
    - Mapping robot position to warehouse grid
    - Calculating distance to targets
    """
    
    def __init__(self):
        """Initialize homography matrix (identity by default)."""
        self.H = np.eye(3)  # Homography matrix
        self.H_inv = np.eye(3)  # Inverse homography
        self.is_initialized = False
    
    def compute_from_points(self, src_points: np.ndarray,
                           dst_points: np.ndarray) -> bool:
        """
        Compute homography from corresponding point pairs.
        
        Args:
            src_points: Source points (N, 2) in image space
            dst_points: Destination points (N, 2) in world space
            
        Returns:
            True if successful
        """
        if len(src_points) < 4:
            logger.error("Need at least 4 point correspondences")
            return False
        
        import cv2
        
        # Compute homography matrix
        H, mask = cv2.findHomography(src_points, dst_points)
        
        if H is None:
            logger.error("Failed to compute homography")
            return False
        
        self.H = H
        self.H_inv = np.linalg.inv(H)
        self.is_initialized = True
        
        logger.info("Homography matrix computed successfully")
        return True
    
    def image_to_world(self, image_point: Tuple[float, float]) -> Tuple[float, float]:
        """
        Transform point from image coordinates to world coordinates.
        
        Args:
            image_point: (x, y) in image space
            
        Returns:
            (x, y) in world space
        """
        if not self.is_initialized:
            logger.warning("Homography not initialized")
            return image_point
        
        # Create homogeneous coordinate
        point_h = np.array([image_point[0], image_point[1], 1], dtype=np.float32)
        
        # Apply homography
        world_h = self.H @ point_h
        
        # Normalize by homogeneous coordinate
        world_point = world_h[:2] / world_h[2]
        
        return float(world_point[0]), float(world_point[1])
    
    def world_to_image(self, world_point: Tuple[float, float]) -> Tuple[float, float]:
        """
        Transform point from world coordinates to image coordinates.
        
        Args:
            world_point: (x, y) in world space
            
        Returns:
            (x, y) in image space
        """
        if not self.is_initialized:
            logger.warning("Homography not initialized")
            return world_point
        
        # Create homogeneous coordinate
        point_h = np.array([world_point[0], world_point[1], 1], dtype=np.float32)
        
        # Apply inverse homography
        image_h = self.H_inv @ point_h
        
        # Normalize by homogeneous coordinate
        image_point = image_h[:2] / image_h[2]
        
        return float(image_point[0]), float(image_point[1])
    
    def batch_transform(self, points: np.ndarray, direction: str = 'image_to_world') -> np.ndarray:
        """
        Transform multiple points at once.
        
        Args:
            points: (N, 2) array of points
            direction: 'image_to_world' or 'world_to_image'
            
        Returns:
            Transformed points (N, 2)
        """
        H = self.H if direction == 'image_to_world' else self.H_inv
        
        # Add homogeneous coordinates
        ones = np.ones((points.shape[0], 1))
        points_h = np.hstack([points, ones])
        
        # Transform
        transformed_h = (H @ points_h.T).T
        
        # Normalize by homogeneous coordinate
        transformed = transformed_h[:, :2] / transformed_h[:, 2:3]
        
        return transformed
    
    def get_matrix(self) -> np.ndarray:
        """Get homography matrix."""
        return self.H.copy()
    
    def set_matrix(self, H: np.ndarray):
        """
        Set homography matrix directly.
        
        Args:
            H: 3x3 homography matrix
        """
        self.H = H
        self.H_inv = np.linalg.inv(H)
        self.is_initialized = True
