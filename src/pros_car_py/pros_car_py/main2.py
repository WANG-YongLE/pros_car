import urwid
import os
import threading
import rclpy
import time
import io
import sys
from pros_car_py.joint_config import JOINT_UPDATES_POSITIVE, JOINT_UPDATES_NEGATIVE
from pros_car_py.car_controller import CarController
from pros_car_py.arm_controller import ArmController
from pros_car_py.data_processor import DataProcessor
from pros_car_py.nav_processing import Nav2Processing
from pros_car_py.ros_communicator import RosCommunicator
from pros_car_py.crane_controller import CraneController
from pros_car_py.custom_control import CustomControl
from pros_car_py.ik_solver import PybulletRobotController
from pros_car_py.mode_app import ModeApp


def init_ros_node():
    rclpy.init()  # 初始化 ROS2
    node = RosCommunicator() # 建立自定義的 ROS node（負責訂閱/發布/服務等）
    thread = threading.Thread(target=rclpy.spin, args=(node,)) # 用 thread 跑 rclpy.spin
    thread.start()
    return node, thread
"""
初始化 ROS2 環境

建立你的 ROS 節點（RosCommunicator）

用一條獨立的 thread 執行 ROS 通訊（非同步 spin）
"""
def main():
    ros_communicator, ros_thread = init_ros_node()#這行程式碼的作用是呼叫 init_ros_node() 函式，並將它回傳的兩個值分別指定給變數 ros_communicator 和 ros_thread
    data_processor = DataProcessor(ros_communicator)
    nav2_processing = Nav2Processing(ros_communicator, data_processor)
    ik_solver = PybulletRobotController(end_eff_index=5)
    car_controller = CarController(ros_communicator, nav2_processing)
    arm_controller = ArmController(
        ros_communicator, data_processor, ik_solver, num_joints=5
    )
    crane_controller = CraneController(
        ros_communicator, data_processor, ik_solver, num_joints=7
    )
    custom_control = CustomControl(car_controller, arm_controller)
    app = ModeApp(car_controller, arm_controller, custom_control, crane_controller)

    try:
        app.main()
    finally:
        rclpy.shutdown() # 結束 ROS2
        ros_thread.join()# 等待 ros spin thread 結束


if __name__ == "__main__":
    main()
