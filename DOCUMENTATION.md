# 📚 Technical Documentation

## System Architecture

### Overview
The AI Traffic Optimization System consists of three main components:

1. **Detection Module** (`yolo_detector.py`)
   - Real-time vehicle detection using YOLOv8
   - Supports 4 vehicle classes: car, motorcycle, bus, truck
   - Configurable confidence thresholds
   - GPU acceleration support

2. **Optimization Module** (`optimize.py`)
   - ML-based signal timing calculation
   - Dynamic green light duration adjustment
   - Multi-lane intersection support
   - Fuel and CO2 savings estimation

3. **Analytics Module** (`analytics.py`)
   - Data visualization and reporting
   - Statistical analysis
   - Performance metrics tracking

### Data Flow

```
Video/Camera Feed
    ↓
YOLOv8 Detection
    ↓
Vehicle Count & Classification
    ↓
Density Estimation
    ↓
Signal Optimization Algorithm
    ↓
Optimal Timing Calculation
    ↓
Savings Estimation
    ↓
Visualization & Logging
```

## API Reference

### YOLOVehicleDetector

```python
from yolo_detector import YOLOVehicleDetector

detector = YOLOVehicleDetector(
    model_size='n',      # 'n', 's', 'm', 'l', 'x'
    confidence=0.5       # 0.0 to 1.0
)

vehicle_count, annotated_frame, detections = detector.detect_vehicles(frame)
```

**Parameters:**
- `model_size`: YOLOv8 model variant
  - 'n' (nano): Fastest, ~6ms inference
  - 's' (small): Balanced, ~10ms inference
  - 'm' (medium): More accurate, ~20ms inference
  - 'l' (large): High accuracy, ~30ms inference
  - 'x' (xlarge): Best accuracy, ~50ms inference
- `confidence`: Detection confidence threshold (0-1)

**Returns:**
- `vehicle_count`: Integer count of detected vehicles
- `annotated_frame`: Frame with bounding boxes drawn
- `detections`: List of detection dictionaries containing:
  - `type`: Vehicle type (car, motorcycle, bus, truck)
  - `confidence`: Detection confidence score
  - `bbox`: Bounding box coordinates (x1, y1, x2, y2)
  - `center`: Center point of detection

### TrafficSignalOptimizer

```python
from optimize import TrafficSignalOptimizer

optimizer = TrafficSignalOptimizer(
    min_green=10.0,      # Minimum green duration (seconds)
    max_green=90.0,      # Maximum green duration (seconds)
    base_green=30.0      # Base green duration (seconds)
)

timing = optimizer.calculate_optimal_timing(
    vehicle_count=10,
    density_score=0.5,
    lane_id="main"
)
```

**Parameters:**
- `min_green`: Minimum allowed green light duration
- `max_green`: Maximum allowed green light duration
- `base_green`: Base duration for medium traffic

**Returns:**
- `SignalTiming` object with:
  - `green_duration`: Optimized green light time (seconds)
  - `yellow_duration`: Yellow light time (seconds, default 3s)
  - `red_duration`: Red light time (seconds, calculated)

### Density Estimation

```python
from yolo_detector import estimate_density

density_level, density_score = estimate_density(vehicle_count)
```

**Returns:**
- `density_level`: String classification
  - "LOW": 0-3 vehicles
  - "MEDIUM": 4-8 vehicles
  - "HIGH": 9-15 vehicles
  - "CRITICAL": 16+ vehicles
- `density_score`: Normalized score (0-1)

### Multi-Lane Optimization

```python
lane_densities = {
    'North': (vehicle_count, density_score),
    'South': (vehicle_count, density_score),
    'East': (vehicle_count, density_score),
    'West': (vehicle_count, density_score)
}

timings = optimizer.calculate_multi_lane_timing(lane_densities)
```

**Returns:**
- Dictionary mapping lane IDs to `SignalTiming` objects
- Red durations automatically calculated based on other lanes

## Optimization Algorithm

### Green Light Duration Formula

```
green_duration = base_green + (density_score × adjustment_range)

where:
  adjustment_range = max_green - base_green
  density_score = min(vehicle_count / 20.0, 1.0)
```

### Fuel Savings Calculation

```
idle_fuel_rate = 0.0001667 L/second per vehicle
wait_time_reduction = fixed_wait - optimized_wait
fuel_saved = vehicle_count × wait_time_reduction × idle_fuel_rate
```

