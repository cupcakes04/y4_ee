# Debugging, Introspection, & GUI Tools

> **Doc References:**  
> - Local: [`ros2_documentation/.../Getting-Started-With-Ros2doctor.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Getting-Started-With-Ros2doctor.rst)  
> - Local: [`ros2_documentation/.../Using-Rqt-Console.rst`](../../ros2_documentation/source/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.rst)

---

## 1. Interface Introspection (`ros2 interface`)

Find out what data fields an interface expects before writing code:

| Command | Purpose |
| :--- | :--- |
| `ros2 interface show <interface_name>` | Print fields of a msg, srv, or action |
| `ros2 interface list` | List all available message and service types |
| `ros2 interface package <pkg>` | List interfaces provided by a specific package |

### Example (`ros2 interface show example_interfaces/srv/AddTwoInts`):
```text
int64 a
int64 b
---
int64 sum
```
*(Lines above `---` are Request fields; lines below are Response fields).*

---

## 2. Visual Introspection (`rqt`)

### `rqt_graph` (Computation Graph)
```bash
rqt_graph
```
- Visualizes all active nodes as ellipses and topics as rectangles.
- Best tool for checking if a publisher is actually connected to a subscriber or if topic names were mismatched.

### `rqt_console` (Log Viewer)
```bash
ros2 run rqt_console rqt_console
```
- Aggregates `get_logger().info()`, `warn()`, `error()` output from all nodes into a searchable GUI.

---

## 3. Diagnostics & Daemon Troubleshooting

### Check ROS 2 Health (`ros2 doctor`)
```bash
ros2 doctor           # Checks network, DDS, environment variables, dependencies
ros2 doctor --report  # Full comprehensive report of machine environment
```

### Resetting the ROS 2 Daemon
If nodes or topics are not appearing in `ros2 node list` or `ros2 topic list`:
```bash
ros2 daemon stop
ros2 daemon start
```

### Checking Domain ID
Ensure all communicating machines/terminals share the same `ROS_DOMAIN_ID`:
```bash
echo $ROS_DOMAIN_ID   # Default is 0 if unset
export ROS_DOMAIN_ID=42
```
