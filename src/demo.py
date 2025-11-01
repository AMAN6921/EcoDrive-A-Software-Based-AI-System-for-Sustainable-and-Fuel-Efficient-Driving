"""
OpenCV Demo for Traffic Flow Optimization
Demonstrates vehicle detection and density estimation
"""

import cv2
import numpy as np
from detect import VehicleDetector, estimate_density


def run_demo_webcam():
    """Run demo using webcam feed"""
    print("🚦 Starting Traffic Detection Demo (Webcam)")
    print("Press 'q' to quit\n")
    
    cap = cv2.VideoCapture(0)
    detector = VehicleDetector(min_contour_area=800)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Detect vehicles
        vehicle_count, annotated_frame = detector.detect_vehicles(frame)
        
        # Estimate density
        frame_area = frame.shape[0] * frame.shape[1]
        density = estimate_density(vehicle_count, frame_area)
        
        # Add info overlay
        cv2.putText(
            annotated_frame, f"Vehicles: {vehicle_count}", 
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        cv2.putText(
            annotated_frame, f"Density: {density}", 
            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        
        # Display
        cv2.imshow("Traffic Detection Demo", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Demo completed")


def run_demo_video(video_path: str):
    """Run demo using video file"""
    print(f"🚦 Starting Traffic Detection Demo (Video: {video_path})")
    print("Press 'q' to quit\n")
    
    cap = cv2.VideoCapture(video_path)
    detector = VehicleDetector(min_contour_area=500)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open video file: {video_path}")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect vehicles
        vehicle_count, annotated_frame = detector.detect_vehicles(frame)
        
        # Estimate density
        frame_area = frame.shape[0] * frame.shape[1]
        density = estimate_density(vehicle_count, frame_area)
        
        # Add info overlay
        cv2.putText(
            annotated_frame, f"Vehicles: {vehicle_count}", 
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        cv2.putText(
            annotated_frame, f"Density: {density}", 
            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        
        # Display
        cv2.imshow("Traffic Detection Demo", annotated_frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Demo completed")


def create_synthetic_traffic():
    """Create a synthetic traffic scene for testing"""
    print("🚦 Starting Synthetic Traffic Demo")
    print("Press 'q' to quit\n")
    
    detector = VehicleDetector(min_contour_area=300)
    
    for i in range(200):
        # Create blank frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 50
        
        # Simulate moving vehicles
        num_vehicles = np.random.randint(1, 8)
        for j in range(num_vehicles):
            x = (i * 5 + j * 80) % 600
            y = 200 + j * 50
            cv2.rectangle(frame, (x, y), (x + 60, y + 40), (200, 200, 200), -1)
        
        # Detect vehicles
        vehicle_count, annotated_frame = detector.detect_vehicles(frame)
        
        # Estimate density
        frame_area = frame.shape[0] * frame.shape[1]
        density = estimate_density(vehicle_count, frame_area)
        
        # Add info overlay
        cv2.putText(
            annotated_frame, f"Vehicles: {vehicle_count}", 
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        cv2.putText(
            annotated_frame, f"Density: {density}", 
            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 255), 2
        )
        cv2.putText(
            annotated_frame, "Synthetic Traffic Scene", 
            (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, (255, 255, 255), 1
        )
        
        # Display
        cv2.imshow("Synthetic Traffic Demo", annotated_frame)
        
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    print("\n✅ Demo completed")


if __name__ == "__main__":
    print("=" * 50)
    print("🚦 AI-Powered Traffic Flow Optimization Demo")
    print("=" * 50)
    print("\nSelect demo mode:")
    print("1. Webcam (live)")
    print("2. Video file")
    print("3. Synthetic traffic (no camera needed)")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        run_demo_webcam()
    elif choice == "2":
        video_path = input("Enter video file path: ").strip()
        run_demo_video(video_path)
    elif choice == "3":
        create_synthetic_traffic()
    else:
        print("Invalid choice")
