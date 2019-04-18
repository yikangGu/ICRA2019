# ROS 的简易教程 (Python 版本)

- [ROS 的简易教程 (Python 版本)](#ros-%E7%9A%84%E7%AE%80%E6%98%93%E6%95%99%E7%A8%8B-python-%E7%89%88%E6%9C%AC)
  - [Publisher 的一般写法](#publisher-%E7%9A%84%E4%B8%80%E8%88%AC%E5%86%99%E6%B3%95)
  - [Subscriber 的一般写法](#subscriber-%E7%9A%84%E4%B8%80%E8%88%AC%E5%86%99%E6%B3%95)

## Publisher 的一般写法

假设已经有一种名为 topic_demo/gps 的消息类型, 其结构是这样:

```cpp
float32 x
float32 y
string state
```

我们也可以通过在终端来查看消息类型的结构.

```bash
user@ubuntu ~> rostopic list
/gps_info
user@ubuntu ~> rostopic info /gps_info
Type: topic_demo/gps

Publishers: 
* /publisher_node (http://user.local:44855/)

Subscribers: None


user@ubuntu ~> rosmsg show topic_demo/gps
float32 x
float32 y
string state
```

消息结构具有顺序性, 这说明我们在写 Publisher 的时候, 要给定的3个参数, 且要一一对应, 类型也要满足.

```python
import rospy
from topic_demo.msg import gps
```

引用 ros 库和消息类型库. 想发布怎么样的消息类型, 我们就引用什么库, 如我们想发有关 /odom 的消息, 那我们理应 from nav_msgs.msg import Odometry

from topic_demo.msg import gps 由三部分组成, topic_demo 是 ros 包名, msg 是指在这个 ros 包下(里面)定义的那些消息, gps 是那些消息中的一个消息结构体.

```python
def talker():
    rospy.init_node("publisher_node", anonymous=True)
    pub = rospy.Publisher('gps_info', gps, queue_size=10)
    rate = rospy.Rate(1)
```

首先定义一个 node, 名为 "publisher_node", anonymous=true 的时候, Publisher 的名字在 rostopic info 里显示的是带时间戳的 (e.g. /publisher_node_4439_1555572029271).

相反, false 的时候, 在 rostopic info 里显示是没有时间戳 (e.g. /publisher_node).

然后构建一个 Publisher, 名为 "gps_info", 消息类型为 gps, 消息长度为 10.

```python
    x = 1.0
    y = 2.0
    state = "working"

    while not rospy.is_shutdown():
         ...
        x = 1.03 * x
        y = 1.01 * y
```

定义 x, y, state 分别为多少, 然后在 while 里如何处理.

```python
        rospy.loginfo("Talker: GPS: x=%f, y=%f", x, y)
        print("Talker: GPS: x=", x, ", y=", y)
```

rospy.loginfo 可以看作 print, 只不过 rospy.loginfo 添加了时间戳.

```python
        pub.publish(gps(x, y, state))
        rospy.sleep()
```

将3个参数放入 gps(x, y, state) 里, 然后用 pub.publish 发布出去.

```python
if __name__ == '__main__':
    talker()
```

完整的代码在 [Publisher.py](https://github.com/yikangGu/ICRA2019/blob/master/Docs/src/Publisher.py)

---

## Subscriber 的一般写法

```python
import rospy
from topic_demo.msg import gps

import math
```

类似的, 引用必要的库, 引用相应的消息类型库.

``` python
def listener():
    rospy.init_node("Subscriber_node")
    rospy.Subscriber("gps_info", gps, callback)
    rospy.spin()
```

定义一个 node, 名为 "Subscriber_node".
构建一个 Subscriber 去订阅名为 "gps_info" 的 Publisher 的消息, 消息类型和 Publisher 发布出来的一致.

callback 是一个函数, 指在每收到一次 Publisher 的消息, 做什么处理.
rospy.spin() 指永不退出, 除非 ros master 退出.

```python
def callback(gps):
    distance = math.sqrt(math.pow(gps.x, 2) + math.pow(gps.y, 2))
    # print "Listener : GPS distance="+str(distance)+", state="+str(gps.state)
    rospy.loginfo("Listener: GPS: distance=%f, state=%s", distance, gps.state)

if __name__ == '__main__':
    listener()
```

说明, 每收到 x, y, 便会计算它们的欧基里德距离, 然后连同 state 一起打印出来.

完整的代码在 [Subscriber.py](https://github.com/yikangGu/ICRA2019/blob/master/Docs/src/Subscriber.py)
