#!/usr/bin/env python3 

import rospy 
from sensor_msgs.msg import Image, CompressedImage

from cv_bridge import CvBridge

import cv2 
import numpy as np

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
    sift = cv2.SIFT_create()

    rate = rospy.Rate(10)

    # Extract KeyPoint Feature 
    ref_kp, ref_des = sift.detectAndCompute(ref_img,None)
    # ref_kp_img = cv2.drawKeypoints(np.copy(ref_img),ref_kp,None,color=(0,255,0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Matching Library 
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)

    try : 
        while not rospy.is_shutdown() : 
            if usb_img_msg is not None : 
                usb_img = cvbridge.imgmsg_to_cv2(usb_img_msg,desired_encoding="passthrough")
                output_img = np.copy(usb_img)
                source_kp, source_des = sift.detectAndCompute(usb_img,None)
                
                matches = flann.knnMatch(ref_des,source_des,k=2)
                # print(len(matches))
                matchesMask = [[0,0] for i in range(len(matches))]
                good = []
                # match_num = 0
                for i,(m,n) in enumerate(matches) : 
                    if m.distance < 0.3*n.distance : 
                        matchesMask[i]=[1,0]
                        good.append(m)
                        # match_num+=1

                draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)
                
                # print(len(good))
                if len(good) > 5 : 
                    src_pts = np.float32([ref_kp[m.queryIdx].pt for m in good]).reshape(-1,1,2)
                    dst_pts = np.float32([source_kp[m.trainIdx].pt for m in good]).reshape(-1,1,2)
                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                    # print(ref_img.shape)

                    h,w,_ = ref_img.shape
                    pts = np.float32([[0,0],
                                      [0,h-1],
                                      [w-1,h-1],
                                      [w-1,0]]).reshape(-1,1,2)
                    dst = cv2.perspectiveTransform(pts, M)
                    vis_img = cv2.polylines(usb_img,[np.int32(dst)],True,255,3, cv2.LINE_AA)
                else :
                    vis_img = usb_img

                output_img = cv2.cvtColor(vis_img,cv2.COLOR_BGR2RGB)
                proc_img_msg = cvbridge.cv2_to_imgmsg(output_img,encoding="bgr8")
                proc_compresedimg_msg = cvbridge.cv2_to_compressed_imgmsg(output_img)
                proc_img_pub.publish(proc_img_msg)
                proc_compressedimg_pub.publish(proc_compresedimg_msg)

            rate.sleep() 

    except rospy.ROSInternalException : 
        pass 