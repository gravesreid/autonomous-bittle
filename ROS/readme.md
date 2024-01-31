# I set up a ROS2 wrapper for Bittle. The instructions and code are here:
https://github.com/gravesreid/bittle_ros2

# this is the step by step guide to use ROS noetic with Bittle
## On the Pi, install docker: 
```bash
sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi
```
## Download the docker image
```bash
git clone https://github.com/osrf/docker_images.git
cd docker_images/ros/your_distro/debian/buster/robot
docker build -t ros_docker .
```


## Set up pi to work with a remote ROS Master
### create a new script:
```bash
touch use_robot.sh
```
### Edit the script
```bash
vim use_robot.sh
```
### Paste this text in (from https://gist.github.com/chfritz/8c2adab45a94e091be77c55b0432ad2e)
```bash
#!/bin/bash

# Simple script to setup your machine env to use a remote ROS master
# example usage: use_robot.sh myrobot
# where myrobot is a resolvable hostname or an IP address

NORMAL=`tput sgr0 2> /dev/null`
GREEN=`tput setaf 2 2> /dev/null`

# get the IP of our device we'll use to conect to the host
TARGET_IP=$1
IP=`ip route get $TARGET_IP | head -n 1 | sed "s/.*src \(\S*\) .*/\1/"`

echo -e "${GREEN}using $1 ($TARGET_IP) via $IP${NORMAL}"

export ROS_MASTER_URI=http://$1:11311
export ROS_HOSTNAME=$IP
export ROS_IP=$IP
```
### source the script
```bash
source use_robot.sh [master_node_ip]
```

