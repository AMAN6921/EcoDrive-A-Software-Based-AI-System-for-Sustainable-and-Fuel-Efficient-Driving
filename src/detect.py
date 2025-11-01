"""
Vehicle Detection and Counting Module
Uses OpenCV for basic vehicle detection in traffic footage
"""

import cv2
import numpy as np
from typing import Tuple, List


class VehicleDetector:
    """Detects and counts vehicles in traffic footage using background subtraction"""
    
    def __init__(self, min_contour_area: int = 500):
        """
        Initialize the vehicle detector
        
        Args:
            min_contour_area: Minimum area to consider as a vehicle
        """
        self.min_contour_area = min_contour_area
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=100, varThreshold=40, detectShadows=True
        )
        
    def detect_vehicles(self, frame: np.ndarray) -> Tuple[int, np.ndarray]:
        """
        Detect vehicles in a frame
        
        Args:
            frame: Input video frame
            
        Returns:
            Tuple of (vehicle_count, annotated_frame)
        """
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Remove shadows (value 127 in MOG2)
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter and count vehicles
        vehicle_count = 0
        annotated_frame = frame.copy()
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                vehicle_count += 1
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    annotated_frame, f"Vehicle {vehicle_count}", 
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2
                )
        
        return vehicle_count, annotated_frame


def estimate_density(vehicle_count: int, frame_area: int) -> str:
    """
    Estimate traffic density level
    
    Args:
        vehicle_count: Number of vehicles detected
        frame_area: Total frame area in pixels
        
    Returns:
        Density level: 'LOW', 'MEDIUM', or 'HIGH'
    """
    # Simple vehicle count based thresholds
    if vehicle_count <= 2:
        return "LOW"
    elif vehicle_count <= 5:
        return "MEDIUM"
    else:
        return "HIGH"
