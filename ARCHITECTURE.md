# Architecture Overview / 架构概述

## System Architecture / 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                          │
│                        (main.py)                              │
└───────────────┬─────────────────────────────┬─────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌────────────────────────────┐
│    Hand Tracker Module    │   │    Snake Game Module       │
│    (hand_tracker.py)      │   │    (snake_game.py)         │
│                           │   │                            │
│  - MediaPipe Integration  │   │  - Game Logic             │
│  - Hand Detection         │   │  - Collision Detection    │
│  - Finger Position        │   │  - Score Management       │
└───────────┬───────────────┘   └────────────┬───────────────┘
            │                                │
            ▼                                ▼
    ┌───────────────┐              ┌────────────────┐
    │   MediaPipe   │              │  Game State    │
    │  Hand Solver  │              │  (Snake, Food) │
    └───────────────┘              └────────────────┘
```

## Module Descriptions / 模块说明

### 1. main.py - Main Application / 主应用程序

**Purpose / 目的:**
- Integrates all components / 整合所有组件
- Manages the main game loop / 管理主游戏循环
- Handles video capture and display / 处理视频捕获和显示

**Key Classes / 关键类:**
- `SnakeVideoGame`: Main game controller

**Key Methods / 关键方法:**
- `__init__()`: Initialize webcam, hand tracker, and game
- `run()`: Main game loop
- `draw_grid()`: Draw game grid overlay
- `draw_snake()`: Render snake on video
- `draw_food()`: Render food on video
- `draw_ui()`: Display score and instructions
- `cleanup()`: Release resources

**Flow / 流程:**
1. Initialize webcam (1280x720)
2. Create hand tracker and game instances
3. Enter main loop:
   - Capture frame from webcam
   - Flip frame for mirror effect
   - Detect hand and get finger position
   - Update game state based on finger position
   - Draw all game elements
   - Display frame
   - Handle keyboard input (Q to quit, R to restart)

### 2. hand_tracker.py - Hand Tracking Module / 手部追踪模块

**Purpose / 目的:**
- Detect and track hand landmarks / 检测和追踪手部关键点
- Extract finger positions / 提取手指位置

**Key Classes / 关键类:**
- `HandTracker`: Wrapper for MediaPipe Hands

**Key Methods / 关键方法:**
- `__init__()`: Initialize MediaPipe hands solution
- `find_hands()`: Detect hands in frame and draw landmarks
- `get_index_finger_position()`: Get index finger tip coordinates
- `get_all_finger_positions()`: Get all finger tip positions
- `close()`: Release MediaPipe resources

**MediaPipe Landmarks / MediaPipe 关键点:**
```
Index Finger Tip: Landmark ID = 8
Other finger tips: 4 (thumb), 12 (middle), 16 (ring), 20 (pinky)
```

**Configuration / 配置:**
- `max_num_hands`: 1 (tracks one hand)
- `min_detection_confidence`: 0.7
- `min_tracking_confidence`: 0.5

### 3. snake_game.py - Game Logic Module / 游戏逻辑模块

**Purpose / 目的:**
- Implement classic Snake game mechanics / 实现经典贪吃蛇游戏机制
- Manage game state / 管理游戏状态

**Key Classes / 关键类:**
- `SnakeGame`: Core game logic

**Key Methods / 关键方法:**
- `__init__()`: Initialize game grid and state
- `generate_food()`: Random food placement
- `update_snake_position()`: Move snake based on finger position
- `reset()`: Reset game to initial state
- `get_snake_head()`: Return head position
- `get_snake_body()`: Return body segments
- `get_food_position()`: Return food position
- `is_game_over()`: Check game over condition

**Game Parameters / 游戏参数:**
- Grid: 20x15 cells
- Cell size: 30 pixels
- Starting position: Center of grid
- Food score: +10 points per food item

**Game Rules / 游戏规则:**
1. Snake follows index finger position
2. Snake grows when eating food
3. Game over if snake bites itself (after length > 4)
4. Food randomly spawns after being eaten

### 4. start.py - Quick Start Script / 快速启动脚本

**Purpose / 目的:**
- Perform pre-flight checks / 执行启动前检查
- Verify dependencies / 验证依赖项
- Check camera availability / 检查摄像头可用性

**Key Functions / 关键函数:**
- `check_dependencies()`: Verify all Python packages installed
- `check_camera()`: Test camera accessibility
- `main()`: Run checks and start game

## Data Flow / 数据流

```
Camera Frame
    ↓
[Flip Horizontally]
    ↓
Hand Tracker
    ↓
