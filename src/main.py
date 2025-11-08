"""
Main Traffic Flow Optimization System
Integrates YOLO detection with ML-based signal optimization
"""

import cv2
import numpy as np
import argparse
from pathlib import Path
import time
from yolo_detector import YOLOVehicleDetector, estimate_density
from optimize import TrafficSignalOptimizer


class TrafficOptimizationSystem:
    """Complete traffic optimization system"""
    
    def __init__(self, model_size: str = 'n', confidence: float = 0.5):
        """Initialize the system"""
        print("🚦 Initializing Traffic Optimization System...")
        self.detector = YOLOVehicleDetector(model_size=model_size, confidence=confidence)
        self.optimizer = TrafficSignalOptimizer()
        self.frame_count = 0
        self.total_vehicles = 0
        self.total_fuel_saved = 0.0
        self.total_co2_saved = 0.0
        
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame"""
        self.frame_count += 1
        
        # Detect vehicles
        vehicle_count, annotated_frame, detections = self.detector.detect_vehicles(frame)
        self.total_vehicles += vehicle_count
        
        # Estimate density
        density_level, density_score = estimate_density(vehicle_count)
        
        # Calculate optimal signal timing
        timing = self.optimizer.calculate_optimal_timing(vehicle_count, density_score)
        
        # Estimate savings
        savings = self.optimizer.estimate_fuel_savings(vehicle_count, timing.green_duration)
        self.total_fuel_saved += savings['fuel_saved_liters']
        self.total_co2_saved += savings['co2_saved_kg']
        
        # Add comprehensive overlay
        self._add_overlay(annotated_frame, vehicle_count, density_level, 
                         density_score, timing, savings)
        
        return annotated_frame
    
    def _add_overlay(self, frame, vehicle_count, density_level, density_score, 
                    timing, savings):
        """Add information overlay to frame"""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (450, 280), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Title
        cv2.putText(frame, "AI Traffic Optimization System", 
                   (20, 35), cv2.FONT_HERSHEY_BOLD, 0.7, (0, 255, 255), 2)
        
        # Detection info
        y_pos = 65
        cv2.putText(frame, f"Vehicles Detected: {vehicle_count}", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        y_pos += 30
        density_color = self._get_density_color(density_level)
        cv2.putText(frame, f"Traffic Density: {density_level} ({density_score:.2f})", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, density_color, 2)
        
        # Signal timing
        y_pos += 40
        cv2.putText(frame, "Optimized Signal Timing:", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        y_pos += 25
        cv2.putText(frame, f"  Green: {timing.green_duration:.0f}s", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        y_pos += 25
        cv2.putText(frame, f"  Yellow: {timing.yellow_duration:.0f}s", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        # Savings estimate
        y_pos += 35
        cv2.putText(frame, "Estimated Savings (this cycle):", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        y_pos += 25
        cv2.putText(frame, f"  Fuel: {savings['fuel_saved_liters']:.3f} L", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        y_pos += 25
        cv2.putText(frame, f"  CO2: {savings['co2_saved_kg']:.3f} kg", 
                   (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Frame counter
        cv2.putText(frame, f"Frame: {self.frame_count}", 
                   (w - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    def _get_density_color(self, density_level: str):
        """Get color based on density level"""
        colors = {
            'LOW': (0, 255, 0),
            'MEDIUM': (0, 255, 255),
            'HIGH': (0, 165, 255),
            'CRITICAL': (0, 0, 255)
        }
        return colors.get(density_level, (255, 255, 255))
    
    def run_video(self, video_path: str, output_path: str = None):
        """Process video file"""
        print(f"\n🎥 Processing video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ Error: Could not open video: {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📊 Video: {width}x{height} @ {fps}fps, {total_frames} frames")
        
        # Setup video writer if output specified
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"💾 Saving output to: {output_path}")
        
        print("\n▶️  Processing... (Press 'q' to quit)")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            processed_frame = self.process_frame(frame)
            
            # Write to output
            if writer:
                writer.write(processed_frame)
            
            # Display
            cv2.imshow("Traffic Optimization System", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n⏸️  Stopped by user")
                break
        
        # Cleanup
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        
        self._print_summary()
    
    def run_webcam(self):
        """Process webcam feed"""
        print("\n📹 Starting webcam feed...")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        print("▶️  Processing... (Press 'q' to quit)")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame(frame)
            cv2.imshow("Traffic Optimization System", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        self._print_summary()
    
    def _print_summary(self):
        """Print processing summary"""
        print("\n" + "="*60)
        print("📊 PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Frames Processed: {self.frame_count}")
        print(f"Total Vehicles Detected: {self.total_vehicles}")
        print(f"Average Vehicles/Frame: {self.total_vehicles/self.frame_count:.1f}")
        print(f"\n💰 Estimated Total Savings:")
        print(f"  Fuel: {self.total_fuel_saved:.2f} liters")
        print(f"  CO2: {self.total_co2_saved:.2f} kg")
        print("\n📈 Optimization Statistics:")
        stats = self.optimizer.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("="*60)
        
        # Save history
        self.optimizer.save_history()


def main():
    parser = argparse.ArgumentParser(description='AI Traffic Flow Optimization System')
    parser.add_argument('--source', type=str, default='webcam',
                       help='Video source: "webcam" or path to video file')
    parser.add_argument('--output', type=str, default=None,
                       help='Output video path (optional)')
    parser.add_argument('--model', type=str, default='n',
                       choices=['n', 's', 'm', 'l', 'x'],
                       help='YOLOv8 model size (n=nano, s=small, m=medium, l=large, x=xlarge)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Detection confidence threshold (0-1)')
    
    args = parser.parse_args()
    
    # Initialize system
    system = TrafficOptimizationSystem(model_size=args.model, confidence=args.confidence)
    
    # Run based on source
    if args.source.lower() == 'webcam':
        system.run_webcam()
    else:
        if not Path(args.source).exists():
            print(f"❌ Error: Video file not found: {args.source}")
            return
        system.run_video(args.source, args.output)


if __name__ == "__main__":
    main()
