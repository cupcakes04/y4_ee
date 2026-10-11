# ROS 2 CLI Master Cheatsheet

> **Doc References:**  
> - Local: [`ros2_documentation/.../Beginner-CLI-Tools.rst`](../../ros2_documentation/source/Tutorials/Beginner-CLI-Tools.rst)  
> - Web: [ROS 2 Beginner CLI Tools](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html)

---

## 1. Node Commands (`ros2 node`)

| Command | Description |
| :--- | :--- |
| `ros2 node list` | List all running active nodes in the domain |
| `ros2 node info /<node_name>` | Show publishers, subscribers, services, and actions for a node |

---

## 2. Topic Commands (`ros2 topic`)

| Command | Description |
| :--- | :--- |
| `ros2 topic list` | List all active topics (`-t` shows types, `-v` shows details) |
| `ros2 topic echo /<topic>` | Stream live messages to terminal (`--csv` or `--once` options) |
| `ros2 topic pub /<topic> <type> "<yaml_data>"` | Publish message: `ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}}"` |
| `ros2 topic pub --rate 10 /<topic> <type> "<data>"` | Publish continuously at 10 Hz |
| `ros2 topic hz /<topic>` | Measure publication rate (Hz) |
| `ros2 topic bw /<topic>` | Measure bandwidth usage (bytes/sec) |
| `ros2 topic info /<topic>` | Show subscriber count, publisher count, and message type |

---

## 3. Service Commands (`ros2 service`)

| Command | Description |
| :--- | :--- |
| `ros2 service list` | List all available service endpoints (`-t` shows types) |
| `ros2 service type /<service>` | Show the interface type of a service |
| `ros2 service find <interface_type>` | Find all services matching a given interface type |
| `ros2 service call /<service> <type> "<data>"` | Trigger service: `ros2 service call /spawn turtlesim/srv/Spawn "{x: 2, y: 2}"` |

---

## 4. Action Commands (`ros2 action`)

| Command | Description |
| :--- | :--- |
| `ros2 action list` | List all available actions (`-t` shows types) |
| `ros2 action info /<action>` | Show servers and clients connected to the action |
| `ros2 action send_goal /<action> <type> "<data>"` | Dispatch a goal to an action server |
| `ros2 action send_goal --feedback /<action> <type> "<data>"` | Dispatch goal and print feedback stream live |

---

## 5. Parameter Commands (`ros2 param`)

| Command | Description |
| :--- | :--- |
| `ros2 param list` | List all parameters across active nodes |
| `ros2 param get /<node> <param_name>` | Read parameter value |
| `ros2 param set /<node> <param_name> <value>` | Modify parameter value at runtime |
| `ros2 param dump /<node> > params.yaml` | Export parameters to a YAML file |
| `ros2 param load /<node> params.yaml` | Load parameters from a YAML file |

---

## 6. Bag Recording & Playback (`ros2 bag`)

| Command | Description |
| :--- | :--- |
| `ros2 bag record -a -o <bag_name>` | Record all topics to `<bag_name>` |
| `ros2 bag record -o <bag_name> /topic1 /topic2` | Record specific topics only |
| `ros2 bag info <bag_dir>` | Inspect message counts, duration, and topics in a bag |
| `ros2 bag play <bag_dir>` | Play back recorded data into active topics |
| `ros2 bag play -r 2.0 <bag_dir>` | Play back at 2x playback speed |

---

## 7. Package & Execution (`ros2 pkg` / `ros2 run`)

| Command | Description |
| :--- | :--- |
| `ros2 pkg list` | List all available packages in underlay & overlay |
| `ros2 pkg executables <package_name>` | List executable node targets in a package |
| `ros2 pkg prefix <package_name>` | Print the install path of a package |
| `ros2 run <package_name> <executable>` | Execute a node |
| `ros2 run <pkg> <exe> --ros-args -r __node:=<new_name>` | Remap node name at startup |
| `ros2 run <pkg> <exe> --ros-args -r <old_topic>:=<new_topic>` | Remap topic name at startup |
