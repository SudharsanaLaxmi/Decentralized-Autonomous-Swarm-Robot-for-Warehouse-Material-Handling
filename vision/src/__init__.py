"""
Swarm Warehouse Robot - Computer Vision Module

Provides real-time computer vision capabilities for autonomous robot localization,
marker detection, and warehouse navigation using ArUco markers and homography
transformations.

Author: Robotics Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Robotics Team"
__all__ = [
    "Camera",
    "ArucoDetector",
    "PoseEstimator",
    "Homography",
    "WarehouseMap",
]

from .camera import Camera
from .aruco_detector import ArucoDetector
from .pose_estimator import PoseEstimator
from .homography import Homography
from .warehouse_map import WarehouseMap

__doc__ = """
Computer Vision Module for Swarm Warehouse Robot

This module provides:
- Real-time camera capture and calibration
- ArUco marker detection and tracking
- Pose estimation for robot localization
- Homography-based coordinate transformations
- Warehouse map representation and visualization

Example:
    >>> from vision import Camera, ArucoDetector
    >>> camera = Camera(camera_id=0)
    >>> detector = ArucoDetector()
    >>> frame = camera.read()
    >>> markers = detector.detect(frame)
"""