Index Finger Position (x, y)
    ↓
[Adjust to Game Grid]
    ↓
Snake Game Logic
    ↓
Update Snake Position
    ↓
Check Collisions
    ↓
Update Score
    ↓
[Render]
    ↓
Display Frame with Overlays
```

## Coordinate Systems / 坐标系统

### Screen Coordinates / 屏幕坐标
- Origin (0,0) at top-left corner
- X increases to the right
- Y increases downward
- Camera resolution: 1280x720

### Game Grid Coordinates / 游戏网格坐标
- Grid offset: (50, 50) pixels from top-left
- Grid size: 20x15 cells
- Cell size: 30x30 pixels
- Total grid size: 600x450 pixels

### Conversion / 转换
```python
# Pixel to grid cell
grid_x = (pixel_x - offset_x) // cell_size
grid_y = (pixel_y - offset_y) // cell_size

# Grid cell to pixel
pixel_x = offset_x + grid_x * cell_size
pixel_y = offset_y + grid_y * cell_size
```

## Performance Considerations / 性能考虑

### Frame Rate / 帧率
- Target: 30 FPS
- Actual: Depends on hardware (typically 20-30 FPS)

### Optimization Strategies / 优化策略
1. Process only necessary frames
2. Minimal drawing operations
3. Efficient collision detection
4. Single hand tracking (max_num_hands=1)

### Resource Usage / 资源使用
- CPU: Moderate (MediaPipe hand tracking)
- Memory: ~200-300 MB
- Camera: 1280x720 @ 30fps

## Color Scheme / 色彩方案 (BGR Format)

```python
snake_head:     (0, 255, 0)    # Bright green
snake_body:     (0, 200, 0)    # Dark green
food:           (0, 0, 255)    # Red
grid:           (50, 50, 50)   # Dark gray
background:     (30, 30, 30)   # Very dark gray
text:           (255, 255, 255)# White
game_over:      (0, 0, 255)    # Red
finger_marker:  (255, 0, 255)  # Magenta
```

## Error Handling / 错误处理

### Camera Errors / 摄像头错误
- Camera not found: Exit with error message
- Camera access denied: Check permissions
- Camera in use: Close other applications

### Hand Detection Errors / 手部检测错误
- No hand detected: Continue game with last position
- Multiple hands: Use first detected hand
- Poor lighting: Suggest better lighting

### Game Errors / 游戏错误
- All handled gracefully
- Game over state allows restart
- Keyboard interrupt caught

## Extension Points / 扩展点

### Easy Modifications / 简单修改
1. Change grid size in `SnakeGame.__init__()`
2. Adjust colors in `SnakeVideoGame.__init__()`
3. Modify detection confidence in `HandTracker.__init__()`
4. Change camera resolution in `SnakeVideoGame.__init__()`

### Advanced Extensions / 高级扩展
1. Add difficulty levels (speed control)
2. Add sound effects
3. Add high score persistence
4. Support multiple gesture controls
5. Add power-ups and obstacles
6. Multi-player mode

## Dependencies / 依赖关系

```
opencv-python (4.8.1.78)
├── numpy (1.24.3)
└── [System: Camera drivers]

mediapipe (0.10.8)
├── numpy (1.24.3)
├── opencv-python
└── [Pre-trained ML models]

numpy (1.24.3)
└── [System: BLAS/LAPACK libraries]
```

## Testing Notes / 测试说明

### Manual Testing Checklist / 手动测试清单
- [ ] Camera opens successfully
- [ ] Hand is detected and landmarks shown
- [ ] Index finger position tracked accurately
- [ ] Snake follows finger smoothly
- [ ] Food collection increases score
- [ ] Snake grows after eating food
- [ ] Collision detection works (game over on self-bite)
- [ ] Restart (R key) works
- [ ] Quit (Q key) works
- [ ] UI displays correctly

### Known Limitations / 已知限制
1. Requires good lighting for hand detection
2. Single hand tracking only
3. No save/load game state
4. No sound effects
5. Fixed difficulty level
6. Requires webcam

## Future Improvements / 未来改进

1. **Performance**
   - GPU acceleration for MediaPipe
   - Reduce detection latency
   - Optimize rendering

2. **Features**
   - Multiple difficulty levels
   - High score leaderboard
   - Sound effects and music
   - Different game modes
   - Custom themes

3. **User Experience**
   - Better visual feedback
   - Tutorial mode
   - Gesture calibration
   - Settings menu

4. **Code Quality**
   - Unit tests
   - Integration tests
   - Code documentation
   - Type hints
