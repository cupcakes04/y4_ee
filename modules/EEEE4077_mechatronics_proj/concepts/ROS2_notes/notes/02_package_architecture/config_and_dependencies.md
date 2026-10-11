# Configuration & Dependencies: `package.xml`, `setup.py`, & `CMakeLists.txt`

> **Doc References:**  
> - Local: [`ros2_documentation/.../Creating-Your-First-ROS2-Package.rst`](../../ros2_documentation/source/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.rst)  
> - Local: [`ros2_documentation/.../Rosdep.rst`](../../ros2_documentation/source/Tutorials/Intermediate/Rosdep.rst)

---

## 1. `package.xml` Dependency Tags

Every package uses a `package.xml` (Format 3). Declare all external packages here so `rosdep` and build tools can resolve them:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_package</name>
  <version>0.0.1</version>
  <description>Package description</description>
  <maintainer email="user@todo.todo">Author Name</maintainer>
  <license>Apache-2.0</license>

  <!-- Universal dependency (build + runtime): use this for most packages -->
  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>example_interfaces</depend>

  <!-- Python runtime-only dependency -->
  <exec_depend>numpy</exec_depend>

  <!-- Testing dependencies -->
  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type> <!-- or ament_cmake -->
  </export>
</package>
```

### Checking Missing Dependencies with `rosdep`:
```bash
cd ros2_ws
rosdep install -i --from-path src --rosdistro jazzy -y
```

---

## 2. Python Configuration: `setup.py` Entry Points

In Python packages, nodes are executed through **console scripts** defined in `setup.py`:

```python
from setuptools import find_packages, setup

package_name = 'my_py_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@todo.todo',
    description='My ROS 2 Python Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # format: '<cli_executable_name> = <pkg_module>.<py_filename>:<callable_function>'
            'my_talker = my_py_package.publisher_node:main',
            'my_listener = my_py_package.subscriber_node:main',
        ],
    },
)
```

> **Rule:** If you add or rename a script in `console_scripts`, you **must re-run `colcon build`**, even if using `--symlink-install`.

---

## 3. C++ Configuration: `CMakeLists.txt` Minimal Skeleton

In C++ packages, binaries are built and linked via CMake:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# 2. Declare executable target (target_name, source_file)
add_executable(my_cpp_node src/my_node.cpp)

# 3. Link ROS 2 dependencies
ament_target_dependencies(my_cpp_node rclcpp std_msgs)

# 4. Install target so "ros2 run" can find it
install(TARGETS
  my_cpp_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
```
