# iRAP_RMRC
Description about iRAP RMRC Robot

## Ubuntu Setup
Ubuntu 20.04 Desktop Image : https://releases.ubuntu.com/focal/

Instruction for Install Ubuntu : https://ubuntu.com/tutorials/install-ubuntu-desktop

Install ROS Noetic : http://wiki.ros.org/noetic/Installation/Ubuntu

### Recommend Software
After setup ubuntu on laptop we recommend to install software ,that will support software development on linux OS

Network Tools
```bash
sudo apt install net-tools 
```

OpenSSH
```bash
sudo apt install openssh-server 
```

Terminator
```bash
sudo apt install terminator 
```

## Raspberry PI4 Setup
For iRAP RMRC Robot we use raspberry PI4 ,that is embeaded computer .This section will explain how to setup it.

Ubuntu 20.04 Mate Image : https://releases.ubuntu-mate.org/20.04/arm64/

1. Install ubuntu-mate-20.04.1-desktop-arm64+raspi.img.xz.
2. Flash image file to SD card.
3. Install ROS Noetic (We recommend to install ROS-Base).
4. Install additional software.

## Create First ROS Workspace
Press [ctrl+alt+t] for open terminal window.

create workspace 
```bash
mkdir -p ~/rmrc_ws/src
cd ~/rmrc_ws/
catkin_make
```
After create workspace, you should to source workspace for use package in it.
```bash
source devel/setup.bash
```

For source this workspace every time you open terminal 
```bash
nano .bashrc
```

Add Command to .bashrc file
```bash
source ~/rmrc_ws/devel/setup.bash
```

Additional Documentation 

[Creating a workspace for catkin](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)

[ROS Tutorials](http://wiki.ros.org/ROS/Tutorials)

## Open Raspberry PI4 Serial Port
Before you use serial port to communicate with microcontroller such as arduino Nano. You should to open and give permission for it.

Open Serial Port : https://github.com/NonStopBle/PiAttachSerial

Check Serial Port list : 

```bash
ls /dev/tty*
```
Give Permission :

```bash
sudo chmod a+rw /dev/ttyAMA0
```

## Additional Software

### Library and Example Code for iRAP Extension Board

iRAP_RMRCBreakout : https://github.com/mtikkyu/iRAP_RMRCBreakout

### Web Interface Package

irap_mini_rescue_GUI : https://github.com/NonStopBle/iRAP-Minirescue-GUI

irap_webengine : https://github.com/NonStopBle/iRAP-WebEngine/

### Image Processing Package

3.image_process : https://github.com/TanakornKulsri/iRAP_RMRC/tree/main/image_process
