"""
Flappy Hand Game Module
A Flappy Bird-style game controlled by hand height
"""

import random
import cv2


class Pipe:
    """Represents an obstacle pipe"""
    
    def __init__(self, x, gap_y, gap_size=200):
        """
        Initialize a pipe
        
        Args:
            x: X position
            gap_y: Center Y position of the gap
            gap_size: Size of the gap
        """
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.width = 80
        self.passed = False
        
    def update(self, speed=3):
        """Move pipe to the left"""
        self.x -= speed
        
    def draw(self, frame):
        """Draw the pipe on frame"""
        height = frame.shape[0]
        
        # Top pipe
        top_height = self.gap_y - self.gap_size // 2
        cv2.rectangle(frame, (self.x, 0), (self.x + self.width, top_height),
                     (0, 200, 0), -1)
        cv2.rectangle(frame, (self.x, 0), (self.x + self.width, top_height),
                     (0, 255, 0), 3)
        
        # Bottom pipe
        bottom_start = self.gap_y + self.gap_size // 2
        cv2.rectangle(frame, (self.x, bottom_start), (self.x + self.width, height),
                     (0, 200, 0), -1)
        cv2.rectangle(frame, (self.x, bottom_start), (self.x + self.width, height),
                     (0, 255, 0), 3)
        
    def is_off_screen(self):
        """Check if pipe is off screen"""
        return self.x + self.width < 0
    
    def check_collision(self, bird_x, bird_y, bird_radius):
        """
        Check if bird collides with pipe
        
        Args:
            bird_x: Bird X position
            bird_y: Bird Y position
            bird_radius: Bird radius
            
        Returns:
            bool: True if collision detected
        """
        # Check if bird is in pipe's X range
        if bird_x + bird_radius > self.x and bird_x - bird_radius < self.x + self.width:
            # Check if bird is outside the gap
            if bird_y - bird_radius < self.gap_y - self.gap_size // 2 or \
               bird_y + bird_radius > self.gap_y + self.gap_size // 2:
                return True
        
        return False


class FlappyHandGame:
    """Flappy Bird-style game controlled by hand height"""
    
    def __init__(self, width=1280, height=720):
        """
        Initialize the game
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.bird_x = 200
        self.bird_y = height // 2
        self.bird_radius = 25
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_timer = 0
        self.pipe_interval = 100  # Frames between pipes
        self.hand_target_y = height // 2
        self.smoothing_factor = 0.3  # Smoothing for bird movement
        
    def spawn_pipe(self):
        """Spawn a new pipe"""
        gap_y = random.randint(150, self.height - 150)
        pipe = Pipe(self.width, gap_y)
        self.pipes.append(pipe)
        
    def update(self, hand_y):
        """
        Update game state
        
        Args:
            hand_y: Y position of hand (controls bird height)
            
        Returns:
            int: Points earned this frame
        """
        if self.game_over:
            return 0
        
        points_earned = 0
        
        # Update bird position based on hand height
        if hand_y is not None:
            self.hand_target_y = hand_y
        
        # Smooth bird movement
        self.bird_y += (self.hand_target_y - self.bird_y) * self.smoothing_factor
        
        # Check boundaries
        if self.bird_y - self.bird_radius < 0:
            self.bird_y = self.bird_radius
            self.game_over = True
        elif self.bird_y + self.bird_radius > self.height:
            self.bird_y = self.height - self.bird_radius
            self.game_over = True
        
        # Spawn pipes
        self.pipe_timer += 1
        if self.pipe_timer >= self.pipe_interval:
            self.spawn_pipe()
            self.pipe_timer = 0
        
        # Update pipes
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.update()
            
            # Check collision
            if pipe.check_collision(self.bird_x, self.bird_y, self.bird_radius):
                self.game_over = True
            
            # Check if passed
            if not pipe.passed and pipe.x + pipe.width < self.bird_x:
                pipe.passed = True
                self.score += 1
                points_earned += 1
            
            # Remove off-screen pipes
            if pipe.is_off_screen():
                pipes_to_remove.append(pipe)
        
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
        
        return points_earned
    
    def draw(self, frame):
        """Draw game elements on frame"""
        # Draw background gradient
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (100, 200, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(frame)
        
        # Draw bird
        cv2.circle(frame, (self.bird_x, int(self.bird_y)), self.bird_radius,
                  (0, 255, 255), -1)
        cv2.circle(frame, (self.bird_x, int(self.bird_y)), self.bird_radius,
                  (255, 255, 255), 3)
        
        # Draw eye
        eye_x = self.bird_x + 10
        eye_y = int(self.bird_y - 5)
        cv2.circle(frame, (eye_x, eye_y), 5, (0, 0, 0), -1)
        
        # Draw beak
        beak_points = [
            (self.bird_x + self.bird_radius, int(self.bird_y)),
            (self.bird_x + self.bird_radius + 15, int(self.bird_y - 5)),
            (self.bird_x + self.bird_radius + 15, int(self.bird_y + 5))
        ]
        cv2.fillPoly(frame, [np.array(beak_points)], (0, 165, 255))
        
        # Draw score
        cv2.putText(frame, f"Score: {self.score}", (10, 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)
        
        # Draw instructions
        if not self.game_over:
            cv2.putText(frame, "Move your hand UP and DOWN to control the bird!",
                       (10, self.height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw game over
        if self.game_over:
            overlay = frame.copy()
            cv2.rectangle(overlay, (self.width//4, self.height//3),
                         (3*self.width//4, 2*self.height//3), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            game_over_text = "GAME OVER!"
            score_text = f"Final Score: {self.score}"
            
            cv2.putText(frame, game_over_text, (self.width//4 + 80, self.height//2 - 30),
                       cv2.FONT_HERSHEY_BOLD, 1.5, (0, 0, 255), 3)
            cv2.putText(frame, score_text, (self.width//4 + 120, self.height//2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        return frame
    
    def reset(self):
        """Reset the game"""
        self.bird_y = self.height // 2
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_timer = 0
        self.hand_target_y = self.height // 2


# Import numpy for drawing
import numpy as np
