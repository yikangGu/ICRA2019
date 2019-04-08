# roborts_base 的简易教程

- [roborts_base 的简易教程](#robortsbase-%E7%9A%84%E7%AE%80%E6%98%93%E6%95%99%E7%A8%8B)
  - [roborts_base_node](#robortsbasenode)
  - [Chassis 类](#chassis-%E7%B1%BB)
    - [ChassisInfoCallback 回调函数](#chassisinfocallback-%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0)
  - [Gimbal 类](#gimbal-%E7%B1%BB)
    - [GimbalInfoCallback 回调函数](#gimbalinfocallback-%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0)

Node 是组成 ROS 的基本运行单位(可以看做一个应用程序, 其包含着各种发送接收的功能), 一个 Node 可以开启多个 Topic, Service 和 Action (TSA), 可以说 Node 又是由这三大基本运行单位所构成.

所以我们在编写程序的时候就会新建一个 Node , 然后创建 TSA , 然后定义新建的 TSA 与其他 TSA 之间的通信信息, 运行逻辑...等等

## roborts_base_node

在官方的 [Roborts Tutorial](https://robomaster.github.io/RoboRTS-Tutorial/#/) 里介绍到 roborts_base 提供了 ROS 接口，接收底层嵌入式控制板发送的数据并控制其完成对机器人的模式切换和运动控制。

所以我们可以编写一个简单的 Node 来与 roborts_base 下的各种 TSA 来通信, 以达到运动控制的目的.

在 RoboRTS/roborts_base/ 下我们可以发现 [roborts_base_node.cpp](https://github.com/yikangGu/ICRA2019/blob/master/Ros/src/RoboRTS/roborts_base/roborts_base_node.cpp) 文件.

分析可以知道, 它创建了名为 "roborts_base_node" 的 Node.

```cpp
  ros::init(argc, argv, "roborts_base_node");
```

并从 [roborts_base_config.h](https://github.com/yikangGu/ICRA2019/blob/master/Ros/src/RoboRTS/roborts_base/roborts_base_config.h) 文件引用了某些参数 (这里我们可以忽视).

```cpp
  roborts_base::Config config;
  config.GetParam(&nh);
  auto handle = std::make_shared<roborts_sdk::Handle>(config.serial_port);
```

并初始化了 Chassis 和 Gimbal 这两个类 (ROS 的源文件喜欢用类来封装, 好处多多, TODO:介绍 Node 用类实现).

```cpp
  roborts_base::Chassis chassis(handle);
  roborts_base::Gimbal gimbal(handle);
```

然后是定义了 ROS 在运行时, 这个 Node 永不退出, 并且随着 1000 ms 后刷新一遍.

```cpp
  while(ros::ok())
  {
    handle->Spin();
    ros::spinOnce();
    usleep(1000);
  }
```

明显, chassis 和 gimbal 这两个类才是我们需要详细了解的东西. 接下来我们就直接看定义它们的源文件吧.

```cpp
#include "gimbal/gimbal.h"
#include "chassis/chassis.h"
#include "roborts_base_config.h"
```

通过引用情况来看, 可知它们分别在 roborts_base_node.cpp 目录下的 chassis/ 和 gimbal/ 文件夹下.

---

## Chassis 类

在 .../roborts_base/chassis/ 下, 我们可以发现 [chassis.cpp](https://github.com/yikangGu/ICRA2019/blob/master/Ros/src/RoboRTS/roborts_base/chassis.cpp) 源文件, 也就是定义 chassis 类的文件.

首先, 可以看见声明了一个名为 "roborts_base" 的命名空间 (namespace), 里面是 chassis类 的定义, 可以想象 gimbal类 应该也属于这个命名空间.

```cpp
namespace roborts_base{
Chassis::Chassis(std::shared_ptr<roborts_sdk::Handle> handle):
    handle_(handle){
  SDK_Init();
  ROS_Init();
}
  ...
}
```

这里表明在实例化(初始化) chassis类 时, 同时会实例化(初始化) SDK_Init() 和 ROS_Init() 这两个函数.

```cpp
void Chassis::SDK_Init(){
  handle_->CreateSubscriber<roborts_sdk::cmd_chassis_info>(CHASSIS_CMD_SET, CMD_PUSH_CHASSIS_INFO,
                                                           CHASSIS_ADDRESS, MANIFOLD2_ADDRESS,
                                                           std::bind(&Chassis::ChassisInfoCallback, this, std::placeholders::_1));
  handle_->CreateSubscriber<roborts_sdk::cmd_uwb_info>(..., ..., this, std::placeholders::_1));

  chassis_speed_pub_ = handle_->CreatePublisher<roborts_sdk::cmd_chassis_speed>(...);
  chassis_spd_acc_pub_ = handle_->CreatePublisher<roborts_sdk::cmd_chassis_spd_acc>(...);
}
```

这里我们注意 handle_ -> CreateSubscriber 和 handle_ -> CreatePublisher 这两个函数, 明显它们是 Topic 的封装体, 也就是 topic 的核心没有变, 但是被 handle 这个类给封装起来了.

| 分解                                                                       | 说明     |
| -------------------------------------------------------------------------- | -------- |
| handle_ -> CreateSubscriber                                                | 指针函数 |
| <roborts_sdk::cmd_chassis_info>                                            | 消息类型 |
| CHASSIS_CMD_SET, CMD_PUSH_CHASSIS_INFO, CHASSIS_ADDRESS, MANIFOLD2_ADDRESS | 通信地址 |
| ChassisInfoCallback                                                        | 回调函数 |

那么这个部分在做什么呢? [Roborts Tutorial](https://robomaster.github.io/RoboRTS-Tutorial/#/) 曾经有介绍到 roborts_base 接收底层嵌入式控制板发送的数据. 那么可以知道, 这个 handle 其实是个桥梁, 一端连接着底层嵌入式控制板, 另一端连接着 ROS 接口. 这里便是桥梁的尾端, 那么 ROS_Init() 应该就是桥梁的首端了.

```cpp
void Chassis::ROS_Init(){
  //ros publisher
  ros_odom_pub_ = ros_nh_.advertise<nav_msgs::Odometry>("odom", 30);
  ros_uwb_pub_ = ros_nh_.advertise<geometry_msgs::PoseStamped>("uwb", 30);
  //ros subscriber
  ros_sub_cmd_chassis_vel_ = ros_nh_.subscribe("cmd_vel", 1, &Chassis::ChassisSpeedCtrlCallback, this);
  ros_sub_cmd_chassis_vel_acc_ = ros_nh_.subscribe("cmd_vel_acc", 1, &Chassis::ChassisSpeedAccCtrlCallback, this);
```

将所建立的 TSA 及其相关信息建立成表格, 如下显示.

| TSA类型    | 名称        | 消息类型                   | 回调函数                    |
| ---------- | ----------- | -------------------------- | --------------------------- |
| Publisher  | odom        | nav_msgs::Odometry         |                             |
| Publisher  | uwb         | geometry_msgs::PoseStamped |                             |
| Subscriber | cmd_vel     |                            | ChassisSpeedCtrlCallback    |
| Subscriber | cmd_vel_acc |                            | ChassisSpeedAccCtrlCallback |

显然, 可以看出 ROS_Init() 定义了两个Publisher "odom" 和 "uwb", 两个Subscriber "cmd_vel" 和 "cmd_vel_acc".

接下来是定义 odom 的 tf tree 关系. odom_ 的声明可以在其头文件 ([chassis.h](https://github.com/yikangGu/ICRA2019/blob/master/Ros/src/RoboRTS/roborts_base/chassis.h)) 看到.

```cpp
  //ros_message_init
  odom_.header.frame_id = "odom";
  odom_.child_frame_id = "base_link";

  odom_tf_.header.frame_id = "odom";
  odom_tf_.child_frame_id = "base_link";

  uwb_data_.header.frame_id = "uwb";
}
```

可以看出 odom_tf_ 定义了从 base_link -> odom 的变换, 消息变量 odom_ 和 uwb_data_ 分别定义了其本身在 /tf 里面被代表的 frame_id 或其 child_frame_id.
变换处理见 ChassisInfoCallback 回调函数.

---

### ChassisInfoCallback 回调函数

```cpp
void Chassis::ChassisInfoCallback(const std::shared_ptr<roborts_sdk::cmd_chassis_info> chassis_info){

  ros::Time current_time = ros::Time::now();
  odom_.header.stamp = current_time;
  odom_.pose.pose.position.x = chassis_info->position_x_mm/1000.;
  odom_.pose.pose.position.y = chassis_info->position_y_mm/1000.;
  odom_.pose.pose.position.z = 0.0;
  geometry_msgs::Quaternion q = tf::createQuaternionMsgFromYaw(chassis_info->gyro_angle / 1800.0 * M_PI);
  odom_.pose.pose.orientation = q;
  odom_.twist.twist.linear.x = chassis_info->v_x_mm / 1000.0;
  odom_.twist.twist.linear.y = chassis_info->v_y_mm / 1000.0;
  odom_.twist.twist.angular.z = chassis_info->gyro_rate / 1800.0 * M_PI;
  ros_odom_pub_.publish(odom_);

  odom_tf_.header.stamp = current_time;
  odom_tf_.transform.translation.x = chassis_info->position_x_mm/1000.;
  odom_tf_.transform.translation.y = chassis_info->position_y_mm/1000.;

  odom_tf_.transform.translation.z = 0.0;
  odom_tf_.transform.rotation = q;
  tf_broadcaster_.sendTransform(odom_tf_);

}
```

---

## Gimbal 类

同样, 在 .../roborts_base/gimbal/ 下, 我们可以发现 [gimbal.cpp](https://github.com/yikangGu/ICRA2019/blob/master/Ros/src/RoboRTS/roborts_base/chassis.cpp) 源文件, 也就是定义 gimbal 类的文件.

直接看 SDK_Init() 和 ROS_Init() 这两个函数.

```cpp
void Gimbal::SDK_Init(){
  handle_->CreateSubscriber<roborts_sdk::cmd_gimbal_info>(GIMBAL_CMD_SET, CMD_PUSH_GIMBAL_INFO,
                                                          GIMBAL_ADDRESS, BROADCAST_ADDRESS,
                                                          std::bind(&Gimbal::GimbalInfoCallback, this, std::placeholders::_1));

  gimbal_angle_pub_ = handle_->CreatePublisher<roborts_sdk::cmd_gimbal_angle>(...);
  gimbal_mode_pub_= handle_->CreatePublisher<roborts_sdk::gimbal_mode_e>(...);
  fric_wheel_pub_= handle_->CreatePublisher<roborts_sdk::cmd_fric_wheel_speed>(...);
  gimbal_shoot_pub_= handle_->CreatePublisher<roborts_sdk::cmd_shoot_info>(...);

}
```

SDK_Init() 定义表明, gimbal 的 handle 嵌入式端建立了四个 Publisher 和一个 Subscriber, 是获取云台上电机的相关信息, 以及向下位机发送命令.

```cpp
void Gimbal::ROS_Init(){

  //ros subscriber
  ros_sub_cmd_gimbal_angle_ = ros_nh_.subscribe("cmd_gimbal_angle", 1, &Gimbal::GimbalAngleCtrlCallback, this);

  //ros service
  ros_gimbal_mode_srv_ = ros_nh_.advertiseService("set_gimbal_mode", &Gimbal::SetGimbalModeService, this);
  ros_ctrl_fric_wheel_srv_ = ros_nh_.advertiseService("cmd_fric_wheel", &Gimbal::CtrlFricWheelService, this);
  ros_ctrl_shoot_srv_ = ros_nh_.advertiseService("cmd_shoot", &Gimbal::CtrlShootService, this);
  //ros_message_init
  gimbal_tf_.header.frame_id = "base_link";
  gimbal_tf_.child_frame_id = "gimbal";

}
```

ROS_Init() 定义表明, gimbal 的 ROS 端建立了一个 Subscriber 和三个 Service.
并建立了 gimbal_tf_ 定义从 base_link -> gimbal 的变换.
变换处理见 GimbalInfoCallback 回调函数.

将所建立的 TSA 及其相关信息建立成表格, 如下显示.

| TSA类型    | 名称             | 消息类型 | 回调函数                |
| ---------- | ---------------- | -------- | ----------------------- |
| Subscriber | cmd_gimbal_angle |          | GimbalAngleCtrlCallback |
| Service    | set_gimbal_mode  |          | SetGimbalModeService    |
| Service    | cmd_fric_wheel   |          | CtrlFricWheelService    |
| Service    | cmd_shoot        |          | CtrlShootService        |

---

### GimbalInfoCallback 回调函数

```cpp
void Gimbal::GimbalInfoCallback(const std::shared_ptr<roborts_sdk::cmd_gimbal_info> gimbal_info){

  ros::Time current_time = ros::Time::now();
  geometry_msgs::Quaternion q = tf::createQuaternionMsgFromRollPitchYaw(0.0,
                                                                        gimbal_info->pitch_ecd_angle / 1800.0 * M_PI,
                                                                        gimbal_info->yaw_ecd_angle / 1800.0 * M_PI);
  gimbal_tf_.header.stamp = current_time;
  gimbal_tf_.transform.rotation = q;
  gimbal_tf_.transform.translation.x = 0;
  gimbal_tf_.transform.translation.y = 0;
  gimbal_tf_.transform.translation.z = 0.15;
  tf_broadcaster_.sendTransform(gimbal_tf_);

}
```
