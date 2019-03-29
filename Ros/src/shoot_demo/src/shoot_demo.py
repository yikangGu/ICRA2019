import rospy
from roborts_msgs.srv import ShootCmd, ShootCmdRequest, ShootCmdResponse

class ShootTest():
    def __init__(self):
        rospy.init_node('shoot_test_demo', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        rospy.wait_for_service("cmd_shoot")
        self.shootTest = rospy.ServiceProxy("cmd_shoot", ShootCmd)
        self.send = ShootCmdRequest()
        while input("hold on or keep down (0 or 1) ?") == 1:
            mode = input("mode : ")
            number = input("number : ")

            # self.send.mode = mode
            # self.send.number = number
            self.feedback = self.shootTest(mode, number)
            rospy.loginfo("Message from server: %s", self.feedback)

        rospy.loginfo("shut down...")
        self.shutdown()

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.shootTest.close()


if __name__ == '__main__':
    try:
        ShootTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("ARMOR DETECTION NODE test finished.")
