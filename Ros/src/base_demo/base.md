# roborts_base 的简易教程

Node 是组成 ROS 的基本运行单位(可以看做一个应用程序, 其包含着各种发送接收的功能), 一个 Node 可以开启多个 Topic, Service 和 Action (TSA), 可以说 Node 又是由这三大基本运行单位所构成. 

所以我们在编写程序的时候就会新建一个 Node , 然后创建 TSA , 然后定义新建的 TSA 与其他 TSA 之间的通信信息, 运行逻辑...等等

## roborts_base_node

在官方的 [Roborts Tutorial](https://robomaster.github.io/RoboRTS-Tutorial/#/) 里介绍到 roborts_base 提供了 ROS 接口，接收底层嵌入式控制板发送的数据并控制其完成对机器人的模式切换和运动控制。

所以我们可以编写一个简单的 Node 来与 roborts_base 下的各种 TSA 来通信, 以达到运动控制的目的.

在 RoboRTS / roborts_base / 下我们可以发现 **roborts_base_node.cpp** 文件.

分析可以知道, 它创建了名为 "roborts_base_node" 的 Node, 并从 **roborts_base_config.h** 文件引用了某些参数 (这里我们可以忽视), 并初始化了 Chassis 和 Gimbal 这两个类 (ROS 的源文件喜欢用类来封装, 好处多多, TODO:介绍 Node 用类实现), 然后是定义了 ROS 在运行时, 这个 Node 永不退出, 并且随着 1000 ms 后刷新一遍.

