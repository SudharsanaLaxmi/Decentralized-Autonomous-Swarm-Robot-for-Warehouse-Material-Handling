"""
Build and Run Commands

Quick reference for common development tasks.
"""

# Build Commands

## Firmware Build

### Development Build (with debug output)
```bash
cd firmware
platformio run -e esp32_dev
```

### Production Build (optimized)
```bash
platformio run -e esp32_prod
```

### Upload to Board
```bash
platformio run -t upload
```

### Monitor Serial Output
```bash
platformio device monitor --baud 115200
```

### Clean Build
```bash
platformio run -t clean
pio run  # Rebuild everything
```

---

## Python Testing

### Run All Tests
```bash
pytest testing/ -v
```

### Run Specific Test File
```bash
pytest testing/unit/test_vision.py -v
```

### Run Tests with Coverage
```bash
pytest testing/ --cov=vision --cov=communication --cov-report=html
```

### Watch Mode (auto-run on file change)
```bash
pytest-watch testing/ -n
```

---

## Code Quality

### Format Code (Black)
```bash
black vision/ firmware_python/
```

### Lint Code (Pylint)
```bash
pylint vision/**/*.py communication/**/*.py
```

### Type Check (Mypy)
```bash
mypy vision/ communication/ --ignore-missing-imports
```

### Sort Imports (isort)
```bash
isort vision/ communication/ tests/
```

### Run All Quality Checks
```bash
./scripts/check_quality.sh
```

---

## Docker Operations

### Build Docker Image
```bash
docker build -t swarm-robot:latest .
```

### Run Development Container
```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  swarm-robot:latest \
  bash
```

### Run Tests in Container
```bash
docker run --rm \
  -v $(pwd):/workspace \
  swarm-robot:latest \
  pytest testing/ -v
```

---

## Git Workflow

### Commit Format (Conventional Commits)
```bash
git commit -m "feat: add motor controller with PWM ramping"
git commit -m "fix: correct PID anti-windup logic"
git commit -m "docs: add PID tuning guide"
git commit -m "test: add integration tests for communication"
```

### Create Feature Branch
```bash
git checkout -b feat/add-slam-algorithm
```

### Push to Repository
```bash
git push origin feat/add-slam-algorithm
```

### Create Pull Request
```bash
# Via GitHub CLI
gh pr create --title "Add SLAM algorithm" --body "Implements visual SLAM..."
```

---

## Development Environment Setup

### First-Time Setup
```bash
# Clone and enter directory
git clone https://github.com/yourorg/swarm-robot.git
cd swarm-robot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install firmware tools
pio platform install espressif32

# Verify setup
python -m pytest testing/unit/test_vision.py::TestArucoDetector::test_detector_initialization
pio boards list | grep esp32
```

---

## Common Troubleshooting

### Serial Port Not Found
```bash
# List available ports
pio device list

# Or on Linux
ls /dev/tty*

# Edit platformio.ini with correct port
```

### Import Errors
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt

# Verify installation
python -c "import cv2, numpy, scipy; print('OK')"
```

### Test Failures
```bash
# Increase verbosity
pytest testing/ -vv --tb=long

# Run single test with debugging
pytest testing/unit/test_vision.py::TestArucoDetector -vv -s
```

### Memory Issues on ESP32
```bash
# Use release build for smaller binary
[env:esp32_release]
build_type = release
```

---

## Performance Profiling

### Profile Python Code
```bash
python -m cProfile -s cumtime examples/example_basic_control.py
```

### Memory Profiling (Python)
```bash
pip install memory-profiler
python -m memory_profiler examples/example_basic_control.py
```

### Firmware Memory Report
```bash
pio run --verbose | grep -i "text\|data\|bss"
```

---

## Documentation Building

### Generate HTML Docs (if using Sphinx)
```bash
cd docs
make html
open _build/html/index.html
```

### Generate API Docs
```bash
pip install pdoc
pdoc vision communication --html --output-dir docs/api
```

---

## CI/CD Pipeline

### Run Local CI Tests (simulate GitHub Actions)
```bash
# Requires act: https://github.com/nektos/act
act -j build
```

### Trigger Release Build
```bash
git tag v1.0.0
git push origin v1.0.0
# GitHub Actions automatically builds and releases
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Build firmware | `cd firmware && pio run` |
| Upload to board | `pio run -t upload` |
| Monitor serial | `pio device monitor` |
| Run tests | `pytest testing/ -v` |
| Check code quality | `black vision/ && pylint vision/` |
| Type check | `mypy vision/` |
| Format code | `black vision/ communication/` |
| Git commit | `git commit -m "feat: description"` |
| Create PR | `gh pr create --title "..." --body "..."` |

---

## Parallel Development

### Using Make (if Makefile exists)
```bash
# Build multiple targets
make build-firmware build-tests check-quality

# Run all checks
make all
```

### Using Scripts
```bash
# Run development workflow
./scripts/dev_workflow.sh

# Deploy to multiple boards
./scripts/deploy_all.sh
```
