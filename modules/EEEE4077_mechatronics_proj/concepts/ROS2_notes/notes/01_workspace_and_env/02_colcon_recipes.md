# Colcon Build Recipes & Workspace Navigation

> **Doc References:**  
> - Local: [`ros2_documentation/.../Colcon-Tutorial.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.rst)  
> - Web: [ROS 2 Colcon Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)

---

## 1. Quick `colcon build` Command Reference

Always run these from the workspace root (`ros2_ws/`):

| Purpose | Command |
| :--- | :--- |
| **Standard Python dev build** | `colcon build --packages-select <pkg> --symlink-install` |
| **Build pkg + its dependencies** | `colcon build --packages-up-to <pkg> --symlink-install` |
| **Stream live compiler stdout** | `colcon build --event-handlers console_direct+` |
| **Sequential build (single core)** | `colcon build --executor sequential` |
| **Skip unit tests (faster build)** | `colcon build --cmake-args -DBUILD_TESTING=0` |
| **Clean workspace rebuild** | `rm -rf build/ install/ log/ && colcon build --symlink-install` |

---

## 2. Skipping Packages (`COLCON_IGNORE`)

If you have a heavy package or an external clone in `src/` that you don't want Colcon to build:

```bash
cd ros2_ws/src/heavy_package
touch COLCON_IGNORE
```

Colcon will completely skip building this folder. Delete the empty `COLCON_IGNORE` file when you want to build it again.

---

## 3. Fast Workspace Navigation with `colcon_cd`

Jump directly to any package directory from anywhere in your terminal (`colcon_cd <package_name>`):

### Setup (Run once in bash):
```bash
echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
# Set root to your workspace install path:
echo "export _colcon_cd_root=~/ros2_ws/install" >> ~/.bashrc
source ~/.bashrc
```

### Usage:
```bash
colcon_cd py_pubsub     # Immediately jumps to ~/ros2_ws/src/py_pubsub
```

---

## 4. Colcon Mixins (Shorthand Macros)

Mixins replace long CMake flags with simple shorthand switches.

### Setup (Run once):
```bash
colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
colcon mixin update default
```

### Common Mixins:
| Mixin Flag | Equivalent Flag | Use Case |
| :--- | :--- | :--- |
| `--mixin debug` | `-DCMAKE_BUILD_TYPE=Debug` | Compiling C++ with GDB symbols |
| `--mixin release` | `-DCMAKE_BUILD_TYPE=Release` | Maximum compiler optimizations |
| `--mixin ccache` | Uses compiler cache | Drastically speeds up C++ rebuilds |
