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
   ```bash
   sudo raspi-config
   ```
   - Localisation Options
   - Set Timezone and WLAN Country
   - go to Advanced Options, set network config to use NetworkManager
   - go to system settings, enter wifi ssid and password
5. Set auto login:
   - 1. S5 Boot / Auto Login
6. Set up interface options
   - 3 Interface Options
   - Enable Legacy Camera support
   - Enable SSHago
   - I6 Serial port: Disable Login Shell, Enable Serial port hardware
   - Ensure one wire communication disabled
   - Enable remote GPIO pins
7. Reboot
8. Fix locale issues:
9.
```bash
   sudo nano /etc/locale.gen
```
In file, uncomment line #en_US.UTF-8
```bash
sudo locale-gen
```
Set locale:
```bash
sudo update-locale LANG=en_US.UTF-8
```
Reboot

10. Install necessary packages:
```bash
sudo apt-get update
```
```bash
bash sudo apt-get install git
```
```bash
git clone https://github.com/PetoiCamp/OpenCat.git
```
```bash
git clone https://github.com/gravesreid/autonomous-bittle.git
```
```bash
sudo apt-get install python3-opencv -y
```
```bash
sudo apt-get install pip
```
```bash
sudo apt-get install python3-tk
```
```bash
pip install pyserial
```
11. Edit bash path:
```bash
sudo apt-get install vim -y
vim ~/.bashrc
```
at the end of the file add:  export PATH=$PATH:/home/pi/.local/bin


# If you have issues with accessing port ttyS0 (this disables bluetooth):
```bash
 sudo vim /boot/config.txt
```
1. add: dtoverlay=disable-bt
2. Enter to terminal:
```bash
sudo systemctl stop hciuart
```
```bash
sudo systemctl disable hciuart
```
```bash
sudo reboot
```


# Set up virtual environment for python:
```bash
sudo apt-get install python3-virtualenv
```
```bash
mkdir project
```
```bash
cd project
```
```bash
python3 -m virtualenv env
```
```bash
source env/bin/activate
```

# Connect to raspberry pi through ssh
1. Hook the pi up to a monitor and type:
 ```bash
ifconfig
```
2. note the ip address for the pi
3. On your desktop terminal type:
```bash
ssh pi@[pi_ip_address]
```
4. You will be prompted for the password for the pi. You can now disconnect the monitor from the pi

# If you get error: WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
```bash 
ssh-keygen -f "/home/[your_username]/.ssh/known_hosts" -R [ip.address]
```

# Send commands to bittle through ardserial.py via ssh
```bash
cd ~/Opencat/serialMaster
```
```bash
python3 ardserial.py
```
Now you can enter commands through the terminal

# Start video streaming from raspberry pi to desktop
1. run ifconfig on your desktop terminal ```bash ifconfig ```
2. enter the desktop ip address in both the sender.py and receiver.py scripts
3. On the desktop, run
```bash
python3 receiver.py
```
4. on the pi, run
```bash
python3 sender.py
```

# Send files from one machine to another (1st part is file being copied)
```bash
scp /path/to/local/file username@remotehost:/path/to/remote/directory
```

# Send entire directory from one machine to another
```bash
scp -r /path/to/local/directory username@remotehost:/path/to/remote/directory
```

# Operate bittle to receive commands based on object recognition
1. Set up two terminals with ssh to pi
2. Open one terminal in bittle python environment on desktop
3. On first bittle terminal run
```bash
   python3 ardSocket.py
   ```
4. On desktop terminal run
```bash
python3 receiver.py
``` 
5. On second bittle terminal run
```bash
python3 sender.py
```

