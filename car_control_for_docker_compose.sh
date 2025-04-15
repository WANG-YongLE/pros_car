#!/bin/bash  # 指定使用的腳本解釋器為 bash
source /opt/ros/humble/setup.bash  # 加載 ROS 2 Humble 版本的環境設置
colcon build  # 使用 colcon 工具構建工作區中的包
. ./install/setup.bash  # 加載構建後的環境設置
ros2 run pros_car_py carB_keboard  # 運行 pros_car_py 包中的 carB_keboard 節點
ros2 launch rosbridge_server rosbridge_websocket_launch.xml  # 啟動 rosbridge_server 的 WebSocket 服務
# ros2 run pros_car_py carB_writer  # （被註解掉）運行 pros_car_py 包中的 carB_writer 節點
tail -f /dev/null  # 持續運行，保持容器不退出