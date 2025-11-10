# 手势控制游戏合集 (Hand-Gesture Controlled Game Collection)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

通过摄像头实时识别手势，控制多款互动游戏的游戏合集。

A collection of interactive games controlled by hand gestures detected through your webcam.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)

## 游戏列表 (Game Collection)

### 🐍 经典贪吃蛇 (Snake Game)
- 使用食指控制蛇头位置
- 支持三种难度级别
- 记录最高分
- 音效反馈

### 🍎 水果切切乐 (Fruit Slicer)
- 类似水果忍者的游戏
- 用手指滑动切割水果
- 不要让水果掉落
- 生命值系统

### 🐦 飞扬之手 (Flappy Hand)
- 类似 Flappy Bird 的游戏
- 通过手的高度控制小鸟飞行
- 避开管道障碍
- 挑战高分

## 功能特点 (Features)

### 核心功能
- 🎮 **实时手势识别**: 使用 MediaPipe 进行手部追踪
- 🎯 **多种手势控制**: 支持点击、滑动、和平手势等多种手势
- 📹 **摄像头视频流**: 实时显示摄像头画面
- 🎵 **音效系统**: 游戏音效和背景音乐
- 💾 **数据持久化**: 自动保存最高分和游戏设置

### 贪吃蛇游戏增强功能
- 🎚️ **难度选择**: 简单、中等、困难三种难度
- 🏆 **最高分记录**: 分难度记录最高分
- ⏸️ **暂停功能**: 随时暂停和恢复游戏
- 📊 **实时统计**: 显示当前分数和最高分
- 🎨 **菜单系统**: 完整的游戏设置菜单

## 工作原理 (How It Works)

1. **摄像头捕获**: 程序从摄像头获取实时视频流
2. **手部检测**: MediaPipe 检测并追踪手部关键点
3. **手势识别**: 识别多种手势（指向、滑动、和平手势等）
4. **游戏控制**: 根据手势控制不同游戏
5. **游戏逻辑**: 实现各个游戏的完整逻辑
6. **音效反馈**: 提供即时的音效反馈

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

#### 启动游戏合集 (Launch Game Collection)
```bash
python game_launcher.py
```

这个启动器包含所有游戏，可以在菜单中选择要玩的游戏。

This launcher includes all games, you can select which game to play from the menu.

#### 单独启动贪吃蛇游戏 (Launch Snake Game Only)
```bash
python start.py
```

或者直接运行：
```bash
python main.py
```

### 游戏控制 (Game Controls)

#### 贪吃蛇游戏 (Snake Game)
- **移动蛇**: 在摄像头前移动你的手，用食指指向你想让蛇头去的位置
- **暂停**: 按 `P` 键或使用和平手势 ✌️
- **菜单**: 按 `M` 键打开游戏菜单
- **重新开始**: 按 `R` 键
- **退出游戏**: 按 `Q` 键

#### 水果切切乐 (Fruit Slicer)
- **切水果**: 用食指在屏幕上快速滑动
- **重新开始**: 按 `R` 键
- **返回菜单**: 按 `ESC` 键
- **退出**: 按 `Q` 键

#### 飞扬之手 (Flappy Hand)
- **控制飞行**: 上下移动手掌来控制小鸟高度
- **重新开始**: 按 `R` 键
- **返回菜单**: 按 `ESC` 键
- **退出**: 按 `Q` 键

---

- **Move snake**: Move your hand in front of the camera, point your index finger where you want the snake head to go
- **Pause**: Press `P` key or use peace gesture ✌️
- **Menu**: Press `M` key to open game menu
- **Restart**: Press `R` key
- **Quit**: Press `Q` key

### 游戏菜单功能 (Game Menu Features)

#### 贪吃蛇游戏菜单
1. **恢复游戏**: 返回游戏
2. **难度选择**: 简单/中等/困难
3. **音效开关**: 开启或关闭音效
4. **最高分**: 查看各难度最高分
5. **退出**: 退出游戏

