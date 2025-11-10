"""
Fruit Slicer Game Module
A Fruit Ninja-style game controlled by hand gestures
"""

import random
import time
import math
import cv2


class Fruit:
    """Represents a falling fruit"""
    
    def __init__(self, x, y, fruit_type, velocity_y, velocity_x=0):
        """
        Initialize a fruit
        
        Args:
            x: Initial x position
            y: Initial y position
            fruit_type: Type of fruit (0-4)
            velocity_y: Vertical velocity
            velocity_x: Horizontal velocity
        """
        self.x = x
        self.y = y
        self.fruit_type = fruit_type
        self.velocity_y = velocity_y
        self.velocity_x = velocity_x
        self.sliced = False
        self.radius = 30
        
        # Fruit colors (BGR)
        self.colors = [
            (0, 0, 255),    # Red - Apple
            (0, 165, 255),  # Orange
            (0, 255, 255),  # Yellow - Banana
            (0, 255, 0),    # Green - Kiwi
            (255, 0, 255),  # Purple - Grape
        ]
        
    def update(self, gravity=0.5):
        """Update fruit position"""
        self.velocity_y += gravity
        self.y += self.velocity_y
        self.x += self.velocity_x
        
    def draw(self, frame):
        """Draw the fruit on frame"""
        if not self.sliced:
            color = self.colors[self.fruit_type]
            cv2.circle(frame, (int(self.x), int(self.y)), self.radius, color, -1)
            cv2.circle(frame, (int(self.x), int(self.y)), self.radius, (255, 255, 255), 2)
        
    def is_off_screen(self, height):
        """Check if fruit is off screen"""
        return self.y > height + 50
    
    def check_slice(self, finger_x, finger_y, prev_x, prev_y):
        """
        Check if finger path slices this fruit
        
        Args:
            finger_x: Current finger x
            finger_y: Current finger y
            prev_x: Previous finger x
            prev_y: Previous finger y
            
        Returns:
            bool: True if sliced
        """
        if self.sliced:
            return False
        
        # Calculate distance from line segment to circle
        distance = self._point_to_segment_distance(
            self.x, self.y, finger_x, finger_y, prev_x, prev_y
        )
        
        if distance < self.radius + 20:  # 20 pixel tolerance
            self.sliced = True
            return True
        
        return False
    
    def _point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        """Calculate distance from point to line segment"""
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        projection_x = x1 + t * dx
        projection_y = y1 + t * dy
        
        return math.sqrt((px - projection_x) ** 2 + (py - projection_y) ** 2)


class FruitSlicerGame:
    """Fruit Ninja-style game with hand gestures"""
    
    def __init__(self, width=1280, height=720):
        """
        Initialize the game
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = 60  # Frames between spawns
        self.prev_finger_pos = None
        self.finger_trail = []
        self.max_trail_length = 10
        
    def spawn_fruit(self):
        """Spawn a new fruit"""
        x = random.randint(100, self.width - 100)
        y = self.height - 50
        fruit_type = random.randint(0, 4)
        velocity_y = random.uniform(-15, -10)
        velocity_x = random.uniform(-3, 3)
        
        fruit = Fruit(x, y, fruit_type, velocity_y, velocity_x)
        self.fruits.append(fruit)
    
    def update(self, finger_pos):
        """
        Update game state
        
        Args:
            finger_pos: (x, y) position of finger
            
        Returns:
            int: Points earned this frame
        """
        if self.game_over:
            return 0
        
        points_earned = 0
        
        # Update finger trail
        if finger_pos:
            self.finger_trail.append(finger_pos)
            if len(self.finger_trail) > self.max_trail_length:
                self.finger_trail.pop(0)
        
        # Spawn fruits
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_fruit()
            self.spawn_timer = 0
            # Increase difficulty over time
            self.spawn_interval = max(30, self.spawn_interval - 1)
        
        # Update fruits
        fruits_to_remove = []
        for fruit in self.fruits:
            fruit.update()
            
            # Check if sliced
            if finger_pos and self.prev_finger_pos and not fruit.sliced:
                if fruit.check_slice(finger_pos[0], finger_pos[1],
                                    self.prev_finger_pos[0], self.prev_finger_pos[1]):
                    self.score += 10
                    points_earned += 10
            
            # Check if off screen
            if fruit.is_off_screen(self.height):
                if not fruit.sliced:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                fruits_to_remove.append(fruit)
        
        # Remove off-screen fruits
        for fruit in fruits_to_remove:
            self.fruits.remove(fruit)
        
        self.prev_finger_pos = finger_pos
        
        return points_earned
    
    def draw(self, frame):
        """Draw game elements on frame"""
        # Draw fruits
        for fruit in self.fruits:
            fruit.draw(frame)
        
        # Draw finger trail
        if len(self.finger_trail) > 1:
            for i in range(1, len(self.finger_trail)):
                thickness = int(5 * (i / len(self.finger_trail)))
                cv2.line(frame, self.finger_trail[i-1], self.finger_trail[i],
                        (0, 255, 255), max(1, thickness))
        
        # Draw score
        cv2.putText(frame, f"Score: {self.score}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Draw lives
        for i in range(self.lives):
            cv2.circle(frame, (self.width - 40 - i * 50, 30), 15, (0, 0, 255), -1)
        
        # Draw instructions
        if not self.game_over:
            cv2.putText(frame, "Slice the fruits! Don't let them fall!", (10, self.height - 20),
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
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.prev_finger_pos = None
        self.finger_trail = []
