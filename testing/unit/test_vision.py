"""
Testing utility for vision module

Unit tests for camera, ArUco detection, and pose estimation.
"""

import pytest
import numpy as np
from vision.src.camera import Camera
from vision.src.aruco_detector import ArucoDetector, ArucoMarker


@pytest.fixture
def aruco_detector():
    """Create ArUco detector instance."""
    return ArucoDetector(marker_size_mm=100)


@pytest.fixture
def dummy_frame():
    """Create dummy BGR image frame."""
    return np.zeros((720, 1280, 3), dtype=np.uint8)


class TestArucoDetector:
    """Tests for ArUco marker detection."""
    
    def test_detector_initialization(self, aruco_detector):
        """Test detector can be initialized."""
        assert aruco_detector is not None
        assert aruco_detector.marker_size > 0
    
    def test_empty_frame_detection(self, aruco_detector, dummy_frame):
        """Test detection returns empty list on empty frame."""
        markers = aruco_detector.detect(dummy_frame)
        assert isinstance(markers, list)
        assert len(markers) == 0
    
    def test_detection_statistics(self, aruco_detector, dummy_frame):
        """Test statistics tracking."""
        aruco_detector.detect(dummy_frame)
        stats = aruco_detector.get_detection_stats()
        
        assert 'frame_count' in stats
        assert 'markers_detected' in stats
        assert stats['frame_count'] > 0
    
    def test_marker_reset(self, aruco_detector, dummy_frame):
        """Test statistics can be reset."""
        aruco_detector.detect(dummy_frame)
        aruco_detector.reset_stats()
        
        stats = aruco_detector.get_detection_stats()
        assert stats['frame_count'] == 0


class TestArucoMarker:
    """Tests for ArucoMarker dataclass."""
    
    def test_marker_creation(self):
        """Test marker can be created."""
        position = np.array([640, 360])
        corners = np.array([[620, 340], [660, 340], [660, 380], [620, 380]])
        
        marker = ArucoMarker(id=5, position=position, corners=corners)
        
        assert marker.id == 5
        assert marker.position is not None
        assert marker.confidence == 1.0
