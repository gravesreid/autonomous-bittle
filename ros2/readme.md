# Setup instructions for ROS2 Bittle Package
## create the package
### go to your workspace:
```bash
cd ~/ros2_ws/src
```
### create the package
```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 bittle_ros2
```
### copy the bittle driver script
```bash
wget https://raw.githubusercontent.com/gravesreid/bittle_ROS2/main/bittle_ROS2/bittle_driver.py
```
