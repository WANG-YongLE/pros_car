from enum import Enum, auto
from typing import List
import pydantic


class StringEnum(str, Enum):
    """字符串枚舉基類，用於創建字符串類型的枚舉值"""
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __eq__(self, other):
        if isinstance(other, StringEnum):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)


class DeviceDataTypeEnum(StringEnum):
    """設備數據類型枚舉，定義了所有支持的設備數據類型"""
    car_A_state = auto()  # A型車狀態
    car_A_control = auto()  # A型車控制
    car_B_state = auto()  # B型車狀態
    car_B_control = auto()  # B型車控制
    car_C_state = auto()  # C型車狀態
    car_C_state_front = auto()  # C型車前部狀態
    car_C_front_wheel = auto()  # C型車前輪
    car_C_rear_wheel = auto()  # C型車後輪
    robot_arm = auto()  # 機械臂



class DeviceData(pydantic.BaseModel):
    """設備數據基礎模型"""
    type: DeviceDataTypeEnum  # 數據類型
    data: dict  # 數據內容


class CarAState(pydantic.BaseModel):
    """A型車狀態模型"""
    vels: List[float] = []  # 速度列表
    encoders: List[int] = []  # 編碼器值列表
    direction: int  # 方向


class CarAControl(pydantic.BaseModel):
    """A型車控制模型"""
    target_vel: List[float] = []  # 目標速度列表
    direction: int = 90  # 目標方向，默認90度


class CarBState(pydantic.BaseModel):
    """B型車狀態模型"""
    vels: List[float] = []  # 速度列表
    encoders: List[int] = []  # 編碼器值列表


class CarBControl(pydantic.BaseModel):
    """B型車控制模型"""
    target_vel: List[float] = []  # 目標速度列表


class CarCState(pydantic.BaseModel):
    """C型車狀態模型"""
    vels: List[float] = []  # 速度列表
    encoders: List[int] = []  # 編碼器值列表


class CarCControl(pydantic.BaseModel):
    """C型車控制模型"""
    target_vel: List[float] = []  # 目標速度列表


class TwoWheelAndServoControlSignal(pydantic.BaseModel):
    """雙輪和舵機控制信號模型"""
    target_vel: List[float] = []  # 目標速度列表
    direction: int = None  # 目標方向


class TwoWheelAndServoState(pydantic.BaseModel):
    """雙輪和舵機狀態模型"""
    motor_count: int = 2  # 電機數量
    vels: List[float] = []  # 速度列表
    encoders: List[int] = []  # 編碼器值列表
    direction: int  # 方向


class TwoWheelControlSignal(pydantic.BaseModel):
    """雙輪控制信號模型"""
    target_vel: List[float] = []  # 目標速度列表


class TwoWheelState(pydantic.BaseModel):
    """雙輪狀態模型"""
    motor_count: int = 2  # 電機數量
    vels: List[float] = []  # 速度列表
    encoders: List[int] = []  # 編碼器值列表
