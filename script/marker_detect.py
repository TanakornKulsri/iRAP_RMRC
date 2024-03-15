#!/usr/bin/env python3

import rospy 

import cv2 
import numpy as np 

from sensor_msgs.msg import Image ,CompressedImage
from cv_bridge import CvBridge ,CvBridgeError

input_img = None 

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

arucoParams = cv2.aruco.DetectorParameters_create()

def input_img_callback(msg) : 
    global input_img 
    input_img = bridge.imgmsg_to_cv2(msg,'bgr8') 

if __name__ == "__main__" : 
    rospy.init_node("detect_marker")
    rospy.loginfo(":: Dectect Marker is Already ::")

    bridge = CvBridge()

    image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,input_img_callback)

    output_pub = rospy.Publisher("/detect_marker/image_raw/compressed",CompressedImage,queue_size=10)
    
    rate = rospy.Rate(10) 

    try : 
        while not rospy.is_shutdown() : 
            if input_img is not None : 
                # print(input_img)
                gray_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
                blur_img = cv2.GaussianBlur(gray_img,(5,5),0)
                thres_img = cv2.adaptiveThreshold(blur_img, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

                (corners, ids, rejected) = cv2.aruco.detectMarkers(thres_img, ARUCO_DICT,parameters=arucoParams)
                
                if len(corners) > 0 :
                    vis_img = np.copy(input_img)
                    vis_img = cv2.aruco.drawDetectedMarkers(vis_img,corners,ids)

                    output_pub.publish(bridge.cv2_to_compressed_imgmsg(vis_img))
                else : 
                    output_pub.publish(bridge.cv2_to_compressed_imgmsg(input_img))

            rate.sleep()

    except rospy.ROSInterruptException : 
        pass 

