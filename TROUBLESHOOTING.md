# Troubleshooting Guide / 故障排除指南

## Common Issues and Solutions / 常见问题及解决方案

### 1. Camera Issues / 摄像头问题

#### Issue: "Cannot open camera" / 问题："无法打开摄像头"

**Symptoms / 症状:**
- Error message when starting the game
- Black screen instead of video feed
- Camera light doesn't turn on

**Solutions / 解决方案:**

1. **Check if camera is already in use / 检查摄像头是否被占用**
   ```bash
   # Close other applications using the camera
   # 关闭其他使用摄像头的应用程序
   # Examples: Zoom, Skype, Teams, other video apps
   ```

2. **Try different camera index / 尝试不同的摄像头索引**
   
   Edit `main.py`, line ~17:
   ```python
   # Change from:
   self.cap = cv2.VideoCapture(0)
   
   # Try:
   self.cap = cv2.VideoCapture(1)  # or 2, 3...
   ```

3. **Check camera permissions / 检查摄像头权限**
   
   **Windows:**
   - Settings → Privacy → Camera
   - Enable "Allow apps to access your camera"
   
   **macOS:**
   - System Preferences → Security & Privacy → Camera
   - Grant permission to Terminal or your Python IDE
   
   **Linux:**
   - Check if user is in video group:
     ```bash
     groups $USER
     sudo usermod -a -G video $USER
     ```

4. **Test camera with other tools / 用其他工具测试摄像头**
   ```bash
   # Test with OpenCV
   python -c "import cv2; print('Camera available:', cv2.VideoCapture(0).isOpened())"
   ```

---

### 2. Hand Detection Issues / 手部检测问题

#### Issue: "Hand not detected" or "Landmarks not showing" / 问题："检测不到手"或"关键点未显示"

**Symptoms / 症状:**
- No hand landmarks drawn on video
- Snake doesn't respond to hand movements
- Green skeleton lines not visible

**Solutions / 解决方案:**

1. **Improve lighting / 改善光照**
   - Ensure room is well-lit
   - Avoid backlighting (light behind you)
   - Use natural or white light
   - Position light source in front of you

2. **Adjust hand position / 调整手部位置**
   - Keep hand within 30-100 cm from camera
   - Face palm toward camera
   - Spread fingers clearly
   - Avoid quick movements

3. **Reduce detection sensitivity / 降低检测灵敏度**
   
   Edit `hand_tracker.py`, line ~19:
   ```python
   # Change from:
   min_detection_confidence=0.7
   
   # To:
   min_detection_confidence=0.5  # Lower = more sensitive
   ```

4. **Check background / 检查背景**
   - Use plain, non-reflective background
   - Avoid busy patterns behind your hand
   - Avoid skin-colored background

5. **Clean camera lens / 清洁摄像头镜头**
   - Gently clean with soft cloth
   - Remove any dust or smudges

---

### 3. Performance Issues / 性能问题

#### Issue: "Laggy video" or "Low frame rate" / 问题："视频卡顿"或"帧率低"

**Symptoms / 症状:**
- Choppy video feed
- Delayed hand tracking
- Slow snake response

**Solutions / 解决方案:**

