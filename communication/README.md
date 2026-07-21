# Communication

## Overview

This module implements the communication layer for decentralized swarm coordination and centralized gateway communication. It supports ESP-NOW for inter-robot messaging and UDP for robot-to-dashboard telemetry.

## Structure

```
communication/
├── protocol/              # Message protocol definitions
│   ├── messages.py        # Message schema and serialization
│   ├── robot_id.py        # Robot identification
│   └── packet_format.py   # Binary packet structure
├── esp_client/            # ESP32 embedded client
│   ├── esp_now_client.c   # ESP-NOW implementation
│   └── udp_client.c       # UDP client
├── gateway/               # Desktop gateway server
│   ├── gateway.py         # Main gateway process
│   ├── message_router.py  # Message routing logic
│   ├── device_manager.py  # Robot device tracking
│   └── telemetry_db.py    # Telemetry storage
└── README.md              # This file
```

## Communication Protocols

### ESP-NOW (Robot-to-Robot)

- **Range**: 200-300 meters (line of sight)
- **Latency**: 5-10ms
- **Throughput**: Up to 1000 messages/sec
- **Message size**: 250 bytes max
- **Features**:
  - Unicast and broadcast modes
  - Automatic retransmission
  - Channel hopping for interference avoidance

### UDP (Robot-to-Dashboard)

- **Range**: Network-dependent (LAN)
- **Port**: 8888 (configurable)
- **Latency**: 10-50ms (LAN)
- **Throughput**: Limited by network bandwidth
- **Features**:
  - Heartbeat mechanism
  - Message acknowledgment
  - Graceful degradation on packet loss

## Message Types

### Heartbeat

```
[HEARTBEAT | robot_id | timestamp | battery_level | status]
Size: 16 bytes
Frequency: 1 Hz
```

### Task Allocation

```
[TASK | task_id | target_x | target_y | priority | deadline]
Size: 24 bytes
```

### Telemetry

```
[TELEMETRY | robot_id | x | y | theta | v | battery | temp]
Size: 32 bytes
```

### Obstacle Report

```
[OBSTACLE | robot_id | obstacle_x | obstacle_y | severity | timestamp]
Size: 20 bytes
```

## Gateway Server

### Features

- Multi-threaded message processing
- Automatic robot discovery
- Persistent telemetry logging
- JSON API for dashboard integration

### Running the Gateway

```bash
python communication/gateway/gateway.py --port 8888 --db-file telemetry.db
```

## ESP-NOW Client Setup

```c
#include "esp_now_client.h"

void setup() {
    esp32::ESPNowClient client(0x01);  // Robot ID: 1
    client.initialize(CHANNEL);
    client.subscribe(message_callback);
}

void message_callback(const esp32::Message& msg) {
    // Handle incoming message
}
```

## Performance

### Latency

| Operation | Min | Max | Avg |
|-----------|-----|-----|-----|
| ESP-NOW round-trip | 5ms | 20ms | 10ms |
| UDP round-trip | 2ms | 50ms | 10ms |
| Gateway message routing | 0.5ms | 5ms | 2ms |

### Throughput

- **ESP-NOW**: 100-300 msg/sec per robot pair
- **UDP Gateway**: 1000+ msg/sec
- **Network**: Limited by hardware

## Security (Future)

- [ ] Message signing with HMAC
- [ ] Replay attack detection
- [ ] TLS for UDP gateway
- [ ] Robot authentication framework

## API Reference

### Protocol Messages

See `communication/protocol/messages.py` for complete message definitions.

### Gateway REST API

- `GET /robots` - List connected robots
- `GET /robots/{id}/status` - Robot status
- `GET /telemetry/{id}` - Robot telemetry data
- `POST /task/allocate` - Allocate task to robot
