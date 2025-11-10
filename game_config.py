"""
Game Configuration Module
Manages game settings, difficulty levels, and high scores
"""

import json
import os
from enum import Enum


class Difficulty(Enum):
    """Game difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameConfig:
    """Manages game configuration and settings"""
    
    DIFFICULTY_SETTINGS = {
        Difficulty.EASY: {
            'name': 'Easy',
            'snake_speed_delay': 15,  # Higher delay = slower
            'score_multiplier': 1,
            'description': 'Slower snake, good for beginners'
        },
        Difficulty.MEDIUM: {
            'name': 'Medium',
            'snake_speed_delay': 8,
            'score_multiplier': 2,
            'description': 'Moderate speed, balanced gameplay'
        },
        Difficulty.HARD: {
            'name': 'Hard',
            'snake_speed_delay': 3,
            'score_multiplier': 3,
            'description': 'Fast snake, for experienced players'
        }
    }
    
    def __init__(self, config_file='game_data.json'):
        """
        Initialize game configuration
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.difficulty = Difficulty.MEDIUM
        self.sound_enabled = True
        self.high_scores = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    
                # Load difficulty
                difficulty_str = data.get('difficulty', 'medium')
                try:
                    self.difficulty = Difficulty(difficulty_str)
                except ValueError:
                    self.difficulty = Difficulty.MEDIUM
                
                # Load sound setting
                self.sound_enabled = data.get('sound_enabled', True)
                
                # Load high scores
                self.high_scores = data.get('high_scores', {})
                
            except Exception as e:
                print(f"Error loading config: {e}")
                self.reset_to_defaults()
        else:
            self.reset_to_defaults()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            data = {
                'difficulty': self.difficulty.value,
                'sound_enabled': self.sound_enabled,
                'high_scores': self.high_scores
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.difficulty = Difficulty.MEDIUM
        self.sound_enabled = True
        self.high_scores = {
            Difficulty.EASY.value: 0,
            Difficulty.MEDIUM.value: 0,
            Difficulty.HARD.value: 0
        }
    
    def get_difficulty_setting(self, key):
        """Get a specific difficulty setting"""
        return self.DIFFICULTY_SETTINGS[self.difficulty].get(key)
    
    def set_difficulty(self, difficulty):
        """
        Set game difficulty
        
        Args:
            difficulty: Difficulty enum value
        """
        if isinstance(difficulty, Difficulty):
            self.difficulty = difficulty
            self.save_config()
    
    def get_high_score(self, difficulty=None):
        """
        Get high score for a difficulty level
        
        Args:
            difficulty: Difficulty enum value (uses current if None)
            
        Returns:
            int: High score
        """
        if difficulty is None:
            difficulty = self.difficulty
        
        return self.high_scores.get(difficulty.value, 0)
    
    def update_high_score(self, score, difficulty=None):
        """
        Update high score if current score is higher
        
        Args:
            score: Current score
            difficulty: Difficulty enum value (uses current if None)
            
        Returns:
            bool: True if new high score was set
        """
        if difficulty is None:
            difficulty = self.difficulty
        
        current_high = self.get_high_score(difficulty)
        
        if score > current_high:
            self.high_scores[difficulty.value] = score
            self.save_config()
            return True
        
        return False
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        self.save_config()
        return self.sound_enabled
