# Simulation

## Overview

This directory provides infrastructure for simulating the warehouse robot platform before deploying to physical hardware. It includes warehouse environment simulation and bridges for future ROS2 integration.

## Structure

```
simulation/
├── warehouse_env/          # Warehouse environment simulator
│   ├── warehouse.py        # Core environment
│   ├── robot_model.py      # Robot dynamics model
│   ├── obstacles.py        # Obstacle representation
│   ├── visualizer.py       # PyQt5 visualization
│   └── physics.py          # Physics engine
│
└── ros2_bridge/            # ROS2 integration (future)
    ├── robot_state_pub.py  # State publisher
    └── command_sub.py      # Command subscriber
```

## Using the Warehouse Simulator

### Prerequisites

```bash
pip install -e ".[vision,dashboard]"
```

### Launch Simulator

```python
from simulation.warehouse_env.warehouse import WarehouseSimulation

sim = WarehouseSimulation(width=10, height=10, num_robots=1)
sim.run()
```

### Python API

```python
# Create simulation
warehouse = WarehouseSimulation(
    width=10.0,    # meters
    height=10.0,
    num_robots=2,
    realtime=True
)

# Add obstacles
warehouse.add_obstacle(5.0, 5.0, 1.0, 1.0)  # x, y, width, height

# Control robots
robot = warehouse.robots[0]
robot.move_to(8.0, 8.0, speed=0.5)

# Get telemetry
x, y, theta = robot.get_pose()
battery = robot.battery_level

# Step simulation
warehouse.step(dt=0.01)  # 10ms timestep
```

## Visualization Features

- Real-time robot position and orientation
- Obstacle map and boundaries
- Sensor ranges (visualization)
- Trajectory history
- Performance metrics (FPS, simulation speed)

## Physics Model

### Robot Dynamics

The robot uses a differential drive model:

```
v_left = (PWM_left / 255) * v_max
v_right = (PWM_right / 255) * v_max

x_dot = (v_left + v_right) / 2 * cos(theta)
y_dot = (v_left + v_right) / 2 * sin(theta)
theta_dot = (v_right - v_left) / wheel_base
```

### Sensor Simulation

- **IR Array**: Simulates line detection
- **Ultrasonic**: Range sensing with noise
- **IMU**: Accelerometer and gyroscope readings

## Future: ROS2 Integration

Bridge code for ROS2 will provide:

- `/robot_0/state` publisher (Odometry)
- `/robot_0/cmd_vel` subscriber (Geometry/Twist)
- `/robot_0/sensor/ir` publisher (Array data)
- `/robot_0/sensor/range` publisher (Range data)

## Integration with Dashboard

Simulated robots are indistinguishable from real ones in the dashboard:

```python
from simulation.warehouse_env.warehouse import WarehouseSimulation
from vision.src.dashboard import WarehouseDashboard

# Start simulator
sim = WarehouseSimulation(num_robots=3)
sim_thread = Thread(target=sim.run, daemon=True)
sim_thread.start()

# Start dashboard (connects to simulated robots)
dashboard = WarehouseDashboard(port=8888)
dashboard.start()
```

## Benchmark Scenarios

### Scenario 1: Single Robot Line Following

- Simulate IR-based line detection
- Test PID parameters in simulation before deployment
- Measure convergence time and overshoot

### Scenario 2: Multi-Robot Coordination

- 2-5 robots in warehouse
- Collision avoidance testing
- Task allocation validation

### Scenario 3: Failure Scenarios

- Robot motor failure
- Communication loss
- Sensor malfunction recovery

## Performance

- **Simulation speed**: 10-20× wallclock speed (depends on complexity)
- **Framerate**: 30 FPS rendering
- **Timestep**: 10ms (configurable)

## Extending the Simulator

### Add Custom Robot

```python
from simulation.warehouse_env.robot_model import Robot

class CustomRobot(Robot):
    def __init__(self, x, y, theta):
        super().__init__(x, y, theta)
        # Custom properties
        
    def update_sensors(self, warehouse):
        # Custom sensor simulation
        pass
```

### Add Custom Obstacles

```python
warehouse.add_obstacle(3.0, 3.0, 2.0, 0.5)  # Rectangular
warehouse.add_circle_obstacle(5.0, 5.0, r=0.5)  # Circular
```

## Future Enhancements

- [ ] URDF robot model loading
- [ ] ROS2 middleware integration
- [ ] Gazebo environment export
- [ ] Physics-based constraints
- [ ] Multi-physics solver backend
