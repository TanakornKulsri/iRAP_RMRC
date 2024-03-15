# iRAP_RMRC
Description about iRAP RMRC Robot

## Ubuntu Setup
Ubuntu 20.04 Desktop Image : https://releases.ubuntu.com/focal/

Install Ubuntu Documentation : https://ubuntu.com/tutorials/install-ubuntu-desktop

Install ROS Noetic Documentation : http://wiki.ros.org/noetic/Installation/Ubuntu

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
For iRAP RMRC Robot we use raspberry PI4 ,that is embedded computer.This section will explain how to setup it.

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

## ROS Network Setup
For setting your labtop to communicate with embedded computer(raspberry PI4) on robot .

1. Set your labtop and raspberry Pi login in same network.
   For example raspberry Pi(master) IP:192.168.1.100 and labtop(host) IP:192.168.1.32

2. Open .bashrc file
```bash
nano ~/.bashrc
```

3. Add ROS_HOSTNAME and ROS_MASTER config to .bashrc file. In raspberry PI
```bash
export ROS_HOSTNAME=master_ip
export ROS_MASTER_URI=http://master_ip:11311
```

In my case, I should replace master_ip to 192.168.1.100

```bash
export ROS_HOSTNAME=192.168.1.100
export ROS_MASTER_URI=http://192.168.1.100:11311
```

4.Add ROS_HOSTNAME and ROS_MASTER config to .bashrc file. In laptop
```bash
export ROS_HOSTNAME=host_ip
export ROS_MASTER_URI=http://master_ip:11311
```

In my case, I should replace master_ip to 192.168.1.100 and host_ip to 192.168.1.32

```bash
export ROS_HOSTNAME=192.168.1.32
export ROS_MASTER_URI=http://192.168.1.100:11311
```

After set ROS_HOSTNAME and ROS_MASTER_URL you should to test 2 machine are communicated.

In raspberry PI4(master)
```bash
roscore
```

output 
```bash
started roslaunch server http://localhost:33797/
ros_comm version 1.16.0


SUMMARY
========

PARAMETERS
 * /rosdistro: noetic
 * /rosversion: 1.16.0

NODES

auto-starting new master
process[master]: started with pid [8499]
ROS_MASTER_URI=http://localhost:11311/

setting /run_id to 512c6820-e2c2-11ee-99c3-8b837eacd76e
process[rosout-1]: started with pid [8520]
started core service [/rosout]
```

In your labtop
```bash
rosnode list
```

output 
```bash
/rosout
```

If you can call rosnode list in your labtop without roscore that mean your labtop and raspberry PI4 are set in same ROS network ,So you can communicate data between your labtop to raspberry PI ,for example velocity command ,filpper position or image.

Additional Documentation : https://razbotics.wordpress.com/2018/01/23/ros-distributed-systems/


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

After open serial port ,you can send data from raspberry PI4(computer) to arduino Nano(microcontroller) by using ROSSERIAL.

## Additional Software

### Library and Example Code for iRAP Extension Board

iRAP_RMRCBreakout : https://github.com/mtikkyu/iRAP_RMRCBreakout

### Web Interface Package

irap_mini_rescue_GUI : https://github.com/NonStopBle/iRAP-Minirescue-GUI

irap_webengine : https://github.com/NonStopBle/iRAP-WebEngine/

### Image Processing Package

image_process : https://github.com/TanakornKulsri/iRAP_RMRC/tree/main/image_process

### USB Camera Package 
Documentation : http://wiki.ros.org/usb_cam

Github : https://github.com/ros-drivers/usb_cam

### ROSSERIAL Package
Documentation : http://wiki.ros.org/rosserial

Github : https://github.com/ros-drivers/rosserial

