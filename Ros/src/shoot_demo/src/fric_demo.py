import rospy
from roborts_msgs.srv import FricWhl, FricWhlRequest, FricWhlResponse


class FricTest():
    def __init__(self):
        rospy.init_node('fric_whl_test_demo', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        rospy.wait_for_service("cmd_fric_wheel")
        self.fricWhlTest = rospy.ServiceProxy("cmd_fric_wheel", FricWhl)

        while input("hold on or keep down (0 or 1) ?") == 1:
            command = input("command(0-2) : ")
            if command == 1:
                rospy.loginfo("I am running the request")
            if command == 0:
                rospy.loginfo("server will pause.")
            if command == 2:
                rospy.loginfo("shut down...")
                self.shutdown()
                break

            self.command = command
            self.feedback = self.fricWhlTest(self.command)
            rospy.loginfo("Message from server: %s", self.feedback)

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.fricWhlTest.close()


if __name__ == '__main__':
    try:
        FricTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("ARMOR DETECTION NODE test finished.")
