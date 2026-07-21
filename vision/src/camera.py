"""
Camera Module - Capture, calibration, and frame processing

Handles camera initialization, frame capture, calibration,
and distortion correction for reliable vision processing.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import yaml
import logging

logger = logging.getLogger(__name__)


class Camera:
    """
    Interface to USB or integrated camera with calibration support.
    
    Attributes:
        camera_id: Camera device ID (0 for default)
        frame_height: Captured frame height in pixels
        frame_width: Captured frame width in pixels
        fps: Frames per second
    """
    
    def __init__(self, camera_id: int = 0, frame_width: int = 1280,
                 frame_height: int = 720, fps: int = 30):
        """
        Initialize camera interface.
        
        Args:
            camera_id: OpenCV camera device ID (0 for default)
            frame_width: Capture resolution width (pixels)
            frame_height: Capture resolution height (pixels)
            fps: Desired capture frame rate
        """
        self.camera_id = camera_id
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        
        # Camera parameters
        self.camera_matrix = None
        self.dist_coeffs = None
        self.calibrated = False
        
        # Initialize camera
        self.cap = cv2.VideoCapture(camera_id)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {camera_id}")
        
        # Configure camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize latency
        
        logger.info(f"Camera {camera_id} initialized: {frame_width}x{frame_height}@{fps}fps")
    
    def read(self) -> Optional[np.ndarray]:
        """
        Capture and return next frame.
        
        Returns:
            BGR image array or None if capture failed
            
        Raises:
            RuntimeError: Camera read error
        """
        ret, frame = self.cap.read()
        if not ret:
            logger.error("Failed to read frame from camera")
            return None
        
        # Apply calibration if available
        if self.calibrated and self.camera_matrix is not None:
            frame = self.undistort(frame)
        
        return frame
    
    def undistort(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply distortion correction to frame.
        
        Args:
            frame: Input BGR image
            
        Returns:
            Undistorted BGR image
        """
        if not self.calibrated:
            logger.warning("Camera not calibrated - returning original frame")
            return frame
        
        undistorted = cv2.undistort(frame, self.camera_matrix,
                                    self.dist_coeffs, None,
                                    self.camera_matrix)
        return undistorted
    
    def calibrate_from_file(self, calibration_file: str) -> bool:
        """
        Load calibration parameters from YAML file.
        
        Args:
            calibration_file: Path to calibration.yaml
            
        Returns:
            True if calibration loaded successfully
        """
        try:
            with open(calibration_file, 'r') as f:
                calib_data = yaml.safe_load(f)
            
            self.camera_matrix = np.array(calib_data['camera_matrix'])
            self.dist_coeffs = np.array(calib_data['dist_coeffs'])
            self.calibrated = True
            
            logger.info(f"Camera calibration loaded from {calibration_file}")
            logger.info(f"Reprojection error: {calib_data.get('calibration_error', 'unknown')}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to load calibration: {e}")
            return False
    
    def save_calibration(self, output_file: str) -> bool:
        """
        Save current calibration parameters to YAML.
        
        Args:
            output_file: Output calibration.yaml path
            
        Returns:
            True if saved successfully
        """
        if not self.calibrated:
            logger.warning("No calibration to save")
            return False
        
        try:
            calib_data = {
                'camera_matrix': self.camera_matrix.tolist(),
                'dist_coeffs': self.dist_coeffs.tolist(),
                'image_width': self.frame_width,
                'image_height': self.frame_height,
                'camera_id': self.camera_id,
            }
            
            with open(output_file, 'w') as f:
                yaml.dump(calib_data, f, default_flow_style=False)
            
            logger.info(f"Calibration saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save calibration: {e}")
            return False
    
    def get_frame_info(self) -> dict:
        """
        Get current camera configuration.
        
        Returns:
            Dict with camera properties
        """
        return {
            'camera_id': self.camera_id,
            'width': self.frame_width,
            'height': self.frame_height,
            'fps': self.fps,
            'calibrated': self.calibrated,
        }
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            logger.info(f"Camera {self.camera_id} released")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
    
    def __repr__(self) -> str:
        return (f"Camera(id={self.camera_id}, {self.frame_width}x{self.frame_height}, "
                f"calibrated={self.calibrated})")
