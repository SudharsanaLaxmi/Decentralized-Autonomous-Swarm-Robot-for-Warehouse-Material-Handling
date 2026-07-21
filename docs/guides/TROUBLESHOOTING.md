"""
Development Troubleshooting Guide

Common issues and solutions during development.
"""

# Development Troubleshooting

## Firmware Development Issues

### Issue: Upload Timeout

**Problem**: Upload stalls at "Leaving..." or "Uploading..."

**Symptoms**:
```
esptool.py v3.3.2
Serial port /dev/ttyUSB0
Connecting.......
(hangs here)
```

**Solutions** (try in order):

1. **Reset the board manually**
   - Press ESP32 Reset button
   - Then immediately press Boot button
   - Hold Boot for 1 second

2. **Check USB cable quality**
   - Use different cable
   - Verify it's not a charge-only cable

3. **Change upload speed**
   ```ini
   [env:esp32_dev]
   upload_speed = 115200  # Try lower speeds
   ```

4. **Update esptool**
   ```bash
   pip install --upgrade esptool platformio
   ```

5. **Full reset sequence**
   ```bash
   pio device list              # Verify port
   pio platform install espressif32 --force  # Reinstall
   cd firmware && pio run -t erase  # Erase chip
   pio run -t upload            # Then upload
   ```

---

### Issue: Firmware Won't Boot

**Problem**: Device doesn't respond after upload

**Symptoms**:
- No serial output
- LED doesn't blink
- Device not detected

**Solutions**:

1. **Verify boot mode**
   ```
   Power cycle: Disconnect USB, reconnect
   Device should show up in: pio device list
   ```

2. **Check power supply**
   - Verify 5V USB power (use multimeter)
   - Try different USB port
   - Check micro-USB connector for damage

3. **Reflash bootloader**
   ```bash
   pio platform install espressif32 --force
   esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
   $ pio run -t upload
   ```

4. **Test with minimal sketch**
   ```cpp
   void setup() {
     Serial.begin(115200);
     Serial.println("Hello");
   }
   void loop() { delay(1000); }
   ```

---

### Issue: Memory Overflow

**Problem**: "Sketch is more than X% of allocated space"

**Solutions**:

1. **Use release build**
   ```ini
   [env:esp32_prod]
   build_type = release
   ```

2. **Disable debug output**
   ```cpp
   // In config.h
   #define DEBUG_LEVEL 0  // Disable
   ```

3. **Check IRAM usage**
   - Mark frequently-called functions with `IRAM_ATTR`
   - Move large arrays to PSRAM

---

## Python Development Issues

### Issue: ImportError on Import

**Problem**: "ModuleNotFoundError: No module named 'vision'"

**Symptoms**:
```python
from vision.src.camera import Camera
# ModuleNotFoundError ...
```

**Solutions**:

1. **Verify file exists**
   ```bash
   ls vision/src/camera.py
   ```

2. **Reinstall package in development mode**
   ```bash
   pip install -e .
   ```

3. **Check Python path**
   ```python
   import sys
   print(sys.path)
   # Should include .../swarm-robot
   ```

4. **Clear Python cache**
   ```bash
   find . -type d -name __pycache__ -exec rm -r {} +
   find . -type f -name "*.pyc" -delete
   ```

---

### Issue: Tests Fail with "Port Already in Use"

**Problem**: Gateway binding fails on port 8888

**Error**:
```python
OSError: [Errno 98] Address already in use
```

**Solutions**:

1. **Kill existing process**
   ```bash
   # Linux/macOS
   lsof -i :8888
   kill -9 <PID>
   
   # Windows
   netstat -ano | findstr :8888
   taskkill /PID <PID> /F
   ```

2. **Use different port in test**
   ```python
   gateway = GatewayServer(port=19999)  # Use unique port
   ```

3. **Add delay between tests**
   ```python
   @pytest.fixture
   def gateway():
       server = GatewayServer()
       server.start()
       time.sleep(0.5)  # Allow socket to release
       yield server
       server.stop()
   ```

---

### Issue: Type Checking Errors

**Problem**: mypy reports false positives

**Error**:
```
error: Incompatible types in assignment
(expression has type "int", variable has type "float")
```

**Solutions**:

1. **Suppress known false positives**
   ```python
   value = int(result)  # type: ignore  # False positive
   ```

2. **Add type stubs for external libraries**
   ```bash
   pip install types-opencv-python
   pip install types-pyyaml
   ```