### CO2 Emissions Calculation

```
co2_per_liter = 2.3 kg
co2_saved = fuel_saved × co2_per_liter
```

## Performance Benchmarks

### Detection Speed (YOLOv8n on different hardware)

| Hardware | FPS | Latency |
|----------|-----|---------|
| CPU (Intel i7) | 15-20 | 50-65ms |
| GPU (RTX 3060) | 80-100 | 10-12ms |
| GPU (RTX 4090) | 150-200 | 5-7ms |
| Jetson Nano | 8-12 | 80-120ms |

### Model Comparison

| Model | Size | Speed | mAP50 | Use Case |
|-------|------|-------|-------|----------|
| YOLOv8n | 6MB | Fastest | 37.3 | Real-time, edge devices |
| YOLOv8s | 22MB | Fast | 44.9 | Balanced performance |
| YOLOv8m | 52MB | Medium | 50.2 | High accuracy needed |
| YOLOv8l | 87MB | Slow | 52.9 | Offline processing |
| YOLOv8x | 136MB | Slowest | 53.9 | Maximum accuracy |

## Configuration

### Environment Variables

```bash
# Force CPU usage
export CUDA_VISIBLE_DEVICES=-1

# Set specific GPU
export CUDA_VISIBLE_DEVICES=0

# Adjust number of workers
export OMP_NUM_THREADS=4
```

### Command Line Arguments

```bash
python main.py \
  --source webcam \           # or video file path
  --output result.mp4 \       # optional output path
  --model n \                 # model size
  --confidence 0.5            # detection threshold
```

## Training Custom Models

### Dataset Preparation

1. **Collect Images**: Gather traffic footage from your target environment
2. **Annotate**: Use tools like LabelImg, CVAT, or Roboflow
3. **Format**: YOLO format (one .txt file per image)

```
# Example annotation format (normalized coordinates)
class_id x_center y_center width height
0 0.5 0.5 0.3 0.2
```

4. **Split**: 70% train, 20% validation, 10% test

### Training Command

```bash
python train_custom.py \
  --data ./data \
  --model n \
  --epochs 100 \
  --batch 16 \
  --img-size 640
```

### Hyperparameter Tuning

Key parameters to adjust:
- `lr0`: Initial learning rate (default: 0.01)
- `momentum`: SGD momentum (default: 0.937)
- `weight_decay`: L2 regularization (default: 0.0005)
- `warmup_epochs`: Warmup period (default: 3)
- `box`: Box loss weight (default: 7.5)
- `cls`: Classification loss weight (default: 0.5)

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
CMD ["python", "src/main.py", "--source", "webcam"]
```

### Edge Device Deployment

For Raspberry Pi or Jetson Nano:

```bash
# Use smaller model
python main.py --source webcam --model n

# Reduce resolution
python main.py --source webcam --model n --img-size 416
```

### ONNX Export

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.export(format='onnx')
```

## Troubleshooting

### Common Issues

**1. Low FPS**
- Use smaller model (n instead of m/l/x)
- Enable GPU acceleration
- Reduce input resolution
- Close other applications

**2. Poor Detection Accuracy**
- Increase confidence threshold
- Use larger model
- Train custom model on your data
- Ensure good lighting conditions

**3. Memory Errors**
- Reduce batch size
- Use smaller model
- Process lower resolution video
- Close other applications

**4. GPU Not Detected**
```bash
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Research Applications

### Metrics for Research Papers

1. **Detection Accuracy**
   - Precision, Recall, F1-Score
   - mAP (mean Average Precision)
   - Confusion matrix

2. **Optimization Performance**
   - Average wait time reduction
   - Fuel consumption savings
   - CO2 emission reduction
   - Throughput improvement

3. **System Performance**
   - Processing speed (FPS)
   - Latency
   - Resource utilization

### Citation

If you use this project in your research, please cite:

```bibtex
@software{ai_traffic_optimization,
  title={AI-Powered Smart Traffic Flow Optimization System},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/AI-Smart-Traffic}
}
```

## Contributing

Contributions are welcome! Areas for improvement:
- Additional vehicle types
- Weather condition handling
- Pedestrian detection
- Emergency vehicle priority
- Multi-camera coordination
- Real-time dashboard

## License

See LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [your-repo-url]/issues
- Documentation: See README.md and SETUP.md
- Examples: See example_usage.py
