# image_process

This package is example for basic image processing with ros ,That will detect aruco marker and visualize the output.

## Install

change directory to src file in yout worksapce ,For my case is rmrc_ws.
```bash
cd rmrc_ws/src
```

clone package 
```bash
git clone git@github.com:TanakornKulsri/iRAP_RMRC.git iRAP_RMRC/image_process
```
This command will install iRAP_RMRC directory to your worksapce and image_process is sub-directory in it.

make worksapce 
```bash
cd ..
catkin_make
```

## Run 

```bash
roslaunch image_process marker_detect.launch
```

check output image 
```bash
rosrun rqt_image_view rqt_image_view 
```
change topic to /detect_marker/image_raw/compressed

output
