#!/usr/bin/env python3 

import rospy 
from sensor_msgs.msg import Image, CompressedImage

from cv_bridge import CvBridge

import cv2 
import numpy as np
import math as m

usb_img_msg = None

def usb_img_callback(msg) : 
    global usb_img_msg
    usb_img_msg = msg  


if __name__ == "__main__" : 
    rospy.init_node("feature_matching")
    rospy.loginfo(":: Feature Matching is Already ::")
    usb_img_sub = rospy.Subscriber("/usb_cam/image_raw",Image,usb_img_callback)
    proc_img_pub = rospy.Publisher("proc_image",Image,queue_size=10)
    proc_compressedimg_pub = rospy.Publisher("proc_image/compressed",CompressedImage,queue_size=10)

    ref_img = cv2.imread("/home/first/rmrc_ws/src/iRAP_RMRC/image_process/script/reference_image.png")
    ref_img = cv2.cvtColor(ref_img,cv2.COLOR_RGB2BGR)

    cvbridge = CvBridge()

    rate = rospy.Rate(10)
    i = 0 
    try : 
        while not rospy.is_shutdown() : 
            if usb_img_msg is not None : 
                usb_img = cvbridge.imgmsg_to_cv2(usb_img_msg,desired_encoding="passthrough")
                output_img = np.copy(ref_img)
                i+= 1 
                if i > 100 :
                    i=0

                M = np.array([[m.cos(np.radians(i)),-m.sin(np.radians(i)),0],
                              [m.sin(np.radians(i)), m.cos(np.radians(i)),0],
                              [0,0,1]])

                # M = np.array([[1,0,10*i],
                #               [0,1,10*i],
                #               [0,0,1]],dtype=np.float32)

                # M = np.array([[i/100,0,0],
                #               [0,i/100,0],
                #               [0,0,1]],dtype=np.float32)

                # M = np.array([[1,i/100,0],
                #               [i/100,1,0],
                #               [0,0,1]],dtype=np.float32)
                
                h,w,_ = output_img.shape
                output_img = cv2.warpPerspective(output_img,M,(w,h))

                output_img = cv2.cvtColor(output_img,cv2.COLOR_BGR2RGB)
                proc_img_msg = cvbridge.cv2_to_imgmsg(output_img,encoding="bgr8")
                proc_compresedimg_msg = cvbridge.cv2_to_compressed_imgmsg(output_img)
                proc_img_pub.publish(proc_img_msg)
                proc_compressedimg_pub.publish(proc_compresedimg_msg)

            rate.sleep() 

    except rospy.ROSInternalException : 
        pass 