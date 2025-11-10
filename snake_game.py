"""
Snake Game Module
Implements the classic Snake game logic
"""

import random
import numpy as np
import time


class SnakeGame:
    """Classic Snake game with gesture control"""
    
    def __init__(self, grid_width=20, grid_height=15, cell_size=30, speed_delay=8):
        """
        Initialize the Snake game
        
        Args:
            grid_width: Number of cells in width
            grid_height: Number of cells in height
            cell_size: Size of each cell in pixels
            speed_delay: Delay between movements (lower = faster)
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.speed_delay = speed_delay
        
        # Initialize snake in the center
        center_x = grid_width // 2
        center_y = grid_height // 2
        self.snake = [(center_x, center_y)]
        
        # Generate first food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False
        self.direction = (1, 0)  # Start moving right
        self.last_move_time = time.time()
        self.frame_counter = 0
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            food_x = random.randint(0, self.grid_width - 1)
            food_y = random.randint(0, self.grid_height - 1)
            
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
        return self.paused
    
    def set_speed_delay(self, delay):
        """
        Set snake movement speed delay
        
        Args:
            delay: Delay between movements (lower = faster)
        """
        self.speed_delay = delay
    
    def update_snake_position(self, finger_pos):
        """
        Update snake based on finger position
        
        Args:
            finger_pos: (x, y) pixel coordinates of finger
            
        Returns:
            tuple: (continues, ate_food) - game continues and whether food was eaten
        """
        if self.game_over or self.paused or finger_pos is None:
            return (not self.game_over, False)
        
        # Speed control - only move every N frames
        self.frame_counter += 1
        if self.frame_counter < self.speed_delay:
            return (True, False)
        
        self.frame_counter = 0  # Reset counter
        
        # Convert pixel coordinates to grid coordinates
        grid_x = finger_pos[0] // self.cell_size
        grid_y = finger_pos[1] // self.cell_size
        
        # Clamp to grid boundaries
        grid_x = max(0, min(grid_x, self.grid_width - 1))
        grid_y = max(0, min(grid_y, self.grid_height - 1))
        
        new_head = (grid_x, grid_y)
        
        # Check if the new position is the same as current head
        if len(self.snake) > 0 and new_head == self.snake[0]:
            return (True, False)  # No movement needed
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if snake ate food
        ate_food = False
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            ate_food = True
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        # Check for collision with self (if snake length > 4 to avoid early game issues)
        if len(self.snake) > 4 and new_head in self.snake[1:]:
            self.game_over = True
            return (False, False)
        
        return (True, ate_food)
    
    def reset(self):
        """Reset the game to initial state"""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [(center_x, center_y)]
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.direction = (1, 0)
        self.frame_counter = 0
    
    def get_snake_head(self):
        """Get the position of snake head"""
        return self.snake[0] if self.snake else None
    
    def get_snake_body(self):
        """Get the snake body positions (excluding head)"""
        return self.snake[1:] if len(self.snake) > 1 else []
    
    def get_food_position(self):
        """Get the food position"""
        return self.food
    
    def get_score(self):
        """Get current score"""
        return self.score
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over
    
    def get_grid_dimensions(self):
        """Get grid dimensions in pixels"""
        return (self.grid_width * self.cell_size, 
                self.grid_height * self.cell_size)
