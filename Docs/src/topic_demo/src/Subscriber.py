import rospy
from topic_demo.msg import gps

import math


def callback(gps):
    distance = math.sqrt(math.pow(gps.x, 2) + math.pow(gps.y, 2))
    # print "Listener : GPS distance="+str(distance)+", state="+str(gps.state)
    rospy.loginfo("Listener: GPS: distance=%f, state=%s", distance, gps.state)


def listener():
    rospy.init_node("Subscriber_node")
    rospy.Subscriber("gps_info", gps, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
