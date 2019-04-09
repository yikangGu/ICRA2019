import rospy
import cv2
import cv_bridge
import numpy as np
from nav_msgs.msg import OccupancyGrid


class ShowMapTest():
    def __init__(self):
        rospy.init_node("show_map_test", anonymous=True)
        rospy.on_shutdown(self.shutdown)

        self.gb_map_sub = rospy.Subscriber(
            '/global_costmap/global_costmap/costmap', OccupancyGrid, callback=self.gb_map_cb, queue_size=1)

        # self.lc_map_sub = rospy.Subscriber(
        #     '/local_costmap/local_costmap/costmap', OccupancyGrid, callback=self.lc_map_cb, queue_size=1)

        while True:
            rospy.spin()
            rospy.sleep(2)

    def gb_map_cb(self, OccupancyGrid):
        rospy.loginfo("gb running")
        gb_map_w = OccupancyGrid.info.width
        gb_map_h = OccupancyGrid.info.height

        gb_map_int64 = np.array(OccupancyGrid.data).reshape(gb_map_h, gb_map_w)

        gb_map_int64[gb_map_int64 == -1] = 255
        gb_map_int64[gb_map_int64 == 99] = 255

        gb_map_uint8 = gb_map_int64.astype(np.uint8)

        cv2.imshow("gb", gb_map_uint8)
        cv2.waitKey(1)

    # def lc_map_cb(self, OccupancyGrid):
    #     rospy.loginfo("lc running")
    #     lc_map_w = OccupancyGrid.info.width
    #     lc_map_h = OccupancyGrid.info.height

    #     lc_map_int64 = np.array(OccupancyGrid.data).reshape(lc_map_h, lc_map_w)

    #     lc_map_int64[lc_map_int64 == -1] = 255
    #     lc_map_int64[lc_map_int64 == 100] = 255

    #     lc_map_uint8 = lc_map_int64.astype(np.uint8)

    #     cv2.imshow("lc", lc_map_uint8)
    #     cv2.waitKey(1)

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        ShowMapTest()
        # rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Show Map NODE test finished.")
