"""
Custom Model Training Script
Train YOLOv8 on custom traffic dataset for improved accuracy
"""

from ultralytics import YOLO
import yaml
from pathlib import Path


def create_dataset_config(dataset_path: str = './data'):
    """
    Create dataset configuration file for training
    
    Expected structure:
    data/
      ├── train/
      │   ├── images/
      │   └── labels/
      ├── val/
      │   ├── images/
      │   └── labels/
      └── test/
          ├── images/
          └── labels/
    """
    config = {
        'path': dataset_path,
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'names': {
            0: 'car',
            1: 'motorcycle',
            2: 'bus',
            3: 'truck'
        }
    }
    
    config_path = Path(dataset_path) / 'dataset.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    
    print(f"✅ Dataset config created: {config_path}")
    return str(config_path)


def train_model(data_config: str, 
                model_size: str = 'n',
                epochs: int = 100,
                img_size: int = 640,
                batch_size: int = 16):
    """
    Train YOLOv8 model on custom dataset
    
    Args:
        data_config: Path to dataset.yaml
        model_size: Model size ('n', 's', 'm', 'l', 'x')
        epochs: Number of training epochs
        img_size: Input image size
        batch_size: Batch size for training
    """
    print(f"\n🚀 Starting YOLOv8{model_size} training...")
    print(f"Epochs: {epochs}, Image Size: {img_size}, Batch: {batch_size}")
    
    # Load pretrained model
    model = YOLO(f'yolov8{model_size}.pt')
    
    # Train
    results = model.train(
        data=data_config,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        name='traffic_model',
        patience=20,  # Early stopping
        save=True,
        plots=True,
        device='cpu',  # Use CPU (change to 'cuda:0' if GPU available)
        workers=4,
        optimizer='Adam',
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0
    )
    
    print("\n✅ Training completed!")
    print(f"Best model saved to: runs/detect/traffic_model/weights/best.pt")
    
    return results


def validate_model(model_path: str, data_config: str):
    """Validate trained model"""
    print(f"\n📊 Validating model: {model_path}")
    
    model = YOLO(model_path)
    results = model.val(data=data_config)
    
    print("\n📈 Validation Results:")
    print(f"mAP50: {results.box.map50:.3f}")
    print(f"mAP50-95: {results.box.map:.3f}")
    print(f"Precision: {results.box.mp:.3f}")
    print(f"Recall: {results.box.mr:.3f}")
    
    return results


def export_model(model_path: str, format: str = 'onnx'):
    """
    Export model to different formats for deployment
    
    Args:
        model_path: Path to trained model
        format: Export format ('onnx', 'torchscript', 'tflite', etc.)
    """
    print(f"\n📦 Exporting model to {format}...")
    
    model = YOLO(model_path)
    model.export(format=format)
    
    print(f"✅ Model exported successfully")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train custom traffic detection model')
    parser.add_argument('--data', type=str, default='./data',
                       help='Path to dataset directory')
    parser.add_argument('--model', type=str, default='n',
                       choices=['n', 's', 'm', 'l', 'x'],
                       help='Model size')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of epochs')
    parser.add_argument('--batch', type=int, default=16,
                       help='Batch size')
    parser.add_argument('--img-size', type=int, default=640,
                       help='Image size')
    parser.add_argument('--validate', action='store_true',
                       help='Validate model after training')
    parser.add_argument('--export', type=str, default=None,
                       help='Export format (onnx, torchscript, etc.)')
    
    args = parser.parse_args()
    
    # Create dataset config
    config_path = create_dataset_config(args.data)
    
    # Train model
    results = train_model(
        data_config=config_path,
        model_size=args.model,
        epochs=args.epochs,
        img_size=args.img_size,
        batch_size=args.batch
    )
    
    # Validate if requested
    if args.validate:
        best_model = 'runs/detect/traffic_model/weights/best.pt'
        validate_model(best_model, config_path)
    
    # Export if requested
    if args.export:
        best_model = 'runs/detect/traffic_model/weights/best.pt'
        export_model(best_model, args.export)
