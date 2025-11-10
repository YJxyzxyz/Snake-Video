"""
Rock Paper Scissors Game Module
Play Rock-Paper-Scissors against the computer using hand gestures
"""

import random
import time
import cv2
import numpy as np


class RockPaperScissorsGame:
    """Rock-Paper-Scissors game with gesture recognition"""
    
    GESTURES = {
        'rock': '✊ Rock',
        'paper': '✋ Paper',
        'scissors': '✌️ Scissors'
    }
    
    def __init__(self, width=1280, height=720):
        """
        Initialize the game
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_state = 'waiting'  # waiting, countdown, show_result
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.countdown = 3
        self.countdown_timer = 0
        self.result_timer = 0
        self.result_display_time = 90  # frames
        
    def detect_gesture(self, gesture_name):
        """
        Set player's gesture choice
        
        Args:
            gesture_name: Name of detected gesture
        """
        if self.game_state == 'waiting':
            if gesture_name == 'fist':
                self.start_round('rock')
            elif gesture_name == 'open_palm':
                self.start_round('paper')
            elif gesture_name == 'peace':
                self.start_round('scissors')
    
    def start_round(self, player_gesture):
        """
        Start a new round with player's choice
        
        Args:
            player_gesture: Player's gesture choice
        """
        self.player_choice = player_gesture
        self.game_state = 'countdown'
        self.countdown = 3
        self.countdown_timer = 0
    
    def update(self):
        """Update game state"""
        if self.game_state == 'countdown':
            self.countdown_timer += 1
            if self.countdown_timer >= 30:  # 30 frames = ~1 second
                self.countdown -= 1
                self.countdown_timer = 0
                
                if self.countdown == 0:
                    # Make computer choice
                    self.computer_choice = random.choice(['rock', 'paper', 'scissors'])
                    self.result = self._determine_winner()
                    self.game_state = 'show_result'
                    self.result_timer = 0
                    self.rounds_played += 1
                    
                    # Update scores
                    if self.result == 'win':
                        self.player_score += 1
                    elif self.result == 'lose':
                        self.computer_score += 1
        
        elif self.game_state == 'show_result':
            self.result_timer += 1
            if self.result_timer >= self.result_display_time:
                self.game_state = 'waiting'
                self.player_choice = None
                self.computer_choice = None
                self.result = None
    
    def _determine_winner(self):
        """
        Determine the winner of the round
        
        Returns:
            str: 'win', 'lose', or 'tie'
        """
        if self.player_choice == self.computer_choice:
            return 'tie'
        
        winning_combinations = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }
        
        if winning_combinations[self.player_choice] == self.computer_choice:
            return 'win'
        else:
            return 'lose'
    
    def draw(self, frame):
        """Draw game elements on frame"""
        # Draw background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (50, 50, 50), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw title
        title = "ROCK PAPER SCISSORS"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_BOLD, 1.5, 3)[0]
        title_x = (self.width - title_size[0]) // 2
        cv2.putText(frame, title, (title_x, 60),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)
        
        # Draw scores
        score_text = f"You: {self.player_score}  |  Computer: {self.computer_score}"
        score_size = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        score_x = (self.width - score_size[0]) // 2
        cv2.putText(frame, score_text, (score_x, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Draw game state
        if self.game_state == 'waiting':
            self._draw_waiting_state(frame)
        elif self.game_state == 'countdown':
            self._draw_countdown(frame)
        elif self.game_state == 'show_result':
            self._draw_result(frame)
        
        # Draw instructions
        instructions = [
            "Show your gesture to play:",
            "FIST (Rock) | OPEN PALM (Paper) | PEACE SIGN (Scissors)",
            "Press R to reset scores | ESC for menu | Q to quit"
        ]
        y = self.height - 100
        for instruction in instructions:
            inst_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
            inst_x = (self.width - inst_size[0]) // 2
            cv2.putText(frame, instruction, (inst_x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            y += 30
        
        return frame
    
    def _draw_waiting_state(self, frame):
        """Draw waiting for player gesture"""
        text = "Show your gesture!"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_BOLD, 1.5, 3)[0]
        text_x = (self.width - text_size[0]) // 2
        cv2.putText(frame, text, (text_x, self.height // 2),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (0, 255, 0), 3)
        
        # Draw gesture icons
        gestures_text = "✊ Rock    ✋ Paper    ✌️ Scissors"
        gestures_size = cv2.getTextSize(gestures_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
        gestures_x = (self.width - gestures_size[0]) // 2
        cv2.putText(frame, gestures_text, (gestures_x, self.height // 2 + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
    def _draw_countdown(self, frame):
        """Draw countdown"""
        if self.countdown > 0:
            countdown_text = str(self.countdown)
            text_size = cv2.getTextSize(countdown_text, cv2.FONT_HERSHEY_BOLD, 5, 10)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = (self.height + text_size[1]) // 2
            cv2.putText(frame, countdown_text, (text_x, text_y),
                       cv2.FONT_HERSHEY_BOLD, 5, (255, 255, 0), 10)
        else:
            shoot_text = "SHOOT!"
            text_size = cv2.getTextSize(shoot_text, cv2.FONT_HERSHEY_BOLD, 3, 6)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = (self.height + text_size[1]) // 2
            cv2.putText(frame, shoot_text, (text_x, text_y),
                       cv2.FONT_HERSHEY_BOLD, 3, (0, 255, 255), 6)
    
    def _draw_result(self, frame):
        """Draw round result"""
        # Draw player choice
        player_text = f"You: {self.GESTURES[self.player_choice]}"
        cv2.putText(frame, player_text, (100, self.height // 2 - 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)
        
        # Draw computer choice
        computer_text = f"Computer: {self.GESTURES[self.computer_choice]}"
        cv2.putText(frame, computer_text, (self.width - 500, self.height // 2 - 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)
        
        # Draw result
        if self.result == 'win':
            result_text = "YOU WIN!"
            color = (0, 255, 0)
        elif self.result == 'lose':
            result_text = "YOU LOSE!"
            color = (0, 0, 255)
        else:
            result_text = "TIE!"
            color = (255, 255, 0)
        
        result_size = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_BOLD, 2.5, 5)[0]
        result_x = (self.width - result_size[0]) // 2
        cv2.putText(frame, result_text, (result_x, self.height // 2 + 50),
                   cv2.FONT_HERSHEY_BOLD, 2.5, color, 5)
    
    def reset(self):
        """Reset scores and game state"""
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_state = 'waiting'
        self.player_choice = None
        self.computer_choice = None
        self.result = None
