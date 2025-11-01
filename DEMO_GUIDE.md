# 🚦 OpenCV Demo Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
cd src
python demo.py
```

## Demo Modes

### Option 1: Webcam Demo
- Uses your computer's webcam as a live traffic feed
- Best for testing with toy cars or simulated traffic
- Press 'q' to quit

### Option 2: Video File Demo
- Processes a pre-recorded traffic video
- You'll need to provide a video file path
- Great for testing with real traffic footage

### Option 3: Synthetic Traffic Demo
- **No camera needed!**
- Generates simulated moving vehicles
- Perfect for quick testing and demonstration

## How It Works

The demo uses **background subtraction** to detect moving objects:

1. **Background Modeling**: Learns what the "static" background looks like
2. **Foreground Detection**: Identifies moving objects (vehicles)
3. **Noise Filtering**: Removes small artifacts using morphological operations
4. **Vehicle Counting**: Counts detected objects above a size threshold
5. **Density Estimation**: Classifies traffic as LOW, MEDIUM, or HIGH

## Expected Output

You'll see:
- Green bounding boxes around detected vehicles
- Vehicle count in the top-left corner
- Traffic density level (LOW/MEDIUM/HIGH)

## Tips for Best Results

- **Webcam**: Position camera to capture a road-like view with moving objects
- **Video**: Use traffic footage with a relatively static camera angle
- **Synthetic**: Just run it - works out of the box!

## Next Steps

This basic demo can be enhanced with:
- YOLO or other deep learning models for better accuracy
- Lane-specific vehicle counting
- Speed estimation
- Signal timing optimization logic
