# ICRA 2019

For the 2019 ICRA AI Challenge

- [ICRA 2019](#icra-2019)
  - [环境](#%E7%8E%AF%E5%A2%83)
  - [设置](#%E8%AE%BE%E7%BD%AE)
  - [教程/说明](#%E6%95%99%E7%A8%8B%E8%AF%B4%E6%98%8E)
  - [简单例子](#%E7%AE%80%E5%8D%95%E4%BE%8B%E5%AD%90)
  - [模拟器（开发中）](#%E6%A8%A1%E6%8B%9F%E5%99%A8%E5%BC%80%E5%8F%91%E4%B8%AD)

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

## 模拟器（开发中）

在 src/map_demo 下是 ICRA 2019 in ROS Simulator 的雏形 Demo.
基于 ROS 环境建立的 ICRA 2019 模拟器应该是较接近现实的.

<div align="center">
  <img src=Docs/imgs/1.gif width="720px"/>
</div>

其中 gl 为 Simulator 的场地信息, 提取自 Global Planner Map, 用 OpenCV 进行处理, 可以从雷达的信息获知与原始地图相冲突的奇异点, 从而的得到潜在敌人的信息.

同时, 通过 ROS 自洽的环境, 在 tf 层上, 此模拟器都可以从中获取信息.
再通过 Pygame 或者 其他界面环境封装, 以达到基于 ROS 的 ICRA 2019 模拟器.
再交由 RL 算法进行训练, 训练结果理论上是贴合现实环境的.
