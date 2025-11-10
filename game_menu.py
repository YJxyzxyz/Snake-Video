"""
Game Menu Module
Provides menu system for game settings and options
"""

import cv2
from game_config import Difficulty


class GameMenu:
    """Manages game menus and UI"""
    
    def __init__(self, config):
        """
        Initialize game menu
        
        Args:
            config: GameConfig instance
        """
        self.config = config
        self.menu_items = []
        self.selected_index = 0
        self.menu_active = False
        self.menu_type = None
        
    def show_main_menu(self, frame):
        """
        Draw main menu on frame
        
        Args:
            frame: Video frame to draw on
            
        Returns:
            frame: Frame with menu drawn
        """
        overlay = frame.copy()
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(overlay, (w//4, h//4), (3*w//4, 3*h//4), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Menu title
        title = "GAME MENU"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_BOLD, 1.5, 3)[0]
        title_x = (w - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, h//4 + 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)
        
        # Menu options
        self.menu_items = [
            "Resume Game",
            "Change Difficulty",
            f"Sound: {'ON' if self.config.sound_enabled else 'OFF'}",
            "High Scores",
            "Quit"
        ]
        
        y_start = h//4 + 120
        for i, item in enumerate(self.menu_items):
            color = (0, 255, 255) if i == self.selected_index else (200, 200, 200)
            prefix = "> " if i == self.selected_index else "  "
            text = prefix + item
            cv2.putText(frame, text, (w//4 + 50, y_start + i * 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Instructions
        instructions = "Use UP/DOWN arrows to navigate | ENTER to select | ESC to close"
        inst_size = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        inst_x = (w - inst_size[0]) // 2
        cv2.putText(frame, instructions, (inst_x, 3*h//4 - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        
        return frame
    
    def show_difficulty_menu(self, frame):
        """
        Draw difficulty selection menu
        
        Args:
            frame: Video frame to draw on
            
        Returns:
            frame: Frame with menu drawn
        """
        overlay = frame.copy()
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(overlay, (w//4, h//4), (3*w//4, 3*h//4), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Menu title
        title = "SELECT DIFFICULTY"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_BOLD, 1.2, 2)[0]
        title_x = (w - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, h//4 + 50),
                   cv2.FONT_HERSHEY_BOLD, 1.2, (255, 255, 255), 2)
        
        # Difficulty options
        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        y_start = h//4 + 120
        
        for i, diff in enumerate(difficulties):
            settings = self.config.DIFFICULTY_SETTINGS[diff]
            is_current = diff == self.config.difficulty
            is_selected = i == self.selected_index
            
            color = (0, 255, 0) if is_current else ((0, 255, 255) if is_selected else (200, 200, 200))
            prefix = "> " if is_selected else "  "
            suffix = " (Current)" if is_current else ""
            
            text = f"{prefix}{settings['name']}{suffix}"
            cv2.putText(frame, text, (w//4 + 50, y_start + i * 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Description
            desc = settings['description']
            cv2.putText(frame, desc, (w//4 + 70, y_start + i * 80 + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        
        return frame
    
    def show_high_scores(self, frame):
        """
        Draw high scores menu
        
        Args:
            frame: Video frame to draw on
            
        Returns:
            frame: Frame with high scores drawn
        """
        overlay = frame.copy()
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(overlay, (w//4, h//4), (3*w//4, 3*h//4), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Title
        title = "HIGH SCORES"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_BOLD, 1.5, 3)[0]
        title_x = (w - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, h//4 + 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 0), 3)
        
        # High scores
        y_start = h//4 + 120
        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        
        for i, diff in enumerate(difficulties):
            settings = self.config.DIFFICULTY_SETTINGS[diff]
            score = self.config.get_high_score(diff)
            
            text = f"{settings['name']}: {score}"
            cv2.putText(frame, text, (w//4 + 80, y_start + i * 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # Instructions
        instructions = "Press ESC or ENTER to return"
        inst_size = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        inst_x = (w - inst_size[0]) // 2
        cv2.putText(frame, instructions, (inst_x, 3*h//4 - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        return frame
    
    def navigate_up(self):
        """Move selection up in menu"""
        if self.selected_index > 0:
            self.selected_index -= 1
    
    def navigate_down(self):
        """Move selection down in menu"""
        if self.menu_items and self.selected_index < len(self.menu_items) - 1:
            self.selected_index += 1
    
    def select(self):
        """
        Select current menu item
        
        Returns:
            str: Action to perform
        """
        if not self.menu_items or self.selected_index >= len(self.menu_items):
            return None
        
        selected = self.menu_items[self.selected_index]
        
        if "Resume" in selected:
            return "resume"
        elif "Difficulty" in selected:
            return "difficulty"
        elif "Sound" in selected:
            return "toggle_sound"
        elif "High Scores" in selected:
            return "high_scores"
        elif "Quit" in selected:
            return "quit"
        
        return None
    
    def select_difficulty(self):
        """
        Select difficulty level
        
        Returns:
            Difficulty: Selected difficulty or None
        """
        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        if 0 <= self.selected_index < len(difficulties):
            return difficulties[self.selected_index]
        return None
