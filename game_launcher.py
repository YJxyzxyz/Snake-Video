"""
Game Launcher Module
Main entry point that allows selecting and switching between different games
"""

import cv2
import numpy as np
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from snake_game import SnakeGame
from fruit_slicer_game import FruitSlicerGame
from flappy_hand_game import FlappyHandGame
from rock_paper_scissors_game import RockPaperScissorsGame
from air_drawing_game import AirDrawingGame
from game_config import GameConfig, Difficulty
from sound_manager import SoundManager
from game_menu import GameMenu


class GameLauncher:
    """Main application that manages multiple games"""
    
    GAMES = {
        'snake': 'Snake Game',
        'fruit_slicer': 'Fruit Slicer',
        'flappy_hand': 'Flappy Hand',
        'rps': 'Rock Paper Scissors',
        'air_drawing': 'Air Drawing',
    }
    
    def __init__(self):
        """Initialize the game launcher"""
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Get actual dimensions
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize hand tracker
        self.hand_tracker = HandTracker(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Initialize gesture recognizer
        self.gesture_recognizer = GestureRecognizer()
        
        # Initialize config and sound
        self.config = GameConfig()
        self.sound_manager = SoundManager(self.config.sound_enabled)
        
        # Initialize menu
        self.menu = GameMenu(self.config)
        
        # Game state
        self.current_game = None
        self.game_instance = None
        self.show_game_select = True
        self.selected_game_index = 0
        self.in_menu = False
        
        # Colors (BGR format)
        self.colors = {
            'text': (255, 255, 255),
            'selected': (0, 255, 255),
            'normal': (200, 200, 200),
            'bg': (30, 30, 30),
        }
        
    def show_game_selection(self, frame):
        """Draw game selection menu"""
        overlay = frame.copy()
        
        # Semi-transparent background
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Title
        title = "GESTURE GAME COLLECTION"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_BOLD, 2, 3)[0]
        title_x = (self.width - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, 100),
                   cv2.FONT_HERSHEY_BOLD, 2, (0, 255, 255), 3)
        
        # Subtitle
        subtitle = "Select a game to play"
        subtitle_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        subtitle_x = (self.width - subtitle_size[0]) // 2
        cv2.putText(frame, subtitle, (subtitle_x, 160),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Game list
        game_keys = list(self.GAMES.keys())
        y_start = 250
        
        for i, game_key in enumerate(game_keys):
            game_name = self.GAMES[game_key]
            color = self.colors['selected'] if i == self.selected_game_index else self.colors['normal']
            prefix = "> " if i == self.selected_game_index else "  "
            
            text = f"{prefix}{i + 1}. {game_name}"
            cv2.putText(frame, text, (self.width // 4, y_start + i * 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
            
            # Description
            descriptions = {
                'snake': 'Classic snake game - Point finger to move',
                'fruit_slicer': 'Slice falling fruits - Swipe with finger',
                'flappy_hand': 'Avoid pipes - Move hand up/down',
                'rps': 'Play against computer - Show hand gestures',
                'air_drawing': 'Draw in the air - Use your finger as brush',
            }
            desc = descriptions.get(game_key, '')
            cv2.putText(frame, desc, (self.width // 4 + 40, y_start + i * 80 + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Instructions
        instructions = [
            "Use NUMBER keys (1-5) to select a game",
            "Press ENTER to start selected game",
            "Press ESC to show this menu during gameplay",
            "Press Q to quit"
        ]
        
        y_inst = self.height - 150
        for instruction in instructions:
            cv2.putText(frame, instruction, (50, y_inst),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            y_inst += 30
        
        return frame
    
    def start_game(self, game_key):
        """Start a specific game"""
        self.current_game = game_key
        self.show_game_select = False
        
        if game_key == 'snake':
            # Use difficulty settings from config
            speed_delay = self.config.get_difficulty_setting('snake_speed_delay')
            self.game_instance = SnakeGame(
                grid_width=20, 
                grid_height=15, 
                cell_size=30,
                speed_delay=speed_delay
            )
        elif game_key == 'fruit_slicer':
            self.game_instance = FruitSlicerGame(self.width, self.height)
        elif game_key == 'flappy_hand':
            self.game_instance = FlappyHandGame(self.width, self.height)
        elif game_key == 'rps':
            self.game_instance = RockPaperScissorsGame(self.width, self.height)
        elif game_key == 'air_drawing':
            self.game_instance = AirDrawingGame(self.width, self.height)
    
    def run_snake_game(self, frame, results):
        """Run snake game logic"""
        # Import snake game rendering
        from main import SnakeVideoGame
        
        # Get finger position
        finger_pos = self.hand_tracker.get_index_finger_position(frame, results)
        
        # Update game
        if finger_pos and not self.game_instance.is_game_over():
            # Adjust finger position relative to game grid
            game_x_offset = 50
            game_y_offset = 50
            adjusted_x = finger_pos[0] - game_x_offset
            adjusted_y = finger_pos[1] - game_y_offset
            
            grid_width, grid_height = self.game_instance.get_grid_dimensions()
            if 0 <= adjusted_x < grid_width and 0 <= adjusted_y < grid_height:
                continues, ate_food = self.game_instance.update_snake_position((adjusted_x, adjusted_y))
                
                if ate_food:
                    self.sound_manager.play_eat_sound()
                    # Check for high score milestone
                    if self.game_instance.get_score() % 50 == 0:
                        self.sound_manager.play_level_up_sound()
                
                if not continues:
                    self.sound_manager.play_game_over_sound()
                    # Update high score
                    is_new_high = self.config.update_high_score(
                        self.game_instance.get_score()
                    )
        
        # Draw game (simplified version)
        self._draw_snake_game(frame, finger_pos)
        
        return frame
    
    def _draw_snake_game(self, frame, finger_pos):
        """Draw snake game elements on frame"""
        game_x_offset = 50
        game_y_offset = 50
        cell_size = self.game_instance.cell_size
        
        # Draw grid
        grid_width, grid_height = self.game_instance.get_grid_dimensions()
        cv2.rectangle(frame, (game_x_offset, game_y_offset),
                     (game_x_offset + grid_width, game_y_offset + grid_height),
                     (30, 30, 30), -1)
        
        # Draw grid lines
        for i in range(self.game_instance.grid_width + 1):
            x = game_x_offset + i * cell_size
            cv2.line(frame, (x, game_y_offset), (x, game_y_offset + grid_height),
                    (50, 50, 50), 1)
        for i in range(self.game_instance.grid_height + 1):
            y = game_y_offset + i * cell_size
            cv2.line(frame, (game_x_offset, y), (game_x_offset + grid_width, y),
                    (50, 50, 50), 1)
        
        # Draw food
        food = self.game_instance.get_food_position()
        food_x = game_x_offset + food[0] * cell_size + cell_size // 2
        food_y = game_y_offset + food[1] * cell_size + cell_size // 2
        cv2.circle(frame, (food_x, food_y), cell_size // 3, (0, 0, 255), -1)
        
        # Draw snake
        head = self.game_instance.get_snake_head()
        if head:
            x = game_x_offset + head[0] * cell_size
            y = game_y_offset + head[1] * cell_size
            cv2.rectangle(frame, (x + 2, y + 2), (x + cell_size - 2, y + cell_size - 2),
                         (0, 255, 0), -1)
        
        for segment in self.game_instance.get_snake_body():
            x = game_x_offset + segment[0] * cell_size
            y = game_y_offset + segment[1] * cell_size
            cv2.rectangle(frame, (x + 3, y + 3), (x + cell_size - 3, y + cell_size - 3),
                         (0, 200, 0), -1)
        
        # Draw UI
        score = self.game_instance.get_score()
        high_score = self.config.get_high_score()
        difficulty = self.config.DIFFICULTY_SETTINGS[self.config.difficulty]['name']
        
        cv2.putText(frame, f"Score: {score}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"High Score: {high_score}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Difficulty: {difficulty}", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Instructions
        cv2.putText(frame, "R: Restart | M: Menu | ESC: Game Select | Q: Quit",
                   (10, self.height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Game over message
        if self.game_instance.is_game_over():
            overlay = frame.copy()
            cv2.rectangle(overlay, (self.width//4, self.height//3),
                         (3*self.width//4, 2*self.height//3), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            cv2.putText(frame, "GAME OVER!", (self.width//4 + 100, self.height//2 - 20),
                       cv2.FONT_HERSHEY_BOLD, 1.5, (0, 0, 255), 3)
            cv2.putText(frame, f"Score: {score}", (self.width//4 + 150, self.height//2 + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    def run_fruit_slicer(self, frame, results):
        """Run fruit slicer game logic"""
        # Get finger position
        finger_pos = self.hand_tracker.get_index_finger_position(frame, results)
        
        # Update game
        points = self.game_instance.update(finger_pos)
        if points > 0:
            self.sound_manager.play_eat_sound()
        
        if self.game_instance.game_over:
            self.sound_manager.play_game_over_sound()
        
        # Draw game
        frame = self.game_instance.draw(frame)
        
        # Instructions
        cv2.putText(frame, "R: Restart | ESC: Game Select | Q: Quit",
                   (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def run_flappy_hand(self, frame, results):
        """Run flappy hand game logic"""
        # Get hand position (use palm center for better control)
        finger_pos = self.hand_tracker.get_index_finger_position(frame, results)
        hand_y = finger_pos[1] if finger_pos else None
        
        # Update game
        points = self.game_instance.update(hand_y)
        if points > 0:
            self.sound_manager.play_eat_sound()
        
        if self.game_instance.game_over:
            self.sound_manager.play_game_over_sound()
        
        # Draw game
        frame = self.game_instance.draw(frame)
        
        # Instructions
        cv2.putText(frame, "R: Restart | ESC: Game Select | Q: Quit",
                   (10, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return frame
    
    def run_rock_paper_scissors(self, frame, results):
        """Run rock paper scissors game logic"""
        # Recognize gesture
        if results.multi_hand_landmarks:
            gesture = self.gesture_recognizer.recognize_gesture(results.multi_hand_landmarks[0])
            if gesture:
                self.game_instance.detect_gesture(gesture)
        
        # Update game
        self.game_instance.update()
        
        # Draw game
        frame = self.game_instance.draw(frame)
        
        return frame
    
    def run_air_drawing(self, frame, results):
        """Run air drawing game logic"""
        # Get finger position
        finger_pos = self.hand_tracker.get_index_finger_position(frame, results)
        
        # Check if drawing (all fingers extended means not drawing)
        is_drawing = False
        if results.multi_hand_landmarks:
            gesture = self.gesture_recognizer.recognize_gesture(results.multi_hand_landmarks[0])
            # Draw only when pointing (index finger up)
            is_drawing = (gesture == 'point')
        
        # Update drawing
        self.game_instance.update(finger_pos, is_drawing)
        
        # Draw UI
        frame = self.game_instance.draw_ui(frame)
        
        return frame
    
    def run(self):
        """Main game loop"""
        print("Starting Gesture Game Collection...")
        print("Use number keys to select a game, or press Q to quit")
        
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
            
            # Show game selection menu
            if self.show_game_select:
                frame = self.show_game_selection(frame)
            elif self.in_menu:
                # Show game menu
                frame = self.menu.show_main_menu(frame)
            else:
                # Run current game
                if self.current_game == 'snake':
                    frame = self.run_snake_game(frame, results)
                elif self.current_game == 'fruit_slicer':
                    frame = self.run_fruit_slicer(frame, results)
                elif self.current_game == 'flappy_hand':
                    frame = self.run_flappy_hand(frame, results)
                elif self.current_game == 'rps':
                    frame = self.run_rock_paper_scissors(frame, results)
                elif self.current_game == 'air_drawing':
                    frame = self.run_air_drawing(frame, results)
            
            # Display the frame
            cv2.imshow("Gesture Game Collection", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == 27:  # ESC key
                if self.in_menu:
                    self.in_menu = False
                else:
                    self.show_game_select = True
                    self.in_menu = False
            elif key == ord('r') or key == ord('R'):
                if self.game_instance:
                    self.game_instance.reset()
            elif key == ord('m') or key == ord('M'):
                if not self.show_game_select:
                    self.in_menu = not self.in_menu
            
            # Game selection with number keys
            if self.show_game_select:
                game_keys = list(self.GAMES.keys())
                if key == ord('1') and len(game_keys) > 0:
                    self.start_game(game_keys[0])
                elif key == ord('2') and len(game_keys) > 1:
                    self.start_game(game_keys[1])
                elif key == ord('3') and len(game_keys) > 2:
                    self.start_game(game_keys[2])
                elif key == ord('4') and len(game_keys) > 3:
                    self.start_game(game_keys[3])
                elif key == ord('5') and len(game_keys) > 4:
                    self.start_game(game_keys[4])
                elif key == 13:  # Enter key
                    self.start_game(game_keys[self.selected_game_index])
                elif key == 82 or key == 0:  # Up arrow
                    self.selected_game_index = (self.selected_game_index - 1) % len(game_keys)
                elif key == 84 or key == 1:  # Down arrow
                    self.selected_game_index = (self.selected_game_index + 1) % len(game_keys)
            
            # Game-specific controls
            if not self.show_game_select and self.current_game == 'air_drawing':
                if key == ord('c') or key == ord('C'):
                    self.game_instance.next_color()
                elif key == ord('t') or key == ord('T'):
                    self.game_instance.toggle_tool()
                elif key == ord('=') or key == ord('+'):
                    self.game_instance.increase_brush_size()
                elif key == ord('-') or key == ord('_'):
                    self.game_instance.decrease_brush_size()
                elif key == ord('u') or key == ord('U'):
                    self.game_instance.undo()
                elif key == ord('x') or key == ord('X'):
                    self.game_instance.clear_canvas()
                elif key == ord('h') or key == ord('H'):
                    self.game_instance.toggle_help()
                elif key == ord('p') or key == ord('P'):
                    self.game_instance.toggle_palette()
        
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
        launcher = GameLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