3. **Adjust mypy settings** (`setup.cfg`)
   ```ini
   [mypy]
   ignore_missing_imports = True
   disallow_incomplete_defs = False
   ```

---

## Communication Issues

### Issue: Gateway Won't Start

**Problem**: Server crashes on initialization

**Symptoms**:
```python
OSError: Address already in use
# or
socket.error: [Errno 48] Address already in use
```

**Solutions**:

1. **Check firewall**
   ```bash
   # macOS
   sudo lsof -i :8888
   
   # Ubuntu
   sudo netstat -tulpn | grep :8888
   ```

2. **Wait for socket timeout**
   - TCP sockets take ~60 seconds to fully release
   - Use SO_REUSEADDR:
   ```python
   socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   ```

3. **Use ephemeral port**
   ```python
   gateway = GatewayServer(port=0)  # OS chooses available port
   print(f"Listening on {gateway.socket.getsockname()}")
   ```

---

### Issue: Messages Not Received

**Problem**: RX queue stays empty

**Symptoms**:
```python
msg = gateway.get_telemetry(timeout=5)  # Returns None
```

**Debugging**:

1. **Check queue depth**
   ```python
   depth = gateway.rx_queue.qsize()
   print(f"Queue depth: {depth}")
   ```

2. **Verify sender is connected**
   ```python
   print(gateway.robot_addresses)
   # Should show: {robot_id: (ip, port), ...}
   ```

3. **Check for deserialization errors**
   - Enable debug logging:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## Vision System Issues

### Issue: Camera Not Found

**Problem**: OpenCV can't open camera

**Error**:
```python
error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```

**Solutions**:

1. **Check camera number**
   ```python
   # List available cameras
   import cv2
   for i in range(5):
       cap = cv2.VideoCapture(i)
       if cap.isOpened():
           print(f"Camera {i} found")
           cap.release()
   ```

2. **Check permissions** (Linux)
   ```bash
   sudo usermod -a -G video $USER
   # Log out and back in
   ```

3. **Try default camera**
   ```python
   camera = Camera(device_id=0, width=1280, height=720)
   ```

---

### Issue: ArUco Detection Too Slow

**Problem**: Detection takes >100ms per frame

**Optimization**:

1. **Reduce frame size**
   ```python
   camera = Camera(device_id=0, width=640, height=480)  # Half size
   ```

2. **Use smaller dictionary**
   ```python
   detector = ArucoDetector(marker_size_mm=100)
   # Uses 5x5 bit dictionary (smaller = faster)
   ```

3. **Profile the code**
   ```bash
   pip install line-profiler
   kernprof -l -v vision/src/aruco_detector.py
   ```

---

## Build System Issues

### Issue: CMake Configuration Fails

**Problem**: Desktop build can't find dependencies

**Error**:
```
CMake Error at CMakeLists.txt:10 (find_package):
Could not find OpenCV
```

**Solutions**:

1. **Install OpenCV for desktop**
   ```bash
   # Ubuntu
   sudo apt install libopencv-dev
   
   # macOS
   brew install opencv
   
   # Windows
   conda install opencv
   ```

2. **Specify OpenCV path**
   ```bash
   cmake .. -DOpenCV_DIR=/usr/local/opt/opencv/lib/cmake/opencv4
   ```

---

## Performance Issues

### Issue: Main Loop Running Too Slow

**Problem**: Firmware loop takes >10ms

**Debugging**:
```cpp
// In main.cpp
unsigned long loop_start = micros();
// ... loop code ...
unsigned long loop_time = micros() - loop_start;
if (loop_time > 10000) {
    printf("Slow loop: %lu us\n", loop_time);
}
```

**Optimization**:
1. Reduce sensor reads
2. Decrease PID update rate
3. Move heavy work to separate task

---

## Getting More Help

**Debug Logs**:
```bash
# Enable verbose output
pio run -t upload --verbose
pytest -vv --tb=long
```

**System Information**:
```bash
# Python
python -c "import sys, cv2, numpy; print(sys.version, cv2.__version__)"

# Firmware
pio system info
```

**Check Logs**:
- Firmware: Serial output (115200 baud)
- Python: `python -m pytest --capture=no testing/`
- Gateway: Enable logging (DEBUG level)

**Report Issues**:
- [GitHub Issues](https://github.com/yourorg/issues)
- Include error logs and reproduction steps

