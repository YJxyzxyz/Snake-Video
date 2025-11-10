"""
Snake Game Module
Implements the classic Snake game logic
"""

import random
import numpy as np


class SnakeGame:
    """Classic Snake game with gesture control"""
    
    def __init__(self, grid_width=20, grid_height=15, cell_size=30):
        """
        Initialize the Snake game
        
        Args:
            grid_width: Number of cells in width
            grid_height: Number of cells in height
            cell_size: Size of each cell in pixels
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        
        # Initialize snake in the center
        center_x = grid_width // 2
        center_y = grid_height // 2
        self.snake = [(center_x, center_y)]
        
        # Generate first food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.game_over = False
        self.direction = (1, 0)  # Start moving right
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            food_x = random.randint(0, self.grid_width - 1)
            food_y = random.randint(0, self.grid_height - 1)
            
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)
    
    def update_snake_position(self, finger_pos):
        """
        Update snake based on finger position
        
        Args:
            finger_pos: (x, y) pixel coordinates of finger
            
        Returns:
            bool: True if game continues, False if game over
        """
        if self.game_over or finger_pos is None:
            return not self.game_over
        
        # Convert pixel coordinates to grid coordinates
        grid_x = finger_pos[0] // self.cell_size
        grid_y = finger_pos[1] // self.cell_size
        
        # Clamp to grid boundaries
        grid_x = max(0, min(grid_x, self.grid_width - 1))
        grid_y = max(0, min(grid_y, self.grid_height - 1))
        
        new_head = (grid_x, grid_y)
        
        # Check if the new position is the same as current head
        if len(self.snake) > 0 and new_head == self.snake[0]:
            return True  # No movement needed
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if snake ate food
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        # Check for collision with self (if snake length > 4 to avoid early game issues)
        if len(self.snake) > 4 and new_head in self.snake[1:]:
            self.game_over = True
            return False
        
        return True
    
    def reset(self):
        """Reset the game to initial state"""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [(center_x, center_y)]
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.direction = (1, 0)
    
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
