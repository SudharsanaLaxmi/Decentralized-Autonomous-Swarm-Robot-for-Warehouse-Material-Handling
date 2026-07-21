"""
Utility functions for vision module
"""

import numpy as np
from typing import Tuple


def normalize_image(image: np.ndarray, method: str = 'minmax') -> np.ndarray:
    """
    Normalize image values to 0-1 or 0-255 range.
    
    Args:
        image: Input image array
        method: 'minmax' or 'zscore'
        
    Returns:
        Normalized image
    """
    if method == 'minmax':
        img_min = image.min()
        img_max = image.max()
        if img_max - img_min == 0:
            return image
        return (image - img_min) / (img_max - img_min)
    elif method == 'zscore':
        return (image - image.mean()) / image.std()
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """
    Crop rectangular region from image.
    
    Args:
        image: Input image
        x, y: Top-left corner
        width, height: Region size
        
    Returns:
        Cropped image region
    """
    return image[y:y+height, x:x+width]


def resize_image(image: np.ndarray, width: int, height: int,
                 interpolation: int = None) -> np.ndarray:
    """
    Resize image to specified dimensions.
    
    Args:
        image: Input image
        width, height: Target size
        interpolation: OpenCV interpolation method
        
    Returns:
        Resized image
    """
    import cv2
    if interpolation is None:
        interpolation = cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interpolation)


def get_image_center(image: np.ndarray) -> Tuple[float, float]:
    """Get center point of image."""
    height, width = image.shape[:2]
    return (width / 2.0, height / 2.0)


def distance_between_points(p1: Tuple[float, float],
                            p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
