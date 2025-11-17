"""
Synthetic Traffic Demo - No camera needed!
Generates realistic traffic scenarios and processes them
"""

import sys
from pathlib import Path
import cv2
import numpy as np
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from yolo_detector import YOLOVehicleDetector, estimate_density
from optimize import TrafficSignalOptimizer


def create_traffic_frame(frame_num, scenario='medium'):
    """Create synthetic traffic scene"""
    # Create road background
    frame = np.ones((720, 1280, 3), dtype=np.uint8) * 60
    
    # Draw road
    cv2.rectangle(frame, (0, 200), (1280, 520), (80, 80, 80), -1)
    
    # Draw lane markings
    for i in range(0, 1280, 100):
        cv2.rectangle(frame, (i, 355), (i + 50, 365), (255, 255, 255), -1)
    
    # Add vehicles based on scenario
    if scenario == 'light':
        num_vehicles = np.random.randint(1, 4)
    elif scenario == 'medium':
        num_vehicles = np.random.randint(4, 9)
    elif scenario == 'heavy':
        num_vehicles = np.random.randint(9, 16)
    else:  # critical
        num_vehicles = np.random.randint(16, 25)
    
    # Draw vehicles (rectangles that look like cars)
    for i in range(num_vehicles):
        # Random position with some movement
        x = (frame_num * 3 + i * 120) % 1200
        y = 250 + (i % 3) * 80
        
        # Vehicle dimensions
        width = 80 + np.random.randint(-10, 10)
        height = 50 + np.random.randint(-5, 5)
        
        # Vehicle color (various shades)
        color = (
            np.random.randint(100, 200),
            np.random.randint(100, 200),
            np.random.randint(100, 200)
        )
        
        # Draw vehicle body
        cv2.rectangle(frame, (x, y), (x + width, y + height), color, -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (50, 50, 50), 2)
        
        # Draw windows
        cv2.rectangle(frame, (x + 10, y + 10), (x + 30, y + 25), (150, 200, 255), -1)
        cv2.rectangle(frame, (x + width - 30, y + 10), (x + width - 10, y + 25), (150, 200, 255), -1)
        
        # Draw wheels
        cv2.circle(frame, (x + 15, y + height), 8, (30, 30, 30), -1)
        cv2.circle(frame, (x + width - 15, y + height), 8, (30, 30, 30), -1)
    
    return frame, num_vehicles


