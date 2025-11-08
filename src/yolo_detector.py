"""
Real YOLO-based Vehicle Detection Module
Uses YOLOv8 for accurate vehicle detection in traffic footage
"""

import cv2
import numpy as np
from typing import Tuple, List, Dict
from ultralytics import YOLO
import torch


class YOLOVehicleDetector:
    """Real-time vehicle detection using YOLOv8"""
    
    # Vehicle class IDs in COCO dataset
    VEHICLE_CLASSES = {
        2: 'car',
        3: 'motorcycle', 
        5: 'bus',
        7: 'truck'
    }
    
    def __init__(self, model_size: str = 'n', confidence: float = 0.5):
        """
        Initialize YOLO detector
        
        Args:
            model_size: YOLOv8 model size ('n', 's', 'm', 'l', 'x')
            confidence: Confidence threshold for detections
        """
        self.confidence = confidence
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        print(f"🚀 Loading YOLOv8{model_size} model on {self.device}...")
        self.model = YOLO(f'yolov8{model_size}.pt')
        self.model.to(self.device)
        print("✅ Model loaded successfully")
        
    def detect_vehicles(self, frame: np.ndarray) -> Tuple[int, np.ndarray, List[Dict]]:
        """
        Detect vehicles in a frame using YOLO
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            Tuple of (vehicle_count, annotated_frame, detections_list)
        """
        # Run YOLO inference
        results = self.model(frame, conf=self.confidence, verbose=False)[0]
        
        detections = []
        annotated_frame = frame.copy()
        vehicle_count = 0
        
        # Process detections
        for box in results.boxes:
            class_id = int(box.cls[0])
            
            # Filter only vehicle classes
            if class_id in self.VEHICLE_CLASSES:
                vehicle_count += 1
                
                # Extract box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                vehicle_type = self.VEHICLE_CLASSES[class_id]
                
                # Store detection info
                detections.append({
                    'type': vehicle_type,
                    'confidence': conf,
                    'bbox': (x1, y1, x2, y2),
                    'center': ((x1 + x2) // 2, (y1 + y2) // 2)
                })
                
                # Draw bounding box
                color = self._get_color(vehicle_type)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Add label
                label = f"{vehicle_type} {conf:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(
                    annotated_frame, 
                    (x1, y1 - label_size[1] - 10), 
                    (x1 + label_size[0], y1), 
                    color, -1
                )
                cv2.putText(
                    annotated_frame, label, 
                    (x1, y1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (255, 255, 255), 2
                )
        
        return vehicle_count, annotated_frame, detections
    
    def _get_color(self, vehicle_type: str) -> Tuple[int, int, int]:
        """Get color for vehicle type"""
        colors = {
            'car': (0, 255, 0),      # Green
            'motorcycle': (255, 0, 0),  # Blue
            'bus': (0, 165, 255),    # Orange
            'truck': (0, 0, 255)     # Red
        }
        return colors.get(vehicle_type, (255, 255, 255))


def estimate_density(vehicle_count: int, frame_area: int = None) -> Tuple[str, float]:
    """
    Estimate traffic density level with score
    
    Args:
        vehicle_count: Number of vehicles detected
        frame_area: Total frame area (optional, for density ratio)
        
    Returns:
        Tuple of (density_level, density_score)
    """
    # Calculate density score (0-1 scale)
    density_score = min(vehicle_count / 20.0, 1.0)  # Normalize to 20 vehicles max
    
    # Classify density
    if vehicle_count <= 3:
        density_level = "LOW"
    elif vehicle_count <= 8:
        density_level = "MEDIUM"
    elif vehicle_count <= 15:
        density_level = "HIGH"
    else:
        density_level = "CRITICAL"
    
    return density_level, density_score
