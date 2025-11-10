# 手势控制贪吃蛇游戏 (Hand-Gesture Controlled Snake Game)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

通过摄像头实时识别手势，用食指控制贪吃蛇的实时游戏。

A real-time Snake game controlled by hand gestures detected through your webcam using your index finger.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)

## 功能特点 (Features)

- 🎮 **实时手势识别**: 使用 MediaPipe 进行手部追踪
- 🐍 **经典贪吃蛇**: 传统贪吃蛇游戏玩法
- 📹 **摄像头视频流**: 实时显示摄像头画面
- 👆 **食指控制**: 使用食指作为蛇头位置
- 🎯 **简单直观**: 无需键盘，仅需手势即可游玩

---

- 🎮 **Real-time gesture recognition**: Hand tracking using MediaPipe
- 🐍 **Classic Snake game**: Traditional Snake gameplay
- 📹 **Webcam video stream**: Live camera feed display
- 👆 **Index finger control**: Use your index finger as the snake head
- 🎯 **Simple and intuitive**: No keyboard needed, just gestures

## 工作原理 (How It Works)

1. **摄像头捕获**: 程序从摄像头获取实时视频流
2. **手部检测**: MediaPipe 检测并追踪手部关键点
3. **食指定位**: 提取食指尖端位置作为控制点
4. **游戏控制**: 蛇头跟随食指移动
5. **游戏逻辑**: 标准贪吃蛇规则（吃食物、增长、碰撞检测）

---

1. **Webcam capture**: Captures real-time video stream from webcam
2. **Hand detection**: MediaPipe detects and tracks hand landmarks
3. **Index finger positioning**: Extracts index finger tip position as control point
4. **Game control**: Snake head follows the index finger
5. **Game logic**: Standard Snake rules (eat food, grow, collision detection)

## 系统要求 (Requirements)

- Python 3.7 或更高版本 (or higher)
- 摄像头 (Webcam)
- 操作系统 (Operating System): Windows, macOS, or Linux

## 安装说明 (Installation)

### 1. 克隆仓库 (Clone the repository)

```bash
git clone https://github.com/YJxyzxyz/Snake-Video.git
cd Snake-Video
```

### 2. 创建虚拟环境（推荐）(Create virtual environment - recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖 (Install dependencies)

```bash
pip install -r requirements.txt
```

## 使用方法 (Usage)

### 快速启动（推荐）(Quick Start - Recommended)

```bash
python start.py
```

这个脚本会自动检查依赖和摄像头，然后启动游戏。

This script automatically checks dependencies and camera, then starts the game.

### 直接启动 (Direct Start)

```bash
python main.py
```

### 游戏控制 (Game Controls)

- **移动蛇**: 在摄像头前移动你的手，用食指指向你想让蛇头去的位置
- **重新开始**: 按 `R` 键
- **退出游戏**: 按 `Q` 键

---

- **Move snake**: Move your hand in front of the camera, point your index finger where you want the snake head to go
- **Restart**: Press `R` key
- **Quit**: Press `Q` key

### 游戏提示 (Game Tips)

1. 确保光线充足，以便更好地识别手部
2. 将手保持在摄像头视野内
3. 伸出食指，其他手指可以握拳
4. 蛇头会跟随食指尖端位置移动
5. 收集红色食物得分并增长
6. 避免咬到自己的身体

---

1. Ensure good lighting for better hand detection
2. Keep your hand within the camera view
3. Extend your index finger, other fingers can be in a fist
4. The snake head follows your index finger tip
5. Collect red food to score and grow
6. Avoid biting your own body

## 项目结构 (Project Structure)

```
Snake-Video/
│
├── main.py              # 主程序入口 (Main application entry)
├── start.py             # 快速启动脚本 (Quick start script with checks)
├── hand_tracker.py      # 手部追踪模块 (Hand tracking module)
├── snake_game.py        # 贪吃蛇游戏逻辑 (Snake game logic)
├── requirements.txt     # 依赖列表 (Dependencies)
├── .gitignore          # Git 忽略文件 (Git ignore file)
├── README.md           # 项目说明 (Project documentation)
└── LICENSE             # 许可证 (License)
```

## 技术栈 (Technology Stack)

- **Python**: 主要编程语言 (Primary programming language)
- **OpenCV**: 视频捕获和图像处理 (Video capture and image processing)
- **MediaPipe**: 手部检测和追踪 (Hand detection and tracking)
- **NumPy**: 数值计算 (Numerical computing)

## 常见问题 (Troubleshooting)

### 摄像头无法打开 (Camera not opening)

- 检查摄像头是否被其他程序占用
- 确认摄像头权限设置
- 尝试更改 `main.py` 中的摄像头索引 (0 改为 1 或 2)

```python
self.cap = cv2.VideoCapture(0)  # 尝试改为 1 或 2 (Try changing to 1 or 2)
```

### 手部识别不准确 (Hand detection inaccurate)

- 确保光线充足
- 调整手与摄像头的距离
- 修改 `hand_tracker.py` 中的检测置信度参数

```python
min_detection_confidence=0.7  # 降低到 0.5 试试 (Try lowering to 0.5)
```

### 游戏运行卡顿 (Game is laggy)

- 降低视频分辨率 (在 `main.py` 中)
- 关闭其他占用 CPU 的程序

## 自定义配置 (Customization)

### 调整游戏难度 (Adjust game difficulty)

在 `main.py` 中修改网格大小：

```python
self.game = SnakeGame(grid_width=20, grid_height=15, cell_size=30)
```

- `grid_width`: 网格宽度（格子数）
- `grid_height`: 网格高度（格子数）
- `cell_size`: 每格像素大小

### 修改颜色主题 (Change color theme)

在 `main.py` 的 `self.colors` 字典中修改颜色（BGR 格式）

## 贡献 (Contributing)

欢迎提交问题和拉取请求！

Issues and pull requests are welcome!

## 许可证 (License)

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 作者 (Author)

Xiao Yizhe

## 致谢 (Acknowledgments)

- [MediaPipe](https://mediapipe.dev/) - Google 的手部追踪解决方案
- [OpenCV](https://opencv.org/) - 计算机视觉库
- 经典贪吃蛇游戏启发

---

- [MediaPipe](https://mediapipe.dev/) - Google's hand tracking solution
- [OpenCV](https://opencv.org/) - Computer vision library
- Inspired by the classic Snake game

## 演示 (Demo)

运行程序后，你将看到：
1. 摄像头实时视频流
2. 手部关键点标注
3. 游戏网格叠加显示
4. 绿色的蛇和红色的食物
5. 实时得分显示

---

After running the program, you will see:
1. Real-time webcam video stream
2. Hand landmark annotations
3. Game grid overlay
4. Green snake and red food
5. Real-time score display

## 未来改进 (Future Improvements)

- [ ] 添加难度级别选择
- [ ] 记录最高分
- [ ] 支持多种手势控制
- [ ] 添加音效
- [ ] 优化性能

---

- [ ] Add difficulty level selection
- [ ] High score tracking
- [ ] Support multiple gesture controls
- [ ] Add sound effects
- [ ] Performance optimization