def run_synthetic_demo():
    """Run demo with synthetic traffic"""
    print("="*70)
    print("🚦 AI TRAFFIC OPTIMIZATION SYSTEM - SYNTHETIC DEMO")
    print("="*70)
    print("\nGenerating synthetic traffic scenarios...")
    print("This demo doesn't require a camera or video file!\n")
    
    # Initialize system with custom trained model
    print("📥 Loading custom trained AI model...")
    custom_model_path = 'runs/detect/traffic_model/weights/best.pt'
    if Path(custom_model_path).exists():
        print(f"✨ Using custom trained model: {custom_model_path}")
        detector = YOLOVehicleDetector(model_path=custom_model_path, confidence=0.3)
    else:
        print("⚠️  Custom model not found, using default YOLOv8n")
        detector = YOLOVehicleDetector(model_size='n', confidence=0.3)
    optimizer = TrafficSignalOptimizer()
    
    # Traffic scenarios
    scenarios = [
        ('light', 30, "Light Traffic (Morning)"),
        ('medium', 40, "Medium Traffic (Midday)"),
        ('heavy', 40, "Heavy Traffic (Rush Hour)"),
        ('critical', 30, "Critical Traffic (Peak)"),
        ('medium', 30, "Medium Traffic (Evening)")
    ]
    
    print("\n▶️  Processing traffic scenarios...")
    print("Press 'q' to quit, 's' to skip to next scenario\n")
    
    frame_count = 0
    total_vehicles = 0
    total_fuel_saved = 0.0
    total_co2_saved = 0.0
    
    for scenario_type, duration, description in scenarios:
        print(f"\n📊 Scenario: {description}")
        
        for i in range(duration):
            frame_count += 1
            
            # Create synthetic frame
            frame, actual_vehicles = create_traffic_frame(i, scenario_type)
            
            # Add scenario label
            cv2.putText(frame, description, (20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            
            # Simulate detection (use actual count for demo)
            density_level, density_score = estimate_density(actual_vehicles)
            total_vehicles += actual_vehicles
            
            # Calculate optimal timing
            timing = optimizer.calculate_optimal_timing(actual_vehicles, density_score)
            
            # Estimate savings
            savings = optimizer.estimate_fuel_savings(actual_vehicles, timing.green_duration)
            total_fuel_saved += savings['fuel_saved_liters']
            total_co2_saved += savings['co2_saved_kg']
            
            # Add comprehensive overlay
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 80), (500, 400), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Info display
            y_pos = 120
            cv2.putText(frame, "AI Traffic Optimization", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            y_pos += 40
            cv2.putText(frame, f"Vehicles: {actual_vehicles}", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            y_pos += 35
            density_color = {
                'LOW': (0, 255, 0),
                'MEDIUM': (0, 255, 255),
                'HIGH': (0, 165, 255),
                'CRITICAL': (0, 0, 255)
            }.get(density_level, (255, 255, 255))
            cv2.putText(frame, f"Density: {density_level}", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, density_color, 2)
            
            y_pos += 45
            cv2.putText(frame, "Optimized Timing:", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            y_pos += 30
            cv2.putText(frame, f"  Green: {timing.green_duration:.0f}s", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            y_pos += 30
            cv2.putText(frame, f"  Yellow: {timing.yellow_duration:.0f}s", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            y_pos += 40
            cv2.putText(frame, "Savings (per cycle):", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            y_pos += 30
            cv2.putText(frame, f"  Fuel: {savings['fuel_saved_liters']:.3f} L", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            y_pos += 30
            cv2.putText(frame, f"  CO2: {savings['co2_saved_kg']:.3f} kg", 
                       (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Frame counter
            cv2.putText(frame, f"Frame: {frame_count}", 
                       (1100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
            
            # Display
            cv2.imshow("AI Traffic Optimization - Synthetic Demo", frame)
            
            key = cv2.waitKey(50) & 0xFF
            if key == ord('q'):
                print("\n⏸️  Demo stopped by user")
                cv2.destroyAllWindows()
                print_summary(frame_count, total_vehicles, total_fuel_saved, total_co2_saved, optimizer)
                return
            elif key == ord('s'):
                print(f"  ⏭️  Skipping to next scenario...")
                break
        
        print(f"  ✅ Completed {i+1} frames")
    
    cv2.destroyAllWindows()
    print_summary(frame_count, total_vehicles, total_fuel_saved, total_co2_saved, optimizer)


def print_summary(frames, vehicles, fuel, co2, optimizer):
    """Print final summary"""
    print("\n" + "="*70)
    print("📊 DEMO SUMMARY")
    print("="*70)
    print(f"Total Frames Processed: {frames}")
    print(f"Total Vehicles Detected: {vehicles}")
    print(f"Average Vehicles/Frame: {vehicles/frames:.1f}")
    print(f"\n💰 Estimated Total Savings:")
    print(f"  Fuel: {fuel:.2f} liters")
    print(f"  CO2: {co2:.2f} kg")
    print(f"  Cost Savings: ${fuel * 1.5:.2f} (assuming $1.50/liter)")
    print("\n📈 Optimization Statistics:")
    stats = optimizer.get_statistics()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print("="*70)
    print("\n✅ Demo completed successfully!")
    print("\nNext steps:")
    print("  • Run with real video: python src/main.py --source video.mp4")
    print("  • Run with webcam: python src/main.py --source webcam")
    print("  • Generate analytics: python src/analytics.py")
    print("  • See examples: python example_usage.py")
    
    # Save history
    optimizer.save_history('demo_optimization_history.json')


if __name__ == "__main__":
    try:
        run_synthetic_demo()
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo interrupted by user")
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've installed all dependencies:")
        print("  pip install -r requirements.txt")
