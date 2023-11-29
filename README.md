# autonomous-bittle
This repository holds the code and configuration for the autonomous swarm robotics project in the CMU-MAIL lab

# Set up raspberry pi
1. Flash image using raspberry pi imager:
   - raspberry pi OS (Legacy) Lite Bullseye
2. On first Power up:
   - Select Keyboard layout
   - set pi as username, select password
   - Log in
3. Set up wifi:
   - sudo raspi-config
   - Localisation Options
   - Set Timezone and WLAN Country
   - go to Advanced Options, set network config to use NetworkManager
   - go to system settings, enter wifi ssid and password
5. Set auto login:
   - 1. S5 Boot / Auto Login
6. Set up interface options
   - 3 Interface Options
   - Enable Legacy Camera support
   - Enable SSH
   - I6 Serial port: Disable Login Shell, Enable Serial port hardware
   - Ensure one wire communication disabled
   - Enable remote GPIO pins
7. Reboot
8. sudo apt-get update 
9. sudo apt-get install git
10. git clone https://github.com/PetoiCamp/OpenCat.git
11. sudo apt-get install python3-opencv -y
12. Set up virtual environment for python:
    - sudo apt-get install python3-virtualenv
    - mkdir project
    - cd project
    - python3 -m virtualenv env
    - source env/bin/activate
13. sudo apt-get install pip
14. Install pyserial: pip install pyserial
15. sudo apt-get install python3-tk

# Connect to raspberry pi through ssh
1. Hook the pi up to a monitor and type: ifconfig
2. note the ip address for the pi
3. On your desktop terminal type: ssh pi@<the ip address for the pi>
4. You will be prompted for the password for the pi. You can now disconnect the monitor from the pi

# Send commands to bittle through ardserial.py via ssh

# Start video streaming from raspberry pi to desktop
