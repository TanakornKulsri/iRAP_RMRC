#!/usr/bin/env python3 

import rospy 
from sensor_msgs.msg import Image, CompressedImage

from cv_bridge import CvBridge

import cv2 
import numpy as np

usb_img_msg = None 
usb_compressedimg_msg = None 

previous_img = None 
def usb_img_callback(msg) : 
    global usb_img_msg
    usb_img_msg = msg  

def usb_compressedimg_callback(msg) :
    global usb_compressedimg_msg  
    usb_compressedimg_msg = msg 

def morphology(img,ksize=5) : 
    kernel = np.ones((ksize,ksize),dtype=np.uint8)
    dilate_img = cv2.dilate(img,kernel,iterations=1)
    erode_img = cv2.erode(dilate_img,kernel,iterations=1)
    return erode_img

def get_frame_differencing(img,pimg,ksize=9) : 
    diff_img = np.array(img,dtype=np.int32)-np.array(pimg,dtype=np.int32)
    diff_img = np.where(diff_img<0,0,diff_img).astype(np.uint8)
    diff_img = cv2.medianBlur(diff_img, 3)
    motion_mask = cv2.adaptiveThreshold(diff_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 3)
    motion_mask = morphology(motion_mask,ksize=ksize)

    return motion_mask 

def get_opticalflow(img,pimg) : 
    flow = cv2.calcOpticalFlowFarneback(img,pimg,None,
                                        pyr_scale=0.75,
                                        levels=3,
                                        winsize=5,
                                        iterations=3,
                                        poly_n=10,
                                        poly_sigma=1.2,
                                        flags=0)
    flow_viz_img = np.zeros((flow.shape[0],flow[1],3),dtype=np.uint8)
    flow_viz_img[:,:,1] = 255
    mag, ang = cv2.cartToPolar(flow[:,:,0],flow[:,:,1])
    flow_viz_img[:,:,0] = ang*180/np.pi/2
    flow_viz_img[:,:,1] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    
    return cv2.cvtColor(flow_viz_img,cv2.COLOR_HSV2RGB) 

def get_contour_detections(mask,thresh=400) : 
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
    detection = []
    for c in contours : 
        x,y,w,h = cv2.boundingRect(c)
        area = w*h 
        if area > thresh : 
            detection.append([x,y,x+w,y+h,area])
    
    return np.array(detection)

def draw_boxes(img,boxes) : 
    for b in boxes : 
        img = cv2.rectangle(img,(b[0],b[1]),(b[2],b[3]),(255,0,0),2)
    
    return img

if __name__ == "__main__" : 
    rospy.init_node("cvbridge_example")
    rospy.loginfo(":: Cv Bridge Example is Already :")

    usb_img_sub = rospy.Subscriber("/usb_cam/image_raw",Image,usb_img_callback)
    usb_compressedimg_sub = rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage,usb_compressedimg_callback)
    proc_img_pub = rospy.Publisher("proc_image",Image,queue_size=10)
    proc_compressedimg_pub = rospy.Publisher("proc_image/compressed",CompressedImage,queue_size=10)

    cvbridge = CvBridge()
    rate = rospy.Rate(10)
    
    try : 
        while not rospy.is_shutdown() : 
            if usb_img_msg is not None : 
                usb_img = cvbridge.imgmsg_to_cv2(usb_img_msg,desired_encoding="passthrough")
                output_img = np.copy(usb_img)
                usb_img = cv2.cvtColor(usb_img,cv2.COLOR_BGR2GRAY)
                if previous_img is not None : 
                    motion_mask = get_frame_differencing(usb_img,previous_img,ksize=9)
                    object_boxes = get_contour_detections(motion_mask,thresh=5000)
                    if len(object_boxes) > 0 :  
                        output_img = draw_boxes(output_img,object_boxes)

                output_img = cv2.cvtColor(output_img,cv2.COLOR_BGR2RGB)
                proc_img_msg = cvbridge.cv2_to_imgmsg(output_img,encoding="bgr8")
                proc_compresedimg_msg = cvbridge.cv2_to_compressed_imgmsg(output_img)
                proc_img_pub.publish(proc_img_msg)
                proc_compressedimg_pub.publish(proc_compresedimg_msg)

                previous_img = usb_img

            rate.sleep() 
    
    except rospy.ROSInterruptException : 
        pass 
        # cv2.destroyAllWindows() 