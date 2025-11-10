"""
Hand-Gesture Controlled Snake Game
Main application that integrates hand tracking with Snake game
"""

import cv2
import numpy as np
from hand_tracker import HandTracker
from snake_game import SnakeGame
from game_config import GameConfig, Difficulty
from sound_manager import SoundManager
from gesture_recognizer import GestureRecognizer
from game_menu import GameMenu


class SnakeVideoGame:
    """Main application class"""
    
    def __init__(self):
        """Initialize the game"""
        # Initialize configuration
        self.config = GameConfig()
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Initialize hand tracker
        self.hand_tracker = HandTracker(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Initialize gesture recognizer
        self.gesture_recognizer = GestureRecognizer()
        
        # Initialize snake game with difficulty settings
        speed_delay = self.config.get_difficulty_setting('snake_speed_delay')
        self.game = SnakeGame(grid_width=20, grid_height=15, cell_size=30, speed_delay=speed_delay)
        
        # Initialize sound manager
        self.sound_manager = SoundManager(self.config.sound_enabled)
        
        # Initialize menu
        self.menu = GameMenu(self.config)
        self.menu_active = False
        self.menu_type = None  # 'main', 'difficulty', 'high_scores'
        
        # Colors (BGR format)
        self.colors = {
            'snake_head': (0, 255, 0),      # Green
            'snake_body': (0, 200, 0),      # Darker green
            'food': (0, 0, 255),            # Red
            'grid': (50, 50, 50),           # Dark gray
            'text': (255, 255, 255),        # White
            'game_over': (0, 0, 255),       # Red
            'finger_marker': (255, 0, 255)  # Magenta
        }
        
        # Game overlay position
        self.game_x_offset = 50
        self.game_y_offset = 50
        
    def draw_grid(self, frame):
        """Draw the game grid on the frame"""
        grid_width, grid_height = self.game.get_grid_dimensions()
        x_offset = self.game_x_offset
        y_offset = self.game_y_offset
        cell_size = self.game.cell_size
        
        # Draw grid background
        cv2.rectangle(
            frame,
            (x_offset, y_offset),
            (x_offset + grid_width, y_offset + grid_height),
            (30, 30, 30),
            -1
        )
        
        # Draw grid lines
        for i in range(self.game.grid_width + 1):
            x = x_offset + i * cell_size
            cv2.line(
                frame,
                (x, y_offset),
                (x, y_offset + grid_height),
                self.colors['grid'],
                1
            )
        
        for i in range(self.game.grid_height + 1):
            y = y_offset + i * cell_size
            cv2.line(
                frame,
                (x_offset, y),
                (x_offset + grid_width, y),
                self.colors['grid'],
                1
            )
    
    def draw_snake(self, frame):
        """Draw the snake on the frame"""
        cell_size = self.game.cell_size
        x_offset = self.game_x_offset
        y_offset = self.game_y_offset
        
        # Draw snake head
        head = self.game.get_snake_head()
        if head:
            x = x_offset + head[0] * cell_size
            y = y_offset + head[1] * cell_size
            cv2.rectangle(
                frame,
                (x + 2, y + 2),
                (x + cell_size - 2, y + cell_size - 2),
                self.colors['snake_head'],
                -1
            )
        
        # Draw snake body
        for segment in self.game.get_snake_body():
            x = x_offset + segment[0] * cell_size
            y = y_offset + segment[1] * cell_size
            cv2.rectangle(
                frame,
                (x + 3, y + 3),
                (x + cell_size - 3, y + cell_size - 3),
                self.colors['snake_body'],
                -1
            )
    
    def draw_food(self, frame):
        """Draw the food on the frame"""
        cell_size = self.game.cell_size
        x_offset = self.game_x_offset
        y_offset = self.game_y_offset
        
        food = self.game.get_food_position()
        x = x_offset + food[0] * cell_size + cell_size // 2
        y = y_offset + food[1] * cell_size + cell_size // 2
        
        cv2.circle(frame, (x, y), cell_size // 3, self.colors['food'], -1)
    
    def draw_finger_marker(self, frame, finger_pos):
        """Draw a marker at the finger position"""
        if finger_pos:
            # Adjust finger position to game grid coordinates
            x = self.game_x_offset + finger_pos[0]
            y = self.game_y_offset + finger_pos[1]
            
            # Draw crosshair
            cv2.circle(frame, (x, y), 10, self.colors['finger_marker'], 2)
            cv2.line(frame, (x - 15, y), (x + 15, y), self.colors['finger_marker'], 2)
            cv2.line(frame, (x, y - 15), (x, y + 15), self.colors['finger_marker'], 2)
    
    def draw_ui(self, frame):
        """Draw UI elements (score, instructions)"""
        # Draw score
        score_text = f"Score: {self.game.get_score()}"
        cv2.putText(
            frame,
            score_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            self.colors['text'],
            2
        )
        
        # Draw high score
        high_score = self.config.get_high_score()
        high_score_text = f"High Score: {high_score}"
        cv2.putText(
            frame,
            high_score_text,
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )
        
        # Draw difficulty
        difficulty_name = self.config.DIFFICULTY_SETTINGS[self.config.difficulty]['name']
        difficulty_text = f"Difficulty: {difficulty_name}"
        cv2.putText(
            frame,
            difficulty_text,
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )
        
        # Draw pause indicator
        if self.game.paused:
            pause_text = "PAUSED"
            text_size = cv2.getTextSize(pause_text, cv2.FONT_HERSHEY_BOLD, 2, 3)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = 50
            cv2.putText(
                frame,
                pause_text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_BOLD,
                2,
                (0, 255, 255),
                3
            )
        
        # Draw instructions
        instructions = [
            "Move your INDEX FINGER to control the snake",
            "Collect red food to grow and score points",
            "Press 'P' to pause | 'M' for menu | 'R' to restart | 'Q' to quit"
        ]
        
        y_pos = frame.shape[0] - 80
        for instruction in instructions:
            cv2.putText(
                frame,
                instruction,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                self.colors['text'],
                1
            )
            y_pos += 25
        
        # Draw game over message
        if self.game.is_game_over():
            game_over_text = "GAME OVER!"
            text_size = cv2.getTextSize(
                game_over_text,
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                3
            )[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (frame.shape[0] + text_size[1]) // 2
            
            # Draw background rectangle
            cv2.rectangle(
                frame,
                (text_x - 10, text_y - text_size[1] - 10),
                (text_x + text_size[0] + 10, text_y + 10),
                (0, 0, 0),
                -1
            )
            
            cv2.putText(
                frame,
                game_over_text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                self.colors['game_over'],
                3
            )
            
            # Show if new high score
            score = self.game.get_score()
            if score > 0 and score == self.config.get_high_score():
                new_high_text = "NEW HIGH SCORE!"
                cv2.putText(
                    frame,
                    new_high_text,
                    (text_x - 50, text_y + 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
    
    def run(self):
        """Main game loop"""
        print("Starting Hand-Gesture Controlled Snake Game...")
        print("Move your index finger to control the snake!")
        print("Press 'P' to pause, 'M' for menu, 'R' to restart, 'Q' to quit")
        
        while True:
            # Read frame from webcam
            success, frame = self.cap.read()
            if not success:
                print("Failed to read from webcam")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find hands in the frame
            frame, results = self.hand_tracker.find_hands(frame, draw=True)
            
            # Check for gestures
            if results.multi_hand_landmarks:
                gesture = self.gesture_recognizer.recognize_gesture(results.multi_hand_landmarks[0])
                if gesture == "peace":
                    # Peace sign toggles menu
                    if not self.menu_active:
                        self.menu_active = True
                        self.menu_type = 'main'
                        self.sound_manager.play_menu_sound()
            
            # Handle menu
            if self.menu_active:
                if self.menu_type == 'main':
                    frame = self.menu.show_main_menu(frame)
                elif self.menu_type == 'difficulty':
                    frame = self.menu.show_difficulty_menu(frame)
                elif self.menu_type == 'high_scores':
                    frame = self.menu.show_high_scores(frame)
            else:
                # Get index finger position
                finger_pos = self.hand_tracker.get_index_finger_position(frame, results)
                
                # Update game if finger is detected and game is not over or paused
                if finger_pos and not self.game.is_game_over() and not self.game.paused:
                    # Adjust finger position relative to game grid
                    adjusted_x = finger_pos[0] - self.game_x_offset
                    adjusted_y = finger_pos[1] - self.game_y_offset
                    
                    # Only update if finger is within game grid
                    grid_width, grid_height = self.game.get_grid_dimensions()
                    if 0 <= adjusted_x < grid_width and 0 <= adjusted_y < grid_height:
                        continues, ate_food = self.game.update_snake_position((adjusted_x, adjusted_y))
                        
                        # Play sound effects
                        if ate_food:
                            self.sound_manager.play_eat_sound()
                            # Check for milestone
                            if self.game.get_score() % 50 == 0:
                                self.sound_manager.play_level_up_sound()
                        
                        if not continues:
                            self.sound_manager.play_game_over_sound()
                            # Update high score
                            self.config.update_high_score(self.game.get_score())
                
                # Draw game elements
                self.draw_grid(frame)
                self.draw_food(frame)
                self.draw_snake(frame)
                
                # Draw finger marker if detected
                if finger_pos:
                    adjusted_x = finger_pos[0] - self.game_x_offset
                    adjusted_y = finger_pos[1] - self.game_y_offset
                    grid_width, grid_height = self.game.get_grid_dimensions()
                    if 0 <= adjusted_x < grid_width and 0 <= adjusted_y < grid_height:
                        self.draw_finger_marker(frame, (adjusted_x, adjusted_y))
                
                # Draw UI
                self.draw_ui(frame)
            
            # Display the frame
            cv2.imshow("Hand-Gesture Snake Game", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('r') or key == ord('R'):
                self.game.reset()
                self.sound_manager.play_menu_sound()
            elif key == ord('p') or key == ord('P'):
                if not self.menu_active:
                    self.game.toggle_pause()
                    self.sound_manager.play_menu_sound()
            elif key == ord('m') or key == ord('M'):
                self.menu_active = not self.menu_active
                if self.menu_active:
                    self.menu_type = 'main'
                    self.menu.selected_index = 0
                self.sound_manager.play_menu_sound()
            
            # Menu navigation
            if self.menu_active:
                if key == 82:  # Up arrow
                    self.menu.navigate_up()
                    self.sound_manager.play_menu_sound()
                elif key == 84:  # Down arrow
                    self.menu.navigate_down()
                    self.sound_manager.play_menu_sound()
                elif key == 13:  # Enter
                    action = None
                    if self.menu_type == 'main':
                        action = self.menu.select()
                    elif self.menu_type == 'difficulty':
                        difficulty = self.menu.select_difficulty()
                        if difficulty:
                            self.config.set_difficulty(difficulty)
                            # Update game speed
                            speed_delay = self.config.get_difficulty_setting('snake_speed_delay')
                            self.game.set_speed_delay(speed_delay)
                            self.menu_type = 'main'
                            self.menu.selected_index = 0
                        self.sound_manager.play_menu_sound()
                    elif self.menu_type == 'high_scores':
                        self.menu_type = 'main'
                        self.menu.selected_index = 0
                    
                    if action == 'resume':
                        self.menu_active = False
                    elif action == 'difficulty':
                        self.menu_type = 'difficulty'
                        self.menu.selected_index = 0
                    elif action == 'toggle_sound':
                        self.config.toggle_sound()
                        self.sound_manager.set_enabled(self.config.sound_enabled)
                        self.sound_manager.play_menu_sound()
                    elif action == 'high_scores':
                        self.menu_type = 'high_scores'
                    elif action == 'quit':
                        break
                    
                    if action:
                        self.sound_manager.play_menu_sound()
                elif key == 27:  # ESC
                    if self.menu_type in ['difficulty', 'high_scores']:
                        self.menu_type = 'main'
                        self.menu.selected_index = 0
                    else:
                        self.menu_active = False
                    self.sound_manager.play_menu_sound()
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        self.hand_tracker.close()
        cv2.destroyAllWindows()
        print("Game closed. Thanks for playing!")


def main():
    """Entry point"""
    try:
        game = SnakeVideoGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
