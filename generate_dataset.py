"""
Generate synthetic traffic dataset for training
Creates realistic traffic images with YOLO format annotations
"""

import cv2
import numpy as np
from pathlib import Path
import random
import json

# YOLO class IDs for vehicles
CLASSES = {
    'car': 0,
    'truck': 1,
    'bus': 2,
    'motorcycle': 3
}

def create_traffic_scene(width=1280, height=720, num_vehicles=None):
    """Generate a realistic traffic scene with vehicles"""
    # Create background
    img = np.ones((height, width, 3), dtype=np.uint8) * 60
    
    # Draw road
    road_y1, road_y2 = 150, 570
    cv2.rectangle(img, (0, road_y1), (width, road_y2), (80, 80, 80), -1)
    
    # Draw lane markings
    for i in range(0, width, 100):
        cv2.rectangle(img, (i, height//2 - 5), (i + 50, height//2 + 5), (255, 255, 255), -1)
    
    # Add road edges
    cv2.line(img, (0, road_y1), (width, road_y1), (255, 255, 255), 2)
    cv2.line(img, (0, road_y2), (width, road_y2), (255, 255, 255), 2)
    
    # Determine number of vehicles
    if num_vehicles is None:
        num_vehicles = random.randint(3, 20)
    
    annotations = []
    
    for i in range(num_vehicles):
        # Random vehicle type
        vehicle_type = random.choice(list(CLASSES.keys()))
        class_id = CLASSES[vehicle_type]
        
        # Vehicle dimensions based on type
        if vehicle_type == 'car':
            v_width = random.randint(70, 100)
            v_height = random.randint(45, 60)
            color = (random.randint(80, 220), random.randint(80, 220), random.randint(80, 220))
        elif vehicle_type == 'truck':
            v_width = random.randint(100, 140)
            v_height = random.randint(70, 90)
            color = (random.randint(60, 150), random.randint(60, 150), random.randint(60, 150))
        elif vehicle_type == 'bus':
            v_width = random.randint(120, 160)
            v_height = random.randint(80, 100)
            color = (random.randint(100, 200), random.randint(150, 220), random.randint(50, 100))
        else:  # motorcycle
            v_width = random.randint(40, 60)
            v_height = random.randint(35, 50)
            color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        
        # Random position (avoid overlap as much as possible)
        max_attempts = 10
        for attempt in range(max_attempts):
            x = random.randint(50, width - v_width - 50)
            y = random.randint(road_y1 + 20, road_y2 - v_height - 20)
            
            # Check for overlap with existing vehicles
            overlap = False
            for ann in annotations:
                if (abs(x - ann['x']) < (v_width + ann['width']) / 2 and
                    abs(y - ann['y']) < (v_height + ann['height']) / 2):
                    overlap = True
                    break
            
            if not overlap or attempt == max_attempts - 1:
                break
        
        # Draw vehicle body
        cv2.rectangle(img, (x, y), (x + v_width, y + v_height), color, -1)
        cv2.rectangle(img, (x, y), (x + v_width, y + v_height), (40, 40, 40), 2)
        
        # Draw windows
        window_color = (150, 200, 255)
        if vehicle_type in ['car', 'truck']:
            cv2.rectangle(img, (x + 10, y + 8), (x + 30, y + 25), window_color, -1)
            cv2.rectangle(img, (x + v_width - 30, y + 8), (x + v_width - 10, y + 25), window_color, -1)
        elif vehicle_type == 'bus':
            for wx in range(x + 15, x + v_width - 15, 25):
                cv2.rectangle(img, (wx, y + 10), (wx + 15, y + 30), window_color, -1)
        
        # Draw wheels
        wheel_color = (30, 30, 30)
        wheel_radius = 8 if vehicle_type != 'motorcycle' else 6
        cv2.circle(img, (x + 15, y + v_height - 5), wheel_radius, wheel_color, -1)
        cv2.circle(img, (x + v_width - 15, y + v_height - 5), wheel_radius, wheel_color, -1)
        
        # Add headlights for some realism
        if random.random() > 0.5:
            cv2.circle(img, (x + 10, y + v_height - 15), 4, (255, 255, 200), -1)
            cv2.circle(img, (x + v_width - 10, y + v_height - 15), 4, (255, 255, 200), -1)
        
        # Store annotation in YOLO format (normalized)
        x_center = (x + v_width / 2) / width
        y_center = (y + v_height / 2) / height
        norm_width = v_width / width
        norm_height = v_height / height
        
        annotations.append({
            'class_id': class_id,
            'x_center': x_center,
            'y_center': y_center,
            'width': norm_width,
            'height': norm_height,
            'x': x,
            'y': y,
            'width_px': v_width,
            'height_px': v_height
        })
    
    # Add some noise/texture for realism
    noise = np.random.randint(-10, 10, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img, annotations


def save_yolo_annotation(annotations, filepath):
    """Save annotations in YOLO format"""
    with open(filepath, 'w') as f:
        for ann in annotations:
            f.write(f"{ann['class_id']} {ann['x_center']:.6f} {ann['y_center']:.6f} "
                   f"{ann['width']:.6f} {ann['height']:.6f}\n")


def generate_dataset(num_train=500, num_val=100):
    """Generate complete dataset"""
    print("="*70)
    print("🎨 SYNTHETIC TRAFFIC DATASET GENERATOR")
    print("="*70)
    
    # Create directory structure
    base_dir = Path('data')
    dirs = [
        base_dir / 'train' / 'images',
        base_dir / 'train' / 'labels',
        base_dir / 'val' / 'images',
        base_dir / 'val' / 'labels'
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Created directory structure in '{base_dir}/'")
    
    # Generate training set
    print(f"\n🚗 Generating {num_train} training images...")
    stats = {'train': {'total_vehicles': 0, 'images': num_train}}
    
    for i in range(num_train):
        img, annotations = create_traffic_scene()
        
        # Save image
        img_path = base_dir / 'train' / 'images' / f'traffic_{i:04d}.jpg'
        cv2.imwrite(str(img_path), img)
        
        # Save annotation
        label_path = base_dir / 'train' / 'labels' / f'traffic_{i:04d}.txt'
        save_yolo_annotation(annotations, label_path)
        
        stats['train']['total_vehicles'] += len(annotations)
        
        if (i + 1) % 100 == 0:
            print(f"  ✓ Generated {i + 1}/{num_train} images")
    
    print(f"  ✅ Training set complete: {num_train} images")
    
    # Generate validation set
    print(f"\n🚗 Generating {num_val} validation images...")
    stats['val'] = {'total_vehicles': 0, 'images': num_val}
    
    for i in range(num_val):
        img, annotations = create_traffic_scene()
        
        # Save image
        img_path = base_dir / 'val' / 'images' / f'traffic_{i:04d}.jpg'
        cv2.imwrite(str(img_path), img)
        
        # Save annotation
        label_path = base_dir / 'val' / 'labels' / f'traffic_{i:04d}.txt'
        save_yolo_annotation(annotations, label_path)
        
        stats['val']['total_vehicles'] += len(annotations)
        
        if (i + 1) % 50 == 0:
            print(f"  ✓ Generated {i + 1}/{num_val} images")
    
    print(f"  ✅ Validation set complete: {num_val} images")
    
    # Create dataset.yaml for YOLO training
    yaml_content = f"""# Traffic Dataset Configuration
path: ../data  # dataset root dir
train: train/images  # train images (relative to 'path')
val: val/images  # val images (relative to 'path')

# Classes
names:
  0: car
  1: truck
  2: bus
  3: motorcycle

# Number of classes
nc: 4
"""
    
    yaml_path = base_dir / 'dataset.yaml'
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"\n📝 Created dataset.yaml configuration")
    
    # Save dataset statistics
    stats_path = base_dir / 'dataset_stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 DATASET SUMMARY")
    print("="*70)
    print(f"Training Images: {stats['train']['images']}")
    print(f"Training Vehicles: {stats['train']['total_vehicles']}")
    print(f"Avg Vehicles/Image: {stats['train']['total_vehicles']/stats['train']['images']:.1f}")
    print(f"\nValidation Images: {stats['val']['images']}")
    print(f"Validation Vehicles: {stats['val']['total_vehicles']}")
    print(f"Avg Vehicles/Image: {stats['val']['total_vehicles']/stats['val']['images']:.1f}")
    print(f"\nTotal Images: {stats['train']['images'] + stats['val']['images']}")
    print(f"Total Vehicles: {stats['train']['total_vehicles'] + stats['val']['total_vehicles']}")
    print("\n📁 Dataset Location: ./data/")
    print("📝 Config File: ./data/dataset.yaml")
    print("="*70)
    print("\n✅ Dataset generation complete!")
    print("\nNext steps:")
    print("  • Train custom model: python src/train_custom.py")
    print("  • View sample images in data/train/images/")
    print("  • Check annotations in data/train/labels/")


if __name__ == "__main__":
    try:
        generate_dataset(num_train=500, num_val=100)
    except KeyboardInterrupt:
        print("\n\n⏸️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
