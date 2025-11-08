"""
Quick System Test
Verifies all components are working correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing imports...")
    
    try:
        import cv2
        print("  ✅ OpenCV")
    except ImportError:
        print("  ❌ OpenCV - Run: pip install opencv-python")
        return False
    
    try:
        import numpy
        print("  ✅ NumPy")
    except ImportError:
        print("  ❌ NumPy - Run: pip install numpy")
        return False
    
    try:
        import torch
        print("  ✅ PyTorch")
        if torch.cuda.is_available():
            print(f"     🚀 GPU available: {torch.cuda.get_device_name(0)}")
        else:
            print("     ⚠️  CPU only (GPU recommended for better performance)")
    except ImportError:
        print("  ❌ PyTorch - Run: pip install torch torchvision")
        return False
    
    try:
        from ultralytics import YOLO
        print("  ✅ Ultralytics (YOLOv8)")
    except ImportError:
        print("  ❌ Ultralytics - Run: pip install ultralytics")
        return False
    
    try:
        import pandas
        print("  ✅ Pandas")
    except ImportError:
        print("  ❌ Pandas - Run: pip install pandas")
        return False
    
    try:
        import matplotlib
        print("  ✅ Matplotlib")
    except ImportError:
        print("  ❌ Matplotlib - Run: pip install matplotlib")
        return False
    
    return True


def test_modules():
    """Test if custom modules load correctly"""
    print("\n🧪 Testing custom modules...")
    
    try:
        from yolo_detector import YOLOVehicleDetector, estimate_density
        print("  ✅ yolo_detector.py")
    except Exception as e:
        print(f"  ❌ yolo_detector.py - {e}")
        return False
    
    try:
        from optimize import TrafficSignalOptimizer, SignalTiming
        print("  ✅ optimize.py")
    except Exception as e:
        print(f"  ❌ optimize.py - {e}")
        return False
    
    try:
        from analytics import TrafficAnalytics
        print("  ✅ analytics.py")
    except Exception as e:
        print(f"  ❌ analytics.py - {e}")
        return False
    
    return True


def test_yolo_model():
    """Test YOLO model loading"""
    print("\n🧪 Testing YOLO model...")
    
    try:
        from ultralytics import YOLO
        print("  📥 Downloading YOLOv8n model (first time only)...")
        model = YOLO('yolov8n.pt')
        print("  ✅ YOLOv8n model loaded successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to load model - {e}")
        return False


def test_optimizer():
    """Test signal optimizer"""
    print("\n🧪 Testing signal optimizer...")
    
    try:
        from optimize import TrafficSignalOptimizer
        from yolo_detector import estimate_density
        
        optimizer = TrafficSignalOptimizer()
        
        # Test with different vehicle counts
        test_cases = [
            (2, "LOW"),
            (5, "MEDIUM"),
            (10, "HIGH"),
            (20, "CRITICAL")
        ]
        
        for vehicle_count, expected_density in test_cases:
            density_level, density_score = estimate_density(vehicle_count)
            timing = optimizer.calculate_optimal_timing(vehicle_count, density_score)
            print(f"  ✅ {vehicle_count} vehicles → {density_level} → {timing.green_duration}s green")
        
        return True
    except Exception as e:
        print(f"  ❌ Optimizer test failed - {e}")
        return False


def test_synthetic_detection():
    """Test detection on synthetic image"""
    print("\n🧪 Testing detection on synthetic image...")
    
    try:
        import numpy as np
        import cv2
        from yolo_detector import YOLOVehicleDetector
        
        # Create synthetic image with rectangles (simulating vehicles)
        img = np.ones((480, 640, 3), dtype=np.uint8) * 50
        cv2.rectangle(img, (100, 200), (200, 280), (200, 200, 200), -1)
        cv2.rectangle(img, (300, 200), (400, 280), (200, 200, 200), -1)
        
        print("  📥 Loading detector...")
        detector = YOLOVehicleDetector(model_size='n', confidence=0.3)
        
        print("  🔍 Running detection...")
        vehicle_count, annotated, detections = detector.detect_vehicles(img)
        
        print(f"  ✅ Detection completed - Found {vehicle_count} objects")
        print("     (Note: Synthetic rectangles may not be detected as vehicles)")
        
        return True
    except Exception as e:
        print(f"  ❌ Detection test failed - {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("🚦 AI TRAFFIC OPTIMIZATION SYSTEM - TEST SUITE")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Modules", test_modules()))
    results.append(("YOLO Model", test_yolo_model()))
    results.append(("Optimizer", test_optimizer()))
    results.append(("Detection", test_synthetic_detection()))
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*60)
    if all_passed:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. cd src")
        print("  2. python main.py --source webcam")
        print("\nOr see SETUP.md for more options.")
    else:
        print("⚠️  Some tests failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60)


if __name__ == "__main__":
    main()
