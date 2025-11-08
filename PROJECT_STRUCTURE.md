# 📂 Project Structure

## Complete File Tree

```
AI-Smart-Traffic/
│
├── 📄 README.md                    # Main project overview
├── 📄 QUICK_START.md               # Fast setup guide (start here!)
├── 📄 SETUP.md                     # Detailed installation instructions
├── 📄 DOCUMENTATION.md             # Technical API documentation
├── 📄 PROJECT_SUMMARY.md           # Resume & portfolio summary
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 DEMO_GUIDE.md                # Original demo guide
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Git ignore rules
├── 📄 LICENSE                      # Project license
│
├── 🧪 test_system.py               # System verification script
├── 📝 example_usage.py             # Code examples and tutorials
│
├── 📁 src/                         # Source code directory
│   ├── 🚀 main.py                  # Main application (START HERE)
│   ├── 🤖 yolo_detector.py         # YOLOv8 vehicle detection
│   ├── ⚙️  optimize.py              # Signal optimization algorithm
│   ├── 📊 analytics.py             # Data analysis & visualization
│   ├── 🎓 train_custom.py          # Custom model training
│   ├── 🎬 demo.py                  # Simple OpenCV demo
│   └── 👁️  detect.py                # Basic detection (demo only)
│
├── 📁 data/                        # Dataset directory (create this)
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       ├── images/
│       └── labels/
│
├── 📁 results/                     # Generated analytics (auto-created)
│   ├── vehicle_distribution.png
│   ├── green_time_optimization.png
│   ├── time_series.png
│   ├── density_heatmap.png
│   └── report.txt
│
└── 📁 runs/                        # Training outputs (auto-created)
    └── detect/
        └── traffic_model/
            └── weights/
                ├── best.pt
                └── last.pt
```

## File Descriptions

### 📚 Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `README.md` | Project overview, features, tech stack | First time visitors |
| `QUICK_START.md` | Fast setup in 5 minutes | Want to run immediately |
| `SETUP.md` | Detailed installation guide | Having setup issues |
| `DOCUMENTATION.md` | API reference, algorithms | Development/integration |
| `PROJECT_SUMMARY.md` | Resume bullets, metrics | Adding to portfolio |
| `PROJECT_STRUCTURE.md` | This file - navigation | Understanding codebase |

### 🔧 Setup Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Files to exclude from git |
| `LICENSE` | Project license (MIT) |

### 🧪 Testing & Examples

| File | Purpose | Command |
|------|---------|---------|
| `test_system.py` | Verify installation | `python test_system.py` |
| `example_usage.py` | Code examples | `python example_usage.py` |

### 💻 Source Code (`src/`)

#### Core Modules

**`main.py`** - Main Application
- Entry point for the system
- Integrates all components
- Handles video/webcam input
- Real-time visualization
- Command-line interface

**`yolo_detector.py`** - Vehicle Detection
- YOLOv8 model loading
- Real-time object detection
- Vehicle classification (4 classes)
- Bounding box annotation
- Density estimation

**`optimize.py`** - Signal Optimization
- Traffic signal timing calculation
- Multi-lane coordination
- Fuel savings estimation
- CO₂ reduction calculation
- History logging

**`analytics.py`** - Data Analysis
- Statistical analysis
- Visualization generation
- Performance metrics
- Report generation

**`train_custom.py`** - Model Training
- Custom dataset training
- Hyperparameter configuration
- Model validation
- Export to ONNX

#### Demo Modules

**`demo.py`** - Simple Demo
- Basic OpenCV demo
- Background subtraction
- No deep learning required
- Good for quick testing

**`detect.py`** - Basic Detection
- Simple vehicle counting
- Background subtraction method
- Used by demo.py

## Module Dependencies

```
main.py
  ├── yolo_detector.py
  │     └── ultralytics (YOLOv8)
  │     └── torch (PyTorch)
  │     └── opencv (cv2)
  │
  └── optimize.py
        └── numpy
        └── pandas

analytics.py
  └── matplotlib
  └── seaborn
  └── pandas

train_custom.py
  └── ultralytics
  └── yaml
```

## Data Flow

```
1. Input Source (Video/Webcam)
   ↓
2. main.py (TrafficOptimizationSystem)
   ↓
3. yolo_detector.py (YOLOVehicleDetector)
   ├── Detect vehicles
   ├── Count & classify
   └── Estimate density
   ↓
4. optimize.py (TrafficSignalOptimizer)
   ├── Calculate optimal timing
   ├── Estimate savings
   └── Log decisions
   ↓
5. Output
   ├── Annotated video display
   ├── optimization_history.json
   └── Terminal statistics
   ↓
6. analytics.py (TrafficAnalytics)
   ├── Load history
   ├── Generate visualizations
   └── Create reports
```

## Quick Navigation Guide

### I want to...

**Run the system**
→ `cd src && python main.py --source webcam`

**Test if everything works**
→ `python test_system.py`

**See code examples**
→ `python example_usage.py`

**Understand the API**
→ Read `DOCUMENTATION.md`

**Add to my resume**
→ Read `PROJECT_SUMMARY.md`

**Train custom model**
→ `cd src && python train_custom.py --help`

**Generate analytics**
→ `cd src && python analytics.py`

**Troubleshoot issues**
→ Read `SETUP.md` troubleshooting section

## File Sizes (Approximate)

| Component | Size |
|-----------|------|
| Source code | ~30 KB |
| Documentation | ~50 KB |
| YOLOv8n model | 6 MB |
| YOLOv8s model | 22 MB |
| YOLOv8m model | 52 MB |
| Dependencies | ~2 GB |

## Generated Files

These files are created when you run the system:

```
optimization_history.json    # Created by main.py
results/                     # Created by analytics.py
  ├── *.png                  # Visualization charts
  └── report.txt             # Statistical report
runs/                        # Created by train_custom.py
  └── detect/
      └── traffic_model/
          └── weights/
              ├── best.pt    # Best model checkpoint
              └── last.pt    # Last model checkpoint
```

## Development Workflow

```
1. Setup
   └── pip install -r requirements.txt

2. Test
   └── python test_system.py

3. Develop
   ├── Edit src/*.py
   └── Test changes

4. Run
   └── python src/main.py

5. Analyze
   └── python src/analytics.py

6. Train (optional)
   └── python src/train_custom.py
```

## Code Statistics

```
Total Lines of Code:     ~1,500
Python Files:            10
Documentation Files:     7
Test Files:             2

Modules:
  - Detection:          ~150 lines
  - Optimization:       ~200 lines
  - Main System:        ~300 lines
  - Analytics:          ~250 lines
  - Training:           ~200 lines
  - Examples:           ~200 lines
  - Tests:              ~200 lines
```

## Architecture Layers

```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│  (Visualization, CLI, Display)      │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│     Application Layer               │
│  (main.py, analytics.py)            │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│     Business Logic Layer            │
│  (optimize.py, density estimation)  │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│     AI/ML Layer                     │
│  (yolo_detector.py, YOLOv8)         │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│     Data Layer                      │
│  (Video input, JSON logs)           │
└─────────────────────────────────────┘
```

## Next Steps

1. ✅ Read `QUICK_START.md` for fast setup
2. ✅ Run `python test_system.py` to verify
3. ✅ Try `python example_usage.py` for examples
4. ✅ Run `python src/main.py --source webcam`
5. ✅ Generate analytics with `python src/analytics.py`
6. ✅ Read `DOCUMENTATION.md` for deep dive

---

**Need help?** Check the troubleshooting section in `SETUP.md`
