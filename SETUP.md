# 🚀 Setup Guide - Real AI Traffic Optimization System

## Prerequisites

- Python 3.8 or higher
- GPU (optional but recommended for better performance)
- Webcam or traffic video footage

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI-Smart-Traffic
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- YOLOv8 (ultralytics)
- PyTorch
- OpenCV
- NumPy, Pandas
- Matplotlib, Seaborn

### 4. Download YOLOv8 Model
The model will download automatically on first run. You can also pre-download:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Quick Start

### Option 1: Run with Webcam
```bash
cd src
python main.py --source webcam
```

### Option 2: Run with Video File
```bash
cd src
python main.py --source path/to/traffic_video.mp4
```

### Option 3: Save Output Video
```bash
cd src
python main.py --source input.mp4 --output output.mp4
```

## Advanced Usage

### Use Different Model Sizes
```bash
# Nano (fastest, less accurate)
python main.py --source webcam --model n

# Small (balanced)
python main.py --source webcam --model s

# Medium (more accurate, slower)
python main.py --source webcam --model m
```

### Adjust Detection Confidence
```bash
python main.py --source webcam --confidence 0.7
```

## Training Custom Model

If you have your own traffic dataset:

### 1. Prepare Dataset
Organize your data:
```
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
```

### 2. Train Model
```bash
cd src
python train_custom.py --data ../data --model n --epochs 100
```

### 3. Use Trained Model
```bash
python main.py --source webcam --model runs/detect/traffic_model/weights/best.pt
```

## Analytics

After running the system, generate analytics:

```bash
cd src
python analytics.py
```

This creates:
- Vehicle distribution charts
- Green time optimization graphs
- Time series analysis
- Density heatmaps
- Statistical report

## Troubleshooting

### CUDA/GPU Issues
If you have GPU but it's not detected:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### OpenCV Camera Issues
If webcam doesn't work, try different camera indices:
```python
# In main.py, change:
cap = cv2.VideoCapture(0)  # Try 1, 2, etc.
```

### Memory Issues
Use smaller model or reduce batch size:
```bash
python main.py --source video.mp4 --model n
```

## Sample Traffic Videos

Download free traffic videos for testing:
- [Pexels Traffic Videos](https://www.pexels.com/search/videos/traffic/)
- [Pixabay Traffic Videos](https://pixabay.com/videos/search/traffic/)

## Performance Tips

1. **Use GPU**: 10-20x faster than CPU
2. **Use smaller models**: YOLOv8n is 5x faster than YOLOv8x
3. **Lower resolution**: Resize videos to 640x480 for faster processing
4. **Adjust confidence**: Higher threshold = fewer false positives

## Next Steps

- Collect your own traffic dataset
- Train custom model for your specific use case
- Integrate with real traffic signal controllers
- Deploy on edge devices (Raspberry Pi, Jetson Nano)
- Add multi-intersection coordination
