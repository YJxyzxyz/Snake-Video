"""
Hand Tracker Module
Uses MediaPipe to detect hands and extract finger positions
"""

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """Tracks hand landmarks and provides finger positions"""
    
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initialize the hand tracker
        
        Args:
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, frame, draw=True):
        """
        Find hands in the frame
        
        Args:
            frame: Input frame (BGR format)
            draw: Whether to draw hand landmarks on the frame
            
        Returns:
            frame: Frame with drawn landmarks (if draw=True)
            results: MediaPipe hand detection results
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(frame_rgb)
        
        # Draw hand landmarks
        if draw and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return frame, results
    
    def get_index_finger_position(self, frame, results):
        """
        Get the position of the index finger tip
        
        Args:
            frame: Input frame
            results: MediaPipe hand detection results
            
        Returns:
            tuple: (x, y) position of index finger tip, or None if not found
        """
        if not results.multi_hand_landmarks:
            return None
        
        # Get the first hand detected
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Index finger tip is landmark 8
        index_finger_tip = hand_landmarks.landmark[8]
        
        # Convert normalized coordinates to pixel coordinates
        h, w, c = frame.shape
        x = int(index_finger_tip.x * w)
        y = int(index_finger_tip.y * h)
        
        return (x, y)
    
    def get_all_finger_positions(self, frame, results):
        """
        Get positions of all finger tips
        
        Args:
            frame: Input frame
            results: MediaPipe hand detection results
            
        Returns:
            dict: Dictionary with finger names as keys and (x, y) positions as values
        """
        if not results.multi_hand_landmarks:
            return None
        
        # Get the first hand detected
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Finger tip landmark indices
        finger_tips = {
            'thumb': 4,
            'index': 8,
            'middle': 12,
            'ring': 16,
            'pinky': 20
        }
        
        h, w, c = frame.shape
        positions = {}
        
        for finger_name, landmark_id in finger_tips.items():
            landmark = hand_landmarks.landmark[landmark_id]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            positions[finger_name] = (x, y)
        
        return positions
    
    def close(self):
        """Release resources"""
        self.hands.close()
