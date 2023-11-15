# autonomous-bittle
This repository holds the code and configuration for the autonomous swarm robotics project in the CMU-MAIL lab

# Set up raspberry pi
1. Flash image using raspberry pi imager:
   a. raspberry pi OS (Legacy) Lite Bullseye
2. On first Power up:
   a. Select Keyboard layout
   b. set pi as username, select password
   c. Log in
3. Set up wifi:
   - sudo raspi-config
   - Localisation Options
   c. Set Timezone and WLAN Country
   d. go to Advanced Options, set network config to use NetworkManager
   e. go to system settings, enter wifi ssid and password
5. Set auto login:
   a. 1. S5 Boot / Auto Login
6. Set up interface options
   a. 3 Interface Options
   b. Enable Legacy Camera support
   c. Enable SSH
   d. I6 Serial port: Disable Login Shell, Enable Serial port hardware
   e. Ensure one wire communication disabled
   f. Enable remote GPIO pins
7. Reboot
8. sudo apt-get update && sudo apt-get upgrade
9. sudo apt-get install git
10. git clone https://github.com/PetoiCamp/OpenCat.git
11. sudo apt-get install python3-opencv -y
