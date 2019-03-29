#!/usr/bin/env python
import rospy
import cv2
import cv_bridge
import numpy as np
from std_msgs.msg import Bool
from sensor_msgs.msg import Image

def isDetect(cam):
    ret, frame = cam.read()
    if not ret:
        return False
    img_pub.publish(bridge.cv2_to_imgmsg(frame, encoding="bgr8"))

    frame = cv2.GaussianBlur(frame, (35, 35), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([170, 50, 150])
    upper_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('red', red_mask)

    red_count = cv2.countNonZero(red_mask)
    # print 'red_count:', red_count
    return red_count > 5000


if __name__ == '__main__':
    bridge = cv_bridge.CvBridge()
    img_pub = rospy.Publisher("back_camera/image_raw", Image, queue_size=1)
    
    rospy.init_node('detection_node')
    detection_flag_pub = rospy.Publisher("detect_flag", Bool, queue_size=1)
    
    cam = cv2.VideoCapture(1)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if isDetect(cam):
            detection_flag_pub.publish(True)
        else:
            detection_flag_pub.publish(False)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rate.sleep()

    cam.release()
    cv2.destroyAllWindows()
