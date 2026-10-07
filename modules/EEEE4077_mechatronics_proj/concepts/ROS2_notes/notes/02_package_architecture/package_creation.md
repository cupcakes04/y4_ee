# Package Creation & File Layout

> **Doc References:**  
> - Local: [`ros2_documentation/.../Creating-Your-First-ROS2-Package.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.rst)  
> - Web: [ROS 2 Creating Your First Package Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

---

## 1. Package Creation Commands

Always run `ros2 pkg create` from inside your `ros2_ws/src/` directory:

### Python Package (`ament_python`):
```bash
cd ros2_ws/src

ros2 pkg create --build-type ament_python --license Apache-2.0 <package_name> --dependencies rclpy std_msgs
```

### C++ Package (`ament_cmake`):
```bash
cd ros2_ws/src

ros2 pkg create --build-type ament_cmake --license Apache-2.0 <package_name> --dependencies rclcpp std_msgs
```

*(Optional: Append `--node-name <my_node>` to have ROS 2 auto-generate a starter node file).*

---

## 2. Python vs C++ Directory Anatomy

| Python (`ament_python`) | C++ (`ament_cmake`) |
| :--- | :--- |
| ```<pkg>/├── package.xml├── setup.py├── setup.cfg├── resource/│   └── <pkg>└── <pkg>/    ├── __init__.py    └── my_node.py``` | ```<pkg>/├── package.xml├── CMakeLists.txt├── include/<pkg>/│   └── ...└── src/    └── my_node.cpp``` |

### Key Differences:
- **Python:** Entry points (executable names mapped to `main` functions) are declared in `setup.py`. Code lives in the inner `<pkg>/` folder alongside `__init__.py`.
- **C++:** Targets (executables, libraries, linked dependencies) are declared in `CMakeLists.txt`. Source code lives in `src/`.
- **Both:** Require a valid `package.xml` specifying the package format, maintainer, license, and dependencies.
