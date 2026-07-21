"""
ArUco Marker Detection

Detects, identifies, and localizes ArUco fiducial markers
in video frames for robot localization.
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ArucoMarker:
    """Single detected ArUco marker."""
    id: int
    position: np.ndarray  # 2D center position (x, y)
    corners: np.ndarray   # 4 corners of marker (N, 2)
    rvec: Optional[np.ndarray] = None  # Rotation vector (if pose estimated)
    tvec: Optional[np.ndarray] = None  # Translation vector (if pose estimated)
    confidence: float = 1.0


class ArucoDetector:
    """
    Detects and tracks ArUco markers in video frames.
    
    Supports the 5x5 bit ArUco dictionary with 250 unique markers.
    Uses OpenCV's cv2.aruco module for fast, reliable detection.
    """
    
    # ArUco 5x5bit dictionary (250 unique markers)
    ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    
    def __init__(self, marker_size_mm: float = 100.0):
        """
        Initialize ArUco detector.
        
        Args:
            marker_size_mm: Physical size of markers in millimeters
        """
        self.marker_size = marker_size_mm / 1000.0  # Convert to meters
        self.detector = cv2.aruco.ArucoDetector(self.ARUCO_DICT)
        self.detected_markers: List[ArucoMarker] = []
        self.frame_count = 0
    
    def detect(self, frame: np.ndarray) -> List[ArucoMarker]:
        """
        Detect ArUco markers in frame.
        
        Args:
            frame: BGR image frame
            
        Returns:
            List of detected ArucoMarker objects
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_count += 1
        
        # Detect markers
        corners, ids, rejected = self.detector.detectMarkers(gray)
        
        self.detected_markers = []
        
        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                marker_corners = corners[i][0]  # 4 corner points
                
                # Calculate marker center
                center_x = np.mean(marker_corners[:, 0])
                center_y = np.mean(marker_corners[:, 1])
                position = np.array([center_x, center_y])
                
                marker = ArucoMarker(
                    id=int(marker_id),
                    position=position,
                    corners=marker_corners,
                    confidence=1.0
                )
                self.detected_markers.append(marker)
                
                logger.debug(f"Detected marker {marker_id} at ({center_x:.1f}, {center_y:.1f})")
        
        if len(self.detected_markers) == 0:
            logger.debug("No markers detected in frame")
        
        return self.detected_markers
    
    def draw_markers(self, frame: np.ndarray, markers: Optional[List[ArucoMarker]] = None,
                    show_ids: bool = True, show_corners: bool = True) -> np.ndarray:
        """
        Draw detected markers on frame for visualization.
        
        Args:
            frame: Input BGR image
            markers: List of markers to draw (uses last detection if None)
            show_ids: Show marker IDs
            show_corners: Draw corner points
            
        Returns:
            Annotated frame
        """
        if markers is None:
            markers = self.detected_markers
        
        output = frame.copy()
        
        for marker in markers:
            corners = marker.corners.astype(int)
            
            # Draw marker outline
            cv2.polylines(output, [corners], True, (0, 255, 0), 2)
            
            # Draw corner points
            if show_corners:
                for pt in corners:
                    cv2.circle(output, tuple(pt), 3, (255, 0, 0), -1)
            
            # Draw marker center
            pos = tuple(marker.position.astype(int))
            cv2.circle(output, pos, 5, (0, 0, 255), -1)
            
            # Draw marker ID
            if show_ids:
                cv2.putText(output, f"ID:{marker.id}", pos,
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Add frame info
        cv2.putText(output, f"Frame: {self.frame_count} | Markers: {len(markers)}",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return output
    
    def get_marker_by_id(self, marker_id: int) -> Optional[ArucoMarker]:
        """
        Get specific marker by ID from last detection.
        
        Args:
            marker_id: Marker ID to find
            
        Returns:
            Marker object or None if not found
        """
        for marker in self.detected_markers:
            if marker.id == marker_id:
                return marker
        return None
    
    def get_detection_stats(self) -> dict:
        """
        Get detection statistics.
        
        Returns:
            Dict with detection metrics
        """
        return {
            'frame_count': self.frame_count,
            'markers_detected': len(self.detected_markers),
            'marker_ids': [m.id for m in self.detected_markers],
        }
    
    def reset_stats(self):
        """Reset frame counter and statistics."""
        self.frame_count = 0
        self.detected_markers = []
