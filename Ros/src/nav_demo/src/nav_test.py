
import rospy
import actionlib
import tf.transformations
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Point, Quaternion, Twist
from nav_msgs.msg import Path
from roborts_msgs.msg import GlobalPlannerAction, GlobalPlannerGoal, GlobalPlannerActionFeedback
from roborts_msgs.msg import LocalPlannerAction, LocalPlannerGoal, LocalPlannerActionFeedback

from random import sample, uniform
from math import pow, sqrt


class NavTest():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=True)
        rospy.on_shutdown(self.shutdown)
        self.rest_time = rospy.get_param("~rest_time", 10)
        self.fake_test = rospy.get_param("~fake_test", False)

        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED',
                       'SUCCEEDED', 'ABORTED', 'REJECTED',
                       'PREEMPTING', 'RECALLING', 'RECALLED',
                       'LOST']

        rate = rospy.Rate(10)  # 10hz

        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher(
            'cmd_vel', Twist, queue_size=5
        )

        self.move_base_goal_pub = rospy.Publisher(
            'move_base_simple/goal', PoseStamped, queue_size=1
        )

        self.move_base_path_sub = rospy.Subscriber(
            'global_planner_node/path', Path, self.PathCallBack
        )

        self.lc_planner_node_action = actionlib.SimpleActionClient(
            "local_planner_node_action", LocalPlannerAction
        )
        self.lc_planner_node_action.wait_for_server(rospy.Duration(60))

        # Variables to keep track of success rate, running time,
        # and distance traveled
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped,
                         self.update_initial_pose)
        while initial_pose.header.stamp == "":
            rospy.sleep(1)

        distance_traveled = 0
        start_time = rospy.Time.now()
        running_time = 0

        rospy.loginfo("Starting navigation test")
        while input("hold on or keep down (0 or 1) ?") == 1:
            x = input("input pose x : ")
            y = input("input pose y : ")
            theta = uniform(0, 360)

            goalPoseStamped = PoseStamped()
            goalPoseStamped.header.stamp = rospy.Time.now()
            goalPoseStamped.header.frame_id = "map"
            goalPoseStamped.pose.position.x = x
            goalPoseStamped.pose.position.y = y
            goalPoseStamped.pose.position.z = 0

            quaternion = tf.transformations.quaternion_from_euler(0, 0, theta)
            goalPoseStamped.pose.orientation.x = quaternion[0]
            goalPoseStamped.pose.orientation.y = quaternion[1]
            goalPoseStamped.pose.orientation.z = quaternion[2]
            goalPoseStamped.pose.orientation.w = quaternion[3]

            # while not rospy.is_shutdown():
            if initial_pose.header.stamp == "":
                distance = sqrt(pow(goalPoseStamped.pose.position.x -
                                    last_location.pose.position.x, 2) +
                                pow(goalPoseStamped.pose.position.y -
                                    last_location.pose.position.y, 2))
            else:
                rospy.loginfo("Updating current pose.")
                distance = sqrt(pow(goalPoseStamped.pose.position.x -
                                    initial_pose.pose.pose.position.x, 2) +
                                pow(goalPoseStamped.pose.position.y -
                                    initial_pose.pose.pose.position.y, 2))
                initial_pose.header.stamp = ""

            last_location = goalPoseStamped
            rospy.loginfo("\nGoing to: x : "+str(goalPoseStamped.pose.position.x)+"\n"
                          "          y : "+str(goalPoseStamped.pose.position.y))

            self.move_base_goal_pub.publish(goalPoseStamped)

            running_time = rospy.Time.now() - start_time
            running_time = running_time.secs / 60.0
            rospy.loginfo("\nRunning time: "+str(trunc(running_time, 1))+"\n"
                          "\nmin Distance: "+str(trunc(distance_traveled, 1))+"m")
            
            print(" request suppor")
            rospy.sleep(self.rest_time)

        print "is shutting down now"
        rospy.is_shutdown()
        # rospy.spin()

    def PathCallBack(self, Path):
        self.goal = LocalPlannerGoal(Path)
        self.lc_planner_node_action.send_goal(
            self.goal, self.PathDoneCallBack, self.PathActiveCallBack, self.PathFeedBackCallBack)

    def PathDoneCallBack(self, state, result):
        print "\nstate : " + str(state) + " result : " + str(result)

    def PathActiveCallBack(self):
        print "\nLC path is active"

    def PathFeedBackCallBack(self, feedback):
        if (feedback.error_code == 1):
            print "\nfeedback : " + str(feedback.error_msg)

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.lc_planner_node_action.cancel_goal()
        self.gb_planner_node_action.cancel_goal()
        self.cmd_vel_pub.publish(Twist())


def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])


if __name__ == '__main__':
    try:
        NavTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")
