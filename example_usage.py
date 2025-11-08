"""
Example Usage of Traffic Optimization System
Demonstrates how to use the system programmatically
"""

import sys
from pathlib import Path
import cv2
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from yolo_detector import YOLOVehicleDetector, estimate_density
from optimize import TrafficSignalOptimizer


def example_1_basic_detection():
    """Example 1: Basic vehicle detection on an image"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Vehicle Detection")
    print("="*60)
    
    # Initialize detector
    detector = YOLOVehicleDetector(model_size='n', confidence=0.5)
    
    # Load an image (or create synthetic one)
    # For demo, create a blank image
    img = np.ones((480, 640, 3), dtype=np.uint8) * 100
    
    # Detect vehicles
    vehicle_count, annotated_img, detections = detector.detect_vehicles(img)
    
    print(f"✅ Detected {vehicle_count} vehicles")
    for i, det in enumerate(detections, 1):
        print(f"   Vehicle {i}: {det['type']} (confidence: {det['confidence']:.2f})")
    
    return vehicle_count, detections


def example_2_signal_optimization():
    """Example 2: Calculate optimal signal timing"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Signal Timing Optimization")
    print("="*60)
    
    # Initialize optimizer
    optimizer = TrafficSignalOptimizer(
        min_green=10.0,
        max_green=90.0,
        base_green=30.0
    )
    
    # Test different traffic scenarios
    scenarios = [
        (2, "Light traffic"),
        (5, "Moderate traffic"),
        (10, "Heavy traffic"),
        (20, "Very heavy traffic")
    ]
    
    for vehicle_count, description in scenarios:
        # Estimate density
        density_level, density_score = estimate_density(vehicle_count)
        
        # Calculate optimal timing
        timing = optimizer.calculate_optimal_timing(vehicle_count, density_score)
        
        # Estimate savings
        savings = optimizer.estimate_fuel_savings(vehicle_count, timing.green_duration)
        
        print(f"\n{description} ({vehicle_count} vehicles):")
        print(f"  Density: {density_level} (score: {density_score:.2f})")
        print(f"  Green light: {timing.green_duration}s")
        print(f"  Fuel saved: {savings['fuel_saved_liters']:.3f} L")
        print(f"  CO2 saved: {savings['co2_saved_kg']:.3f} kg")


def example_3_multi_lane():
    """Example 3: Multi-lane intersection optimization"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-Lane Intersection")
    print("="*60)
    
    optimizer = TrafficSignalOptimizer()
    
    # Simulate 4-way intersection
    lane_densities = {
        'North': (8, 0.4),   # (vehicle_count, density_score)
        'South': (12, 0.6),
        'East': (5, 0.25),
        'West': (15, 0.75)
    }
    
    # Calculate timings for all lanes
    timings = optimizer.calculate_multi_lane_timing(lane_densities)
    
    print("\n4-Way Intersection Signal Timings:")
    print("-" * 60)
    
    total_cycle = 0
    for lane, timing in timings.items():
        vehicles, density = lane_densities[lane]
        print(f"\n{lane} Lane ({vehicles} vehicles):")
        print(f"  Green:  {timing.green_duration}s")
        print(f"  Yellow: {timing.yellow_duration}s")
        print(f"  Red:    {timing.red_duration}s")
        total_cycle = max(total_cycle, 
                         timing.green_duration + timing.yellow_duration + timing.red_duration)
    
    print(f"\nTotal cycle time: {total_cycle}s")


def example_4_process_video():
    """Example 4: Process video file (if available)"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Video Processing")
    print("="*60)
    
    # This is a template - requires actual video file
    video_path = "sample_traffic.mp4"
    
    if not Path(video_path).exists():
        print(f"⚠️  Video file not found: {video_path}")
        print("   To test video processing:")
        print("   1. Download a traffic video")
        print("   2. Save it as 'sample_traffic.mp4'")
        print("   3. Run: python main.py --source sample_traffic.mp4")
        return
    
    # Initialize system
    detector = YOLOVehicleDetector(model_size='n')
    optimizer = TrafficSignalOptimizer()
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    print(f"📹 Processing video: {video_path}")
    
    while cap.isOpened() and frame_count < 10:  # Process first 10 frames
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Detect and optimize
        vehicle_count, annotated, detections = detector.detect_vehicles(frame)
        density_level, density_score = estimate_density(vehicle_count)
        timing = optimizer.calculate_optimal_timing(vehicle_count, density_score)
        
        print(f"Frame {frame_count}: {vehicle_count} vehicles → {timing.green_duration}s green")
    
    cap.release()
    print(f"✅ Processed {frame_count} frames")


def example_5_custom_parameters():
    """Example 5: Custom optimization parameters"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Optimization Parameters")
    print("="*60)
    
    # Create optimizer with custom parameters
    custom_optimizer = TrafficSignalOptimizer(
        min_green=15.0,   # Minimum 15 seconds
        max_green=120.0,  # Maximum 2 minutes
        base_green=45.0   # Base time 45 seconds
    )
    
    vehicle_count = 10
    density_level, density_score = estimate_density(vehicle_count)
    timing = custom_optimizer.calculate_optimal_timing(vehicle_count, density_score)
    
    print(f"\nCustom parameters:")
    print(f"  Min green: 15s, Max green: 120s, Base: 45s")
    print(f"\nFor {vehicle_count} vehicles:")
    print(f"  Calculated green time: {timing.green_duration}s")
    
    # Compare with default
    default_optimizer = TrafficSignalOptimizer()
    default_timing = default_optimizer.calculate_optimal_timing(vehicle_count, density_score)
    
    print(f"\nDefault parameters:")
    print(f"  Calculated green time: {default_timing.green_duration}s")
    print(f"\nDifference: {timing.green_duration - default_timing.green_duration}s")


def main():
    """Run all examples"""
    print("="*60)
    print("🚦 TRAFFIC OPTIMIZATION SYSTEM - USAGE EXAMPLES")
    print("="*60)
    
    try:
        example_1_basic_detection()
        example_2_signal_optimization()
        example_3_multi_lane()
        example_4_process_video()
        example_5_custom_parameters()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        print("\nTo run the full system:")
        print("  cd src")
        print("  python main.py --source webcam")
        print("\nFor more options, see SETUP.md")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you've installed all dependencies:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
