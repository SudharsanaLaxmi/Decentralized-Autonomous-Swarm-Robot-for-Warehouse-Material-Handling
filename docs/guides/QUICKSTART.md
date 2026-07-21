"""
Quick Start Guide

Get your first robot running in 30 minutes.
"""

# Quick Start Guide

Get your Autonomous Warehouse Robot up and running in 30 minutes.

## Prerequisites

- [ ] ESP32 DevKit-C v4 board
- [ ] USB cable (USB-C or Micro-USB)
- [ ] Assembled robot hardware (motor, sensors, battery)
- [ ] Computer with Python 3.8+ and pip
- [ ] 30 minutes of time

---

## Step 1: Clone the Repository (2 minutes)

```bash
git clone https://github.com/yourorg/swarm-warehouse-robot.git
cd swarm-warehouse-robot
```

---

## Step 2: Set Up Python Environment (5 minutes)

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 3: Install Firmware Tools (3 minutes)

```bash
pip install platformio
pio platform install espressif32
```

Verify:
```bash
pio boards list | grep esp32
```

---

## Step 4: Connect Your Board (2 minutes)

1. Plug ESP32 into USB port
2. Identify the port:
   - **Linux**: `/dev/ttyUSB0` or `/dev/ttyACM0`
   - **macOS**: `/dev/tty.usbserial-*`
   - **Windows**: `COM3` to `COM9`

3. Edit `firmware/platformio.ini`:
   ```ini
   [env:esp32_dev]
   upload_port = /dev/ttyUSB0   ; Change to your port
   ```

---

## Step 5: Upload Firmware (8 minutes)

```bash
cd firmware
platformio run -t upload
```

Expected output:
```
RAM:   [==        ]  16.4% (used 53668 bytes ...)
Flash: [====      ]  36.5% (used 477956 bytes ...)
Leaving...
Hard resetting via RTS pin...
```

---

## Step 6: Monitor Output (2 minutes)

```bash
platformio device monitor --baud 115200
```

You should see output like:
```
[INFO] System initialized
[INFO] Motor controller ready
[INFO] Sensors calibrated
[INFO] Main loop started
```

Press `Ctrl+C` to exit.

---

## Step 7: Test Motor Movement (3 minutes)

The robot will:
1. Move forward slowly for 2 seconds
2. Move backward slowly for 2 seconds
3. Stop

**Check for**:
- [ ] Both motors spinning
- [ ] Wheels moving smoothly
- [ ] No unusual noises
- [ ] LED indicators present

---

## Step 8: Run Python Examples (Bonus)

```bash
cd examples
python example_basic_control.py
```

This demonstrates:
- Vision system initialization
- Motor control patterns
- Communication setup

---

## Troubleshooting

### USB Port Not Found

```bash
# List available ports
pio device list

# Install drivers if needed (Windows/macOS)
# https://sparks.gogo.co.nz/ch340.html

# Check permissions (Linux)
sudo usermod -a -G dialout $USER
# Log out and back in
```

### Upload Fails

```bash
# Try different speed
platformio run -t upload --upload-speed 115200

# Or use slower option
platformio run -t upload -- --no-stub
```

### No Serial Output

1. Reset ESP32: Press reset button
2. Check baud rate: 115200
3. Try different cable
4. Update CH340 drivers

---

## Next Steps

✅ **Done!** Your robot is running.

### What's Next:

1. **Calibrate line sensors**: Run calibration routine (firmware)
2. **Test on marked line**: Place robot on a black line
3. **Tune PID controller**: Follow [PID_TUNING.md](PID_TUNING.md)
4. **Build more robots**: Scale to swarm
5. **Run full test suite**: `pytest testing/`

---

## Full Documentation

- [Installation Guide](INSTALLATION.md) - Detailed setup
- [Hardware Assembly](../hardware/README.md) - Build instructions
- [API Reference](../api/API_REFERENCE.md) - Code documentation
- [Architecture Overview](../architecture/SystemArchitecture.md) - System design
- [Examples](../../examples/) - Code samples

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourorg/issues)
- **Questions**: [GitHub Discussions](https://github.com/yourorg/discussions)
- **Docs**: [Full Documentation](../../docs/)
- **Examples**: [Code Examples](../../examples/)

---

**Version**: 0.4.0  
**Last Updated**: 2024  
**Status**: Production Ready
