
import rospy
import actionlib
from actionlib_msgs.msg import *
from roborts_msgs.msg import ArmorDetectionAction, ArmorDetectionGoal, ArmorDetectionActionFeedback

class DetectionClientTest():
    def __init__(self):
        rospy.init_node('detection_client_test', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        self.ac = actionlib.SimpleActionClient(
            "armor_detection_node_action", ArmorDetectionAction
        )
        self.ac.wait_for_server(rospy.Duration(60))

        while input("hold on or keep down (0 or 1) ?") == 1:
            command = input("command(1-3) : ")
            if command == 1:
                rospy.loginfo("I am running the request")
            if command == 2:
                rospy.loginfo("Action server will pause.")
            if command == 3:
                rospy.loginfo("I am cancelling the request")
                self.shutdown()
                break

            self.ac.send_goal(ArmorDetectionGoal(command),
                              self.AcDoneCb,
                              self.AcActiveCb,
                              self.AcFeedbackCb)

    def AcDoneCb(self, state, result):
        print "\nstate : " + str(state) + " result : " + str(result)

    def AcActiveCb(self):
        print "\nDetection Action is active"

    def AcFeedbackCb(self, feedback):
        print "\nfeedback : " + str(feedback.detected)
        if (feedback.error_code == 1):
            print feedback.error_msg

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.ac.cancel_goal()


def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])


if __name__ == '__main__':
    try:
        DetectionClientTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("ARMOR DETECTION NODE test finished.")
