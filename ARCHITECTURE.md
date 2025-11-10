# Architecture Overview / 架构概述

## System Architecture / 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Game Launcher                                │
│                   (game_launcher.py)                             │
│  - Multiple game selection                                       │
│  - Game switching                                                │
└───────────────┬──────────────────────────┬──────────────────────┘
                │                          │
                ▼                          ▼
┌───────────────────────────┐  ┌────────────────────────────────┐
│   Main Application        │  │    Additional Games            │
│      (main.py)            │  │  - Fruit Slicer Game           │
│  - Snake Game Enhanced    │  │  - Flappy Hand Game            │
│  - Menu Integration       │  │                                │
└───────┬──────┬──────┬─────┘  └────────────────────────────────┘
        │      │      │
        ▼      ▼      ▼
┌─────────┐ ┌──────────┐ ┌──────────────┐
│ Hand    │ │ Gesture  │ │  Snake Game  │
│ Tracker │ │Recognizer│ │   Module     │
└────┬────┘ └────┬─────┘ └───────┬──────┘
     │           │               │
     ▼           ▼               ▼
┌─────────────────────────────────────────┐
│         Supporting Modules              │
│  - GameConfig: Settings & High Scores   │
│  - SoundManager: Audio Effects          │
│  - GameMenu: UI Menu System             │
└─────────────────────────────────────────┘
```

## Module Descriptions / 模块说明

### 1. game_launcher.py - Game Launcher / 游戏启动器

**Purpose / 目的:**
- Manage multiple games / 管理多个游戏
- Provide game selection interface / 提供游戏选择界面
- Handle game switching / 处理游戏切换

**Key Classes / 关键类:**
- `GameLauncher`: Main launcher controller

**Key Methods / 关键方法:**
- `show_game_selection()`: Display game menu
- `start_game()`: Initialize selected game
- `run_snake_game()`, `run_fruit_slicer()`, `run_flappy_hand()`: Game-specific logic

### 2. main.py - Main Snake Game Application / 主贪吃蛇应用程序

**Purpose / 目的:**
- Enhanced snake game with all features / 增强版贪吃蛇游戏
- Integrate config, sound, menu systems / 整合配置、音效、菜单系统
- Manage the main game loop / 管理主游戏循环

**Key Classes / 关键类:**
- `SnakeVideoGame`: Enhanced game controller

**Key Methods / 关键方法:**
- `__init__()`: Initialize with config, sound, menu
- `run()`: Main game loop with menu support
- `draw_ui()`: Enhanced UI with high scores and difficulty
- All previous drawing methods

**New Features / 新功能:**
- Difficulty level support
- High score tracking
- Sound effects
- Pause functionality
- Menu system integration
- Gesture-based menu control

### 3. game_config.py - Configuration Module / 配置模块

**Purpose / 目的:**
- Manage game settings / 管理游戏设置
- Handle difficulty levels / 处理难度级别
- Persist high scores / 持久化最高分

**Key Classes / 关键类:**
- `Difficulty`: Enum for difficulty levels
- `GameConfig`: Configuration manager

**Key Methods / 关键方法:**
- `load_config()`, `save_config()`: Persistence
- `set_difficulty()`: Change difficulty
- `update_high_score()`: Track high scores
- `toggle_sound()`: Sound on/off

**Configuration / 配置:**
- Easy: slow speed, 1x multiplier
- Medium: normal speed, 2x multiplier
- Hard: fast speed, 3x multiplier

### 4. sound_manager.py - Sound Manager / 音效管理器

**Purpose / 目的:**
- Play game sound effects / 播放游戏音效
- Cross-platform audio support / 跨平台音频支持

**Key Classes / 关键类:**
- `SoundManager`: Audio controller

**Key Methods / 关键方法:**
- `play_eat_sound()`: Food collection sound
- `play_game_over_sound()`: Game over sequence
- `play_level_up_sound()`: Milestone sound
- `play_menu_sound()`: Menu navigation sound

**Platform Support / 平台支持:**
- Windows: winsound
- macOS: afplay
- Linux: system beep

### 5. gesture_recognizer.py - Gesture Recognition / 手势识别

**Purpose / 目的:**
- Recognize various hand gestures / 识别多种手势
- Enable gesture-based controls / 启用手势控制

**Key Classes / 关键类:**
- `GestureRecognizer`: Gesture detection engine

**Key Methods / 关键方法:**
- `recognize_gesture()`: Main recognition method
- `_detect_gesture()`: Internal gesture detection
- `_count_fingers_up()`: Finger state detection
- `_is_pinch()`, `_is_thumbs_up()`, etc.: Specific gestures

**Supported Gestures / 支持的手势:**
- Point (index finger)
- Peace (index + middle)
- Open palm (all fingers)
- Fist (no fingers)
- Pinch (thumb + index close)
- Thumbs up/down

### 6. game_menu.py - Menu System / 菜单系统

**Purpose / 目的:**
- Provide in-game menu UI / 提供游戏内菜单UI
- Handle menu navigation / 处理菜单导航

**Key Classes / 关键类:**
- `GameMenu`: Menu controller

**Key Methods / 关键方法:**
- `show_main_menu()`: Main menu display
- `show_difficulty_menu()`: Difficulty selection
- `show_high_scores()`: High score display
- `navigate_up()`, `navigate_down()`: Navigation
- `select()`: Menu item selection

### 7. fruit_slicer_game.py - Fruit Slicer Game / 水果切切乐

**Purpose / 目的:**
- Fruit Ninja-style game / 水果忍者风格游戏
- Swipe gesture interaction / 滑动手势交互

**Key Classes / 关键类:**
- `Fruit`: Fruit object
- `FruitSlicerGame`: Game logic

**Game Mechanics / 游戏机制:**
- Fruits spawn from bottom
- Swipe to slice fruits
- Don't let fruits fall
- 3 lives system

### 8. flappy_hand_game.py - Flappy Hand Game / 飞扬之手

**Purpose / 目的:**
- Flappy Bird-style game / Flappy Bird 风格游戏
- Hand height control / 手部高度控制

**Key Classes / 关键类:**
- `Pipe`: Obstacle pipe
- `FlappyHandGame`: Game logic

**Game Mechanics / 游戏机制:**
- Control bird with hand height
- Avoid pipes
- Smooth movement
- Score for passing pipes

### 9. hand_tracker.py - Hand Tracking Module / 手部追踪模块

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

### 10. snake_game.py - Game Logic Module / 游戏逻辑模块

**Purpose / 目的:**
- Implement classic Snake game mechanics / 实现经典贪吃蛇游戏机制
- Manage game state / 管理游戏状态

**Key Classes / 关键类:**
- `SnakeGame`: Core game logic

**Key Methods / 关键方法:**
- `__init__()`: Initialize game grid and state with speed control
- `generate_food()`: Random food placement
- `update_snake_position()`: Move snake based on finger position with speed delay
- `toggle_pause()`: Pause/resume game
- `set_speed_delay()`: Adjust game speed
- `reset()`: Reset game to initial state
- `get_snake_head()`, `get_snake_body()`, `get_food_position()`: Getters
- `is_game_over()`: Check game over condition

**Game Parameters / 游戏参数:**
- Grid: 20x15 cells
- Cell size: 30 pixels
- Starting position: Center of grid
- Food score: +10 points per food item
- Speed delay: Varies by difficulty (3-15 frames)

**New Features / 新功能:**
- Pause functionality
- Adjustable speed
- Frame-based movement control
- Returns ate_food status

**Game Rules / 游戏规则:**
1. Snake follows index finger position
2. Snake grows when eating food
3. Game over if snake bites itself (after length > 4)
4. Food randomly spawns after being eaten

### 11. start.py - Quick Start Script / 快速启动脚本

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
