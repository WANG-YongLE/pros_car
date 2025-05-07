# 2025/5/7更新
在 Docker 環境中執行時，`p.connect(p.GUI)` 會因無法連接到 X Server 而失敗 (錯誤訊息: "cannot connect to X server")。 此修改將 GUI 模式下的連線方式改為 `p.connect(p.DIRECT)`，以確保可以正常啟動和運行。

完整errors:
```
 ⚡ root@6380aa841108  ~  ros2 run pros_car_py robot_control
pybullet build time: Aug  9 2024 12:32:26
startThreads creating 1 threads.
starting thread 0
started thread 0
argc=2
argv[0] = --unused
argv[1] = --start_demo_name=Physics Server
ExampleBrowserThreadFunc started
X11 functions dynamically loaded using dlopen/dlsym OK!
    cannot connect to X server
[ros2run]: Process exited with failure 1
 ✘⚡ root@6380aa841108  ~ 
```
附註：此問題在「特定用戶」 MacOS 環境(M Series)下，但不確定是否為所有 MacOS 環境的普遍問題。Docker 環境下的 X Server 連接失敗是明確的觸發原因。

為 `robot_control` 節點（main2.py）增加 `--ros-args -p gui:=<bool>` 參數功能，以控制 PyBullet 模擬環境是否顯示 GUI。

主要修改：
- 在 `main2.py` 中增加 `gui` ROS 參數的宣告與讀取邏輯，預設值為 `True`。
- 修改 `ArmController` 的 `__init__` 方法，增加 `use_gui` 參數，並將其傳遞給 `ik_solver.createWorld` 方法。
- 將從 ROS 參數讀取的 `use_gui` 值從 `main2.py` 傳遞給 `ArmController` 實例。

如此一來，使用者可以透過以下指令啟動節點：
- `ros2 run pros_car_py robot_control` (啟用 GUI，預設)
- `ros2 run pros_car_py robot_control --ros-args -p gui:=true` (明確啟用 GUI)
- `ros2 run pros_car_py robot_control --ros-args -p gui:=false` (停用 GUI)

# pros_car 使用說明
## class diagram
![pros_car](https://github.com/alianlbj23/pros_car/blob/main/img/pros_car.drawio.png?raw=true)
## 🚀 環境初始化
1. 執行以下指令進入環境：
   ```bash
   ./car_control.sh
   ```
2. 在環境內輸入 `r` 來執行建置與設定：
   ```bash
   r  # 進行 colcon build 並執行 . ./install/setup.bash
   ```

## 🚗 車輛控制
執行以下指令來開始車輛控制：
```bash
ros2 run pros_car_py robot_control
```
執行後，畫面將會顯示控制介面。

### 🔹 車輛手動控制
| 鍵盤按鍵 | 功能描述 |
|---------|---------|
| `w` | **前進** |
| `s` | **後退** |
| `a` | **左斜走** |
| `d` | **右斜走** |
| `e` | **左自轉** |
| `r` | **右自轉** |
| `z` | **停止** |
| `q` | **回到主選單** |

## 🤖 手動機械臂控制
1. 進入機械臂控制模式後，選擇 **0~4 號關節** 來調整角度。
2. 角度調整指令：
   | 鍵盤按鍵 | 功能描述 |
   |---------|---------|
   | `i` | **增加角度** |
   | `k` | **減少角度** |
   | `q` | **回到關節選擇** |

## 📍 自動導航模式
共有 **兩種自動導航模式**：

### 1️⃣ 手動導航 (`manual_auto_nav`)
- **功能**：接收 **Foxglove** 所發送的 `/goal_pose` **座標** 來進行導航。

### 2️⃣ 目標導航 (`target_auto_nav`)
- **功能**：由 `car_controller.py` 內部自動 `publish` `/goal_pose` **座標**，進行自動導航。

📢 **注意**：在使用導航模式時，**按下 `q`** 即可立即停止車輛移動並退出導航模式。

---

# pros_car Usage Guide

## 🚀 Environment Setup
1. Enter the environment by running:
   ```bash
   ./car_control.sh
   ```
2. Inside the environment, enter `r` to build and set up:
   ```bash
   r  # Run colcon build and source setup.bash
   ```

## 🚗 Vehicle Control
Start vehicle control by running:
```bash
ros2 run pros_car_py robot_control
```
Once started, the control interface will appear.

### 🔹 Manual Vehicle Control
| Key | Action |
|---------|---------|
| `w` | **Move forward** |
| `s` | **Move backward** |
| `a` | **Move diagonally left** |
| `d` | **Move diagonally right** |
| `e` | **Rotate left** |
| `r` | **Rotate right** |
| `z` | **Stop** |
| `q` | **Return to the main menu** |

## 🤖 Manual Arm Control
1. Enter **joint control mode**, then select a joint (0~4) to adjust its angle.
2. Use the following keys to control the joint angles:
   | Key | Action |
   |---------|---------|
   | `i` | **Increase angle** |
   | `k` | **Decrease angle** |
   | `q` | **Return to joint selection** |

## 📍 Autonomous Navigation Modes
There are **two autonomous navigation modes**:

### 1️⃣ Manual Auto Navigation (`manual_auto_nav`)
- **Function**: Receives `/goal_pose` coordinates from **Foxglove** and navigates accordingly.

### 2️⃣ Target Auto Navigation (`target_auto_nav`)
- **Function**: `car_controller.py` internally **publishes** `/goal_pose` coordinates for automatic navigation.

📢 **Note**: Press `q` at any time to **stop the vehicle immediately** and exit navigation mode.

