"""
Air Drawing Game Module
Draw in the air using your index finger
"""

import cv2
import numpy as np
from collections import deque


class AirDrawingGame:
    """Drawing application using finger tracking"""
    
    def __init__(self, width=1280, height=720):
        """
        Initialize the drawing game
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        
        # Drawing canvas
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.canvas.fill(255)  # White background
        
        # Drawing state
        self.drawing = False
        self.prev_point = None
        self.current_color = (0, 0, 255)  # Red (BGR)
        self.brush_size = 5
        self.eraser_size = 30
        self.tool = 'pen'  # pen, eraser, none
        
        # Drawing history for undo
        self.history = []
        self.max_history = 20
        
        # Color palette
        self.colors = [
            ((0, 0, 255), 'Red'),
            ((0, 255, 0), 'Green'),
            ((255, 0, 0), 'Blue'),
            ((0, 255, 255), 'Yellow'),
            ((255, 0, 255), 'Magenta'),
            ((255, 255, 0), 'Cyan'),
            ((0, 0, 0), 'Black'),
            ((128, 128, 128), 'Gray'),
        ]
        
        self.current_color_index = 0
        
        # UI elements
        self.show_palette = False
        self.show_help = True
        
    def save_to_history(self):
        """Save current canvas to history"""
        self.history.append(self.canvas.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def undo(self):
        """Undo last drawing action"""
        if self.history:
            self.canvas = self.history.pop()
    
    def clear_canvas(self):
        """Clear the entire canvas"""
        self.save_to_history()
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.canvas.fill(255)
    
    def set_color(self, color_index):
        """
        Set drawing color
        
        Args:
            color_index: Index in color palette
        """
        if 0 <= color_index < len(self.colors):
            self.current_color_index = color_index
            self.current_color = self.colors[color_index][0]
    
    def next_color(self):
        """Switch to next color"""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.current_color = self.colors[self.current_color_index][0]
    
    def increase_brush_size(self):
        """Increase brush size"""
        if self.tool == 'pen':
            self.brush_size = min(self.brush_size + 2, 30)
        else:
            self.eraser_size = min(self.eraser_size + 5, 100)
    
    def decrease_brush_size(self):
        """Decrease brush size"""
        if self.tool == 'pen':
            self.brush_size = max(self.brush_size - 2, 1)
        else:
            self.eraser_size = max(self.eraser_size - 5, 10)
    
    def toggle_tool(self):
        """Switch between pen and eraser"""
        if self.tool == 'pen':
            self.tool = 'eraser'
        else:
            self.tool = 'pen'
    
    def update(self, finger_pos, is_drawing):
        """
        Update drawing state
        
        Args:
            finger_pos: (x, y) position of finger
            is_drawing: Boolean indicating if drawing mode is active
        """
        if finger_pos and is_drawing:
            if self.prev_point is not None:
                # Draw line from previous point to current point
                if self.tool == 'pen':
                    cv2.line(self.canvas, self.prev_point, finger_pos,
                            self.current_color, self.brush_size)
                elif self.tool == 'eraser':
                    cv2.circle(self.canvas, finger_pos, self.eraser_size,
                              (255, 255, 255), -1)
            
            self.prev_point = finger_pos
            self.drawing = True
        else:
            if self.drawing:
                # Save to history when stopping drawing
                self.save_to_history()
            self.prev_point = None
            self.drawing = False
    
    def draw_ui(self, frame):
        """
        Draw UI elements on frame
        
        Args:
            frame: Video frame
            
        Returns:
            Combined frame with canvas and UI
        """
        # Blend canvas with video frame
        alpha = 0.7
        result = cv2.addWeighted(self.canvas, alpha, frame, 1 - alpha, 0)
        
        # Draw toolbar background
        cv2.rectangle(result, (10, 10), (350, 120), (50, 50, 50), -1)
        cv2.rectangle(result, (10, 10), (350, 120), (255, 255, 255), 2)
        
        # Draw current tool indicator
        tool_text = f"Tool: {self.tool.upper()}"
        cv2.putText(result, tool_text, (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw current color indicator
        color_name = self.colors[self.current_color_index][1]
        cv2.putText(result, f"Color: {color_name}", (20, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.rectangle(result, (180, 45), (220, 70), self.current_color, -1)
        cv2.rectangle(result, (180, 45), (220, 70), (255, 255, 255), 2)
        
        # Draw brush size indicator
        size = self.brush_size if self.tool == 'pen' else self.eraser_size
        cv2.putText(result, f"Size: {size}", (20, 95),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw drawing indicator
        if self.drawing:
            cv2.circle(result, (320, 60), 15, (0, 255, 0), -1)
            cv2.putText(result, "DRAWING", (240, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw help text
        if self.show_help:
            help_texts = [
                "C: Next Color | T: Toggle Tool | +/-: Brush Size",
                "U: Undo | X: Clear | H: Toggle Help",
                "ESC: Menu | Q: Quit"
            ]
            y = self.height - 90
            for text in help_texts:
                cv2.putText(result, text, (10, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                # Black outline for better visibility
                cv2.putText(result, text, (10, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3)
                cv2.putText(result, text, (10, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y += 30
        
        # Draw color palette if visible
        if self.show_palette:
            self._draw_color_palette(result)
        
        return result
    
    def _draw_color_palette(self, frame):
        """Draw color selection palette"""
        palette_x = self.width - 250
        palette_y = 10
        palette_w = 240
        palette_h = 60 + len(self.colors) * 40
        
        # Background
        cv2.rectangle(frame, (palette_x, palette_y),
                     (palette_x + palette_w, palette_y + palette_h),
                     (50, 50, 50), -1)
        cv2.rectangle(frame, (palette_x, palette_y),
                     (palette_x + palette_w, palette_y + palette_h),
                     (255, 255, 255), 2)
        
        # Title
        cv2.putText(frame, "Color Palette", (palette_x + 20, palette_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Colors
        y = palette_y + 60
        for i, (color, name) in enumerate(self.colors):
            # Color box
            cv2.rectangle(frame, (palette_x + 20, y),
                         (palette_x + 60, y + 30), color, -1)
            cv2.rectangle(frame, (palette_x + 20, y),
                         (palette_x + 60, y + 30), (255, 255, 255), 2)
            
            # Color name
            cv2.putText(frame, f"{i + 1}. {name}", (palette_x + 70, y + 22),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Selection indicator
            if i == self.current_color_index:
                cv2.putText(frame, "<", (palette_x + 200, y + 22),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            y += 40
    
    def toggle_palette(self):
        """Toggle color palette visibility"""
        self.show_palette = not self.show_palette
    
    def toggle_help(self):
        """Toggle help text visibility"""
        self.show_help = not self.show_help
    
    def reset(self):
        """Reset the drawing application"""
        self.clear_canvas()
        self.history = []
        self.tool = 'pen'
        self.current_color_index = 0
        self.current_color = self.colors[0][0]
        self.brush_size = 5
        self.eraser_size = 30
