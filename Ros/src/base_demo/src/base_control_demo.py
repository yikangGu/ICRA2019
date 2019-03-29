#!/usr/bin/env python
'''base control demo ROS Node'''
# license removed for brevity
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


def callback(Odometry):
    '''odom sub demo Callback Function'''
    global twist, cmd_vel_pub

    # twist.linear.x = 0.6
    twist.angular.z = 0.5

    rospy.loginfo(
        "\nSub : Odometry.pose.pose.orientation.z : %s\
         \nPub : Twist.angular.z                  : %f",
        Odometry.pose.pose.orientation.z, twist.angular.z)

    cmd_vel_pub.publish(twist)


if __name__ == '__main__':
    rospy.init_node('base_control_demo', anonymous=False)

    odom_sub = rospy.Subscriber('odom', Odometry, callback)
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    twist = Twist()

    rate = rospy.Rate(10)  # 10hz
    rospy.spin()