1. **Reduce video resolution / 降低视频分辨率**
   
   Edit `main.py`, lines ~17-18:
   ```python
   # Change from:
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
   
   # To:
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

2. **Close other applications / 关闭其他应用程序**
   - Close browsers with many tabs
   - Close video editing software
   - Close other Python processes

3. **Reduce game grid size / 减小游戏网格**
   
   Edit `main.py`, line ~26:
   ```python
   # Change from:
   self.game = SnakeGame(grid_width=20, grid_height=15, cell_size=30)
   
   # To:
   self.game = SnakeGame(grid_width=15, grid_height=10, cell_size=30)
   ```

4. **Upgrade Python packages / 升级 Python 包**
   ```bash
   pip install --upgrade opencv-python mediapipe
   ```

---

### 4. Installation Issues / 安装问题

#### Issue: "Module not found" errors / 问题："找不到模块"错误

**Symptoms / 症状:**
```
ModuleNotFoundError: No module named 'cv2'
ModuleNotFoundError: No module named 'mediapipe'
```

**Solutions / 解决方案:**

1. **Ensure virtual environment is activated / 确保虚拟环境已激活**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install all dependencies / 安装所有依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install packages individually / 单独安装包**
   ```bash
   pip install opencv-python==4.8.1.78
   pip install mediapipe==0.10.8
   pip install numpy==1.24.3
   ```

4. **Check Python version / 检查 Python 版本**
   ```bash
   python --version  # Should be 3.7 or higher
   ```

5. **Use Python 3 explicitly / 明确使用 Python 3**
   ```bash
   python3 -m pip install -r requirements.txt
   python3 main.py
   ```

---

### 5. Game Control Issues / 游戏控制问题

#### Issue: "Snake doesn't follow finger accurately" / 问题："蛇不能准确跟随手指"

**Symptoms / 症状:**
- Snake moves erratically
- Snake position doesn't match finger
- Delayed response

**Solutions / 解决方案:**

1. **Position hand within game grid / 将手放在游戏网格内**
   - Game grid is in upper-left area of screen
   - Keep index finger within the grid boundaries
   - Watch for magenta crosshair on finger

2. **Move finger slowly / 缓慢移动手指**
   - Avoid jerky movements
   - Make smooth transitions
   - Give time for snake to follow

3. **Calibrate finger position / 校准手指位置**
   - Observe the magenta crosshair
   - Align finger tip with desired position
   - Keep other fingers folded

4. **Adjust grid offset / 调整网格偏移**
   
   Edit `main.py`, lines ~38-39:
   ```python
   # Change position of game grid
   self.game_x_offset = 50  # Horizontal position
   self.game_y_offset = 50  # Vertical position
   ```

---

### 6. Game Over Issues / 游戏结束问题

#### Issue: "Game over too quickly" / 问题："游戏过早结束"

**Symptoms / 症状:**
- Immediate game over when starting
- Game over without apparent collision

**Solutions / 解决方案:**

1. **This is expected behavior / 这是预期行为**
   - Snake dies when it bites itself
   - Length must be > 4 for collision detection
   - Avoid crossing your own path

2. **Adjust collision threshold / 调整碰撞阈值**
   
   Edit `snake_game.py`, line ~78:
   ```python
   # Change from:
   if len(self.snake) > 4 and new_head in self.snake[1:]:
   
   # To:
   if len(self.snake) > 8 and new_head in self.snake[1:]:
   ```

3. **Start with longer snake / 从更长的蛇开始**
   
   Edit `snake_game.py`, line ~23:
   ```python
   # Change from:
   self.snake = [(center_x, center_y)]
   
   # To:
   self.snake = [(center_x, center_y), (center_x-1, center_y), (center_x-2, center_y)]
   ```

---

### 7. Display Issues / 显示问题

#### Issue: "Window too small/large" or "Can't see full game" / 问题："窗口太小/大"或"看不到完整游戏"

**Symptoms / 症状:**
- Game window doesn't fit screen
- Can't see score or instructions
- Grid is cut off

**Solutions / 解决方案:**

1. **Resize window manually / 手动调整窗口大小**
   - Drag window corners
   - Maximize window if needed

2. **Adjust camera resolution / 调整摄像头分辨率**
   
   Edit `main.py`, lines ~17-18:
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Adjust width
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Adjust height
   ```

3. **Change grid size and position / 更改网格大小和位置**
   
   Edit `main.py`:
   ```python
   # Grid size
   self.game = SnakeGame(grid_width=20, grid_height=15, cell_size=30)
   
   # Grid position
   self.game_x_offset = 50
   self.game_y_offset = 50
   ```

---

## Platform-Specific Issues / 平台特定问题

### Windows

**Issue: "DLL load failed" errors**

Solution:
```bash
# Install Visual C++ Redistributable
# Download from Microsoft website
# Or reinstall opencv-python
pip uninstall opencv-python
pip install opencv-python
```

### macOS

**Issue: "Operation not permitted" errors**

Solution:
- Grant camera permissions in System Preferences
- Run from Terminal instead of IDE
- Use Python installed via Homebrew

### Linux

**Issue: "Could not initialize video device"**

Solution:
```bash
# Install v4l-utils
sudo apt-get install v4l-utils

# Check available cameras
v4l2-ctl --list-devices

# Test camera
ffplay /dev/video0
```

---

## Debug Mode / 调试模式

To enable debug output, add this to the start of `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will print additional information about:
- Camera initialization
- Hand detection confidence
- Frame processing time
- Game state changes

---

## Getting Help / 获取帮助

If you're still experiencing issues:

1. **Check Python version**
   ```bash
   python --version
   ```

2. **Check package versions**
   ```bash
   pip list | grep -E "opencv|mediapipe|numpy"
   ```

3. **Run diagnostics**
   ```bash
   python start.py  # Includes built-in checks
   ```

4. **Create an issue on GitHub**
   - Include error messages
   - Include Python version
   - Include OS information
   - Describe what you tried

5. **Common info to provide**
   ```bash
   python --version
   pip list
   # Camera model
   # Operating system version
   ```

---

## Quick Fixes Checklist / 快速修复清单

- [ ] Camera permissions granted
- [ ] No other app using camera
- [ ] Good lighting in room
- [ ] Hand visible and within range
- [ ] All dependencies installed
- [ ] Python version 3.7+
- [ ] Virtual environment activated (if using)
- [ ] Latest code from repository
- [ ] Camera lens clean
- [ ] Sufficient system resources (RAM/CPU)

---

## Performance Optimization / 性能优化

For best experience:
1. Close unnecessary applications
2. Use good lighting
3. Position hand 50-80 cm from camera
4. Use plain background
5. Keep Python packages updated
6. Consider lower resolution if laggy
