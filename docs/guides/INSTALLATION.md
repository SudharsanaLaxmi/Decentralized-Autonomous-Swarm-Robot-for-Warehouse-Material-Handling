"""
Installation and setup guide

Detailed instructions for setting up the development environment
and building both firmware and software components.
"""

# Installation Guide

## System Requirements

### Hardware
- **Computer**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **ESP32 Board**: DevKit-C v4/v1/v2
- **USB Cable**: USB-C or Micro-USB (depending on board variant)
- **Robot Hardware**: Assembled per [hardware/README.md](../hardware/README.md)

### Software
- **Python**: 3.8 or newer
- **Git**: 2.25+
- **C++ Compiler**: GCC 9+ or Clang 10+

## Step 1: Clone Repository

```bash
git clone https://github.com/yourorg/swarm-warehouse-robot.git
cd swarm-warehouse-robot
```

## Step 2: Python Environment Setup

### Create Virtual Environment

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Firmware Tools

### Install PlatformIO

```bash
pip install platformio
```

### Verify Installation

```bash
pio --version
pio boards list | grep esp32
```

### Install ESP32 Board Package

```bash
pio platform install espressif32
pio boards list
```

## Step 4: Hardware Setup

### Assemble Robot

Follow [hardware assembly guide](../hardware/README.md):
1. Mount motors and wheels
2. Install sensor PCB
3. Connect battery and components
4. Verify all connections

### Connect to Computer

1. Plug ESP32 into USB port
2. Identify port:
   - **Linux**: `/dev/ttyUSB0` or `/dev/ttyACM0`
   - **macOS**: `/dev/tty.usbserial-*` or `/dev/tty.wchusbserial*`
   - **Windows**: `COM3` - `COM9`

3. Test connection:
   ```bash
   pio device list
   ```

## Step 5: Upload Firmware

### Configure platformio.ini

Edit `platformio.ini` for your board:
```ini
[env:esp32_dev]
upload_port = /dev/ttyUSB0   # Or COM4 on Windows
```

### Build Firmware

```bash
cd firmware
platformio run
```

### Upload to Board

```bash
platformio run -t upload
```

### Monitor Serial Output

```bash
platformio device monitor --baud 115200
```

## Step 6: Verify Python Installation

### Test Imports

```bash
python -c "import cv2; import numpy; import scipy; print('All imports OK')"
```

### Run Vision Tests

```bash
pytest vision/tests/ -v
```

## Step 7: Run Examples

### Basic Firmware Example

Robot will slowly move forward for 2 seconds:

```bash
cd firmware
platformio run -t upload
platformio device monitor
# Watch serial output
```

### Python Vision Example

```bash
python -c "
from vision.src.camera import Camera
from vision.src.aruco_detector import ArucoDetector

cam = Camera(0)
detector = ArucoDetector()
print('Vision hardware initialized')
"
```

## Troubleshooting

### USB Connection Issues

**Problem**: `pio device list` shows no devices

**Solution**:
1. Install USB drivers for your board:
   - CH340: https://sparks.gogo.co.nz/ch340.html
   - CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

2. Check permissions (Linux):
   ```bash
   sudo usermod -a -G dialout $USER
   # Log out and back in
   ```

### Python Module Errors

**Problem**: `ModuleNotFoundError` on import

**Solution**:
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Or install specific package
pip install opencv-python
```

### Firmware Upload Fails

**Problem**: Upload times out or fails

**Solution**:
1. Reset ESP32: Press reset button
2. Use different upload speed:
   ```ini
   upload_speed = 115200
   ```
3. Add delay before reset:
   ```bash
   pio run -t upload --verbose
   ```

### Low Memory on Board

**Problem**: Compilation fails with memory errors

**Solution**:
1. Use release build:
   ```ini
   [env:esp32_prod]
   build_type = release
   ```

2. Disable unnecessary features in config.h

## Development Workflow

### Code Changes Workflow

```bash
# 1. Make changes in your editor
# 2. Format code
black vision/*.py
clang-format -i firmware/src/*.cpp

# 3. Run tests
pytest testing/ -v

# 4. Commit and push
git add .
git commit -m "feat: description"
git push origin feature-branch
```

### Building for Different Boards

```bash
# Development board with debug output
pio run -e esp32_dev -t upload

# Production board (optimized)
pio run -e esp32_prod -t upload

# Testing board  
pio run -e esp32_testing -t upload
```

## Next Steps

- [Quick Start Guide](QUICKSTART.md) - Get your first example running
- [Hardware Assembly](../hardware/README.md) - Build the robot
- [Architecture Documentation](../docs/architecture/SystemArchitecture.md) - Understand system design
- [PID Tuning](CALIBRATION.md) - Optimize robot performance

## Getting Help

- **Documentation**: [docs/](../docs/)
- **Examples**: [examples/](../examples/)
- **Issues**: [GitHub Issues](https://github.com/yourorg/swarm-warehouse-robot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourorg/swarm-warehouse-robot/discussions)
