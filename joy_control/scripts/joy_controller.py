#!/usr/bin/env python3 

import rospy 
from sensor_msgs.msg import Joy 
from std_msgs.msg import Int16

recived_joy = None 

servo_position = 0

def joy_callback(msg) :
    global recived_joy
    recived_joy = msg

if __name__ == "__main__" : 
    rospy.init_node("joy_controller")
    rospy.loginfo(":: Joy Controller is Already ::")
    joy_sub = rospy.Subscriber("gui/output/joy",Joy,joy_callback)
    left_servo_pub = rospy.Publisher("a_value",Int16,queue_size=10)

    rate = rospy.Rate(10)

    try : 
        while not rospy.is_shutdown() : 
            if recived_joy is not None :
                # print(recived_joy)
                if recived_joy.buttons[12] == 1 : 
                    servo_position = servo_position + 1 

                elif recived_joy.buttons[13] == 1 : 
                    servo_position = servo_position - 1 

                if servo_position >= 180 :
                    servo_position = 180 
                elif servo_position <= 0 : 
                    servo_position = 0 

                left_servo_pub.publish(servo_position)

                # print(servo_position)

            rate.sleep()

    except rospy.ROSInterruptException : 
        pass 