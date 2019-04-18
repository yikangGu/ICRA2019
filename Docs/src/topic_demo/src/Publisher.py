import rospy
from topic_demo.msg import gps


def talker():
    pub = rospy.Publisher('gps_info', gps, queue_size=10)
    rospy.init_node("publisher_node", anonymous=True)
    rate = rospy.Rate(1)

    x = 1.0
    y = 2.0
    state = "working"

    while not rospy.is_shutdown():
        rospy.loginfo("Talker: GPS: x=%f, y=%f", x, y)

        pub.publish(gps(x, y, state))
        x = 1.03 * x
        y = 1.01 * y

        rate.sleep()


def main():
    talker()


if __name__ == '__main__':
    main()
