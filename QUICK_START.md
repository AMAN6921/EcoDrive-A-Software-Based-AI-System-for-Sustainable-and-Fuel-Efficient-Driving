# ⚡ Quick Start Guide

## 1. Install (2 minutes)

```bash
# Clone repository
git clone <your-repo-url>
cd AI-Smart-Traffic

# Install dependencies
pip install -r requirements.txt
```

## 2. Test Installation (1 minute)

```bash
python test_system.py
```

This will verify all components are working.

## 3. Run System (30 seconds)

### Option A: Webcam (Live Demo)
```bash
cd src
python main.py --source webcam
```

### Option B: Video File
```bash
cd src
python main.py --source path/to/video.mp4
```

### Option C: Save Output
```bash
cd src
python main.py --source input.mp4 --output result.mp4
```

## 4. View Results

After running, you'll see:
- ✅ Real-time vehicle detection with bounding boxes
- ✅ Traffic density classification (LOW/MEDIUM/HIGH/CRITICAL)
- ✅ Optimized signal timings
- ✅ Fuel and CO2 savings estimates

Press 'q' to quit.

## 5. Generate Analytics

```bash
cd src
python analytics.py
```

This creates charts and reports in the `results/` folder.

## Common Commands

```bash
# Use different model sizes
python main.py --source webcam --model n  # Fastest
python main.py --source webcam --model s  # Balanced
python main.py --source webcam --model m  # More accurate

# Adjust detection sensitivity
python main.py --source webcam --confidence 0.7  # More strict
python main.py --source webcam --confidence 0.3  # More lenient

# See all options
python main.py --help
```

## What You Get

### Real-Time Display Shows:
- Vehicle count
- Traffic density level and score
- Optimized green/yellow light durations
- Estimated fuel savings per cycle
- Estimated CO2 reduction per cycle
- Frame counter

### After Processing:
- `optimization_history.json` - All decisions logged
- Statistics summary in terminal
- Ready for analytics visualization

## Next Steps

1. **Try with real traffic video** - Download from Pexels or Pixabay
2. **Experiment with parameters** - Adjust confidence, model size
3. **Generate analytics** - Run `python analytics.py`
4. **Read full docs** - See DOCUMENTATION.md for API details

## Troubleshooting

**"No module named 'ultralytics'"**
```bash
pip install ultralytics
```

**"CUDA not available"**
- System will use CPU (slower but works)
- For GPU: Install CUDA-enabled PyTorch

**Webcam not working**
- Try different camera index: Change `VideoCapture(0)` to `VideoCapture(1)`
- Or use video file instead

**Low FPS**
- Use smaller model: `--model n`
- Close other applications
- Use GPU if available

## Performance Tips

| Scenario | Recommended Settings |
|----------|---------------------|
| Real-time demo | `--model n` |
| High accuracy | `--model m` or `--model l` |
| Edge device | `--model n --confidence 0.6` |
| Video processing | `--model s` with output file |

## Example Workflow

```bash
# 1. Test system
python test_system.py

# 2. Run on webcam
cd src
python main.py --source webcam --model n

# 3. Process video
python main.py --source traffic.mp4 --output result.mp4

# 4. Generate analytics
python analytics.py

# 5. View results
open results/
```

## Getting Help

- **Setup issues**: See SETUP.md
- **API usage**: See DOCUMENTATION.md
- **Code examples**: Run `python example_usage.py`
- **Test system**: Run `python test_system.py`

---

**Ready to optimize traffic? Run `python test_system.py` to begin!** 🚦
