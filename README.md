# ICRA 2019

For the 2019 ICRA AI Challenge

## 环境

| name    | version    | comment               |
|:--------|:-----------|:----------------------|
| Ubuntu  | 16.04 LTS  |                       |
| ROS     | kinetic    |                       |
| RoboRTS | f43ac5f... | isn't the latest ver. |

## 设置

前提先安装 ros-kinetic-full-desktop 版本, 而后依次安装以下 RoboRTS 依赖包.

```bash
sudo apt-get install -y ros-kinetic-opencv3             \
                        ros-kinetic-cv-bridge           \
                        ros-kinetic-image-transport     \
                        ros-kinetic-stage-ros           \
                        ros-kinetic-map-server          \
                        ros-kinetic-laser-geometry      \
                        ros-kinetic-interactive-markers \
                        ros-kinetic-tf                  \
                        ros-kinetic-pcl-*               \
                        ros-kinetic-libg2o              \
                        ros-kinetic-rplidar-ros         \
                        ros-kinetic-rviz                \
                        protobuf-compiler               \
                        libprotobuf-dev                 \
                        libsuitesparse-dev              \
                        libgoogle-glog-dev              \
```

当所有包正常安装完毕后, 下载本仓库后进入 Ros/ 下目录, 并运行 catkin_make 命令

```bash
$ git clone https://github.com/yikangGu/ICRA2019.git && cd ICRA2019/Ros
$ catkin_make
$ source devel/setup.bash
```

## 教程/说明

ROS/RoboRTS 入门简易教程 : [Tutorial for beginner](https://github.com/yikangGu/ICRA2019/blob/master/Docs/README.md)

demo 都是自己写的文件, 可以参考并DIY, 需要学习基本的 ros node/ server/ action 的写法, demo 基本都在引用官方写的 node/ server/ action 而做处理而已.

## 简单例子

环境配置完全后, 依次输入以下命令

```bash
$ roslaunch roborts_bringup roborts_stage.launch
$ roscd nav_demo/src
$ python nav_test.py
```

这里运行 nav_test 后, 可以输入 x, y = 7.5, 4.5 看看. 如果想设置定点巡航, 可以试着自行修改 nav_test.py 来实现. 希望此次之后, 能对 ros 的认识愈发深入和对 ros 的热情愈发浓郁.

同时也可以另外打开一个 terminal, 输入 rosrun rqt_graph rqt_graph 来查看 node/ server/ action 直接互相引用的情况等等.

类似的 ros 自带命令有

```bash
rosrun rqt_tree rqt_tree 
rosrun rqt_...

rostopic list
rostopic ...

rosservice list
rosservice ...

rosnode list
rosnode ...
```