使用 ↑↓ 键导航，Enter 键选择。

### 游戏提示 (Game Tips)

#### 通用提示
1. 确保光线充足，以便更好地识别手部
2. 将手保持在摄像头视野内
3. 保持手部稳定，避免抖动
4. 调整与摄像头的距离以获得最佳识别效果

#### 贪吃蛇游戏提示
1. 伸出食指，其他手指可以握拳
2. 蛇头会跟随食指尖端位置移动
3. 收集红色食物得分并增长
4. 避免咬到自己的身体
5. 选择合适的难度开始游戏

#### 水果切切乐提示
1. 快速滑动手指切割水果
2. 不要让水果掉落，会失去生命
3. 连续切割可以获得更高分数
4. 注意水果出现的速度会逐渐加快

#### 飞扬之手提示
1. 平稳移动手掌控制小鸟高度
2. 提前预判管道位置
3. 保持冷静，不要过度反应
4. 练习可以提高反应速度

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

贪吃蛇游戏支持三种难度：

1. **简单模式**: 蛇速度较慢，适合初学者
2. **中等模式**: 中等速度，平衡的游戏体验
3. **困难模式**: 蛇速度很快，适合高手挑战

在游戏菜单中选择难度，或在 `game_config.py` 中修改默认难度。

### 调整游戏参数 (Adjust game parameters)

在 `main.py` 中修改网格大小：

```python
self.game = SnakeGame(grid_width=20, grid_height=15, cell_size=30, speed_delay=8)
```

- `grid_width`: 网格宽度（格子数）
- `grid_height`: 网格高度（格子数）
- `cell_size`: 每格像素大小
- `speed_delay`: 蛇移动速度延迟（越小越快）

### 修改颜色主题 (Change color theme)

在 `main.py` 的 `self.colors` 字典中修改颜色（BGR 格式）

### 音效设置 (Sound Settings)

在游戏菜单中可以开启或关闭音效，设置会自动保存。

## 贡献 (Contributing)

欢迎提交问题和拉取请求！

Issues and pull requests are welcome!

## 许可证 (License)

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 演示 (Demo)

运行程序后，你将看到：

### 游戏选择界面
1. 游戏列表和说明
2. 可以使用数字键快速选择
3. 按 Enter 开始游戏

### 贪吃蛇游戏
1. 摄像头实时视频流
2. 手部关键点标注
3. 游戏网格叠加显示
4. 绿色的蛇和红色的食物
5. 实时得分和最高分显示
6. 难度显示
7. 暂停状态指示

### 水果切切乐
1. 从底部弹出的彩色水果
2. 手指滑动轨迹显示
3. 分数和生命值显示
4. 游戏结束统计

### 飞扬之手
1. 可爱的小鸟角色
2. 移动的管道障碍
3. 实时分数显示
4. 流畅的动画效果

## 已实现的改进 (Implemented Improvements)

✅ **难度级别选择**: 三种难度（简单、中等、困难）  
✅ **最高分记录**: 分难度记录并持久化保存  
✅ **多种手势控制**: 支持和平手势打开菜单等  
✅ **音效系统**: 吃食物、游戏结束等音效  
✅ **性能优化**: 帧率控制和流畅的游戏体验  
✅ **暂停功能**: 随时暂停和恢复游戏  
✅ **菜单系统**: 完整的设置和选项菜单  
✅ **多个游戏**: 三款不同类型的手势控制游戏  
✅ **数据持久化**: 自动保存游戏数据和设置  
✅ **手势识别增强**: 识别多种手势（拳头、和平、指向等）

## 技术特点 (Technical Features)

- **模块化设计**: 各个模块独立，易于扩展
- **配置管理**: 统一的配置管理系统
- **手势识别**: 支持多种手势的识别系统
- **音效管理**: 跨平台的音效系统
- **菜单系统**: 完整的UI菜单系统
- **游戏引擎**: 可扩展的游戏框架
