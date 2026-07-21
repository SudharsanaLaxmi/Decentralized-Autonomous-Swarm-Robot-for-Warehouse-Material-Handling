"""
Pose estimation from ArUco markers

Estimates robot position and orientation using ArUco marker detection
and pose estimation algorithms.
"""

import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class PoseEstimator:
    """
    Estimates 3D pose (position and orientation) from ArUco markers.
    
    Uses cv2.solvePnP with marker corners and known marker size
    to calculate 6-DOF pose.
    """
    
    def __init__(self, camera_matrix: np.ndarray, dist_coeffs: np.ndarray,
                 marker_size_m: float = 0.1):
        """
        Initialize pose estimator.
        
        Args:
            camera_matrix: Camera intrinsic parameters
            dist_coeffs: Camera distortion coefficients
            marker_size_m: Physical marker size in meters
        """
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.marker_size = marker_size_m
    
    def estimate_single_marker_pose(self, corners: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimate pose from single ArUco marker.
        
        Args:
            corners: 4 marker corner points (4, 2)
            
        Returns:
            (rvec, tvec) - Rotation and translation vectors
        """
        # 3D model points of marker (in marker frame)
        half_size = self.marker_size / 2.0
        object_points = np.array([
            [-half_size, half_size, 0],
            [half_size, half_size, 0],
            [half_size, -half_size, 0],
            [-half_size, -half_size, 0]
        ], dtype=np.float32)
        
        # 2D image points  
        image_points = corners.astype(np.float32)
        
        # Solve PnP
        import cv2
        success, rvec, tvec = cv2.solvePnP(
            object_points, image_points,
            self.camera_matrix, self.dist_coeffs,
            useExtrinsicGuess=False,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if not success:
            logger.warning("solvePnP failed")
            return None, None
        
        return rvec, tvec
    
    def get_robot_position(self, rvec: np.ndarray, tvec: np.ndarray) -> Tuple[float, float, float]:
        """
        Extract XYZ position from pose vectors.
        
        Args:
            rvec: Rotation vector
            tvec: Translation vector
            
        Returns:
            (x, y, z) position in meters
        """
        return float(tvec[0][0]), float(tvec[1][0]), float(tvec[2][0])
    
    def get_robot_orientation_euler(self, rvec: np.ndarray) -> Tuple[float, float, float]:
        """
        Extract Euler angles (roll, pitch, yaw) from rotation vector.
        
        Args:
            rvec: Rotation vector
            
        Returns:
            (roll, pitch, yaw) in radians
        """
        import cv2
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        
        # Extract Euler angles from rotation matrix
        # Using ZYX convention
        sy = np.sqrt(rotation_matrix[0, 0]**2 + rotation_matrix[1, 0]**2)
        singular = sy < 1e-6
        
        if not singular:
            x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            y = np.arctan2(-rotation_matrix[2, 0], sy)
            z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        else:
            x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
            y = np.arctan2(-rotation_matrix[2, 0], sy)
            z = 0
        
        return float(x), float(y), float(z)
