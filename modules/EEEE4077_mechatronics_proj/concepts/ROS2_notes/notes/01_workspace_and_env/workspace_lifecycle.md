# Workspace Lifecycle & Mental Model

> **Doc References:**  
> - Local: [`ros2_documentation/.../Creating-A-Workspace.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.rst)  
> - Web: [ROS 2 Creating a Workspace Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

---

## 1. Directory Structure: What Lives Where

```
ros2_ws/
├── src/        <-- [YOUR CODE] Packages live here. ONLY edit files inside this folder!
├── build/      <-- [BUILD CACHE] CMake / setuptools build artifacts. Safe to delete.
├── install/    <-- [PACKAGED OUTPUT] Sourced environment, binaries, python libs. Safe to delete.
└── log/        <-- [LOGGING] Logs generated during colcon build invocations. Safe to delete.
```

### The 3 Ground Rules
1. **Never edit `build/` or `install/` directly.** Any manual changes will be wiped on the next build.
2. **Always build from the workspace root (`ros2_ws/`), not from `src/`.**
3. **If builds get corrupted or weird:** run `rm -rf build install log` and re-run `colcon build`.

---

## 2. Underlay vs. Overlay

```
  ┌────────────────────────────────────────────────────────┐
  │  Overlay: <workspace>/ros2_ws/install/setup.bash       │ <-- Your custom packages
  ├────────────────────────────────────────────────────────┤
  │  Underlay: /opt/ros/jazzy/setup.bash                   │ <-- System ROS 2 packages
  └────────────────────────────────────────────────────────┘
```

- **Underlay:** The base ROS 2 system installation provided by the OS package manager (`/opt/ros/jazzy/setup.bash`).
- **Overlay:** Your workspace. When sourced, it intercepts package searches: if your workspace has a package with the same name as the underlay, **the overlay version takes precedence**.

### Which setup script do you source?
- `source install/setup.bash` *(Recommended)*: Chains both your overlay AND the underlay it was built against.
- `source install/local_setup.bash`: Only exposes the packages in your current workspace without chaining the underlay.

---

## 3. The 5-Step Development Loop

| Step | Action | Command | Where to run |
| :--- | :--- | :--- | :--- |
| **1** | Write or edit code | Edit files in `src/<package_name>/...` | `ros2_ws/src/` |
| **2** | Build target package | `colcon build --packages-select <pkg> --symlink-install` | `ros2_ws/` |
| **3** | Open runtime terminal | `source install/setup.bash` | `ros2_ws/` |
| **4** | Execute node | `ros2 run <pkg> <executable_name>` | Any terminal |
| **5** | Inspect & debug | `ros2 topic list`, `ros2 node info /<node_name>` | Another terminal |

---

## 4. The `--symlink-install` Superpower

```bash
colcon build --packages-select my_py_package --symlink-install
```

- **Without `--symlink-install`:** Colcon copies `.py` files into `install/`. Every time you change 1 line of Python, you must run `colcon build`.
- **With `--symlink-install`:** Colcon creates symbolic links in `install/` pointing directly to your `.py` source code in `src/`.
- **Result:** You edit Python code $\rightarrow$ save file $\rightarrow$ re-run `ros2 run`. **No build needed!**
- *(Note: You still need to run `colcon build` if you change `package.xml`, `setup.py` entry points, or C++ code).*
