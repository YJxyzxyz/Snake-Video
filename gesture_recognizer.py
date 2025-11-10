"""
Gesture Recognizer Module
Recognizes various hand gestures for game control
"""

import math


class GestureRecognizer:
    """Recognizes hand gestures from MediaPipe landmarks"""
    
    def __init__(self):
        """Initialize gesture recognizer"""
        self.last_gesture = None
        self.gesture_cooldown = 0
        
    def recognize_gesture(self, hand_landmarks):
        """
        Recognize gesture from hand landmarks
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            str: Recognized gesture name or None
        """
        if not hand_landmarks:
            return None
        
        # Cooldown to prevent rapid gesture detection
        if self.gesture_cooldown > 0:
            self.gesture_cooldown -= 1
            return self.last_gesture
        
        gesture = self._detect_gesture(hand_landmarks)
        
        if gesture and gesture != self.last_gesture:
            self.last_gesture = gesture
            self.gesture_cooldown = 10  # 10 frame cooldown
            return gesture
        
        return None
    
    def _detect_gesture(self, hand_landmarks):
        """
        Internal method to detect specific gestures
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            str: Gesture name or None
        """
        # Get finger states (extended or not)
        fingers_up = self._count_fingers_up(hand_landmarks)
        
        # Recognize gestures based on finger count and positions
        if fingers_up == [0, 1, 0, 0, 0]:  # Only index finger up
            return "point"
        elif fingers_up == [0, 1, 1, 0, 0]:  # Index and middle up
            return "peace"
        elif fingers_up == [1, 0, 0, 0, 1]:  # Thumb and pinky up
            return "call"
        elif fingers_up == [1, 1, 1, 1, 1]:  # All fingers up
            return "open_palm"
        elif fingers_up == [0, 0, 0, 0, 0]:  # Fist
            return "fist"
        elif self._is_pinch(hand_landmarks):
            return "pinch"
        elif self._is_thumbs_up(hand_landmarks):
            return "thumbs_up"
        elif self._is_thumbs_down(hand_landmarks):
            return "thumbs_down"
        
        return None
    
    def _count_fingers_up(self, hand_landmarks):
        """
        Count which fingers are extended
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            list: [thumb, index, middle, ring, pinky] - 1 if up, 0 if down
        """
        fingers = []
        landmarks = hand_landmarks.landmark
        
        # Thumb (special case - check horizontal distance)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        fingers.append(1 if thumb_tip.x < thumb_ip.x - 0.05 else 0)
        
        # Other fingers (check vertical position)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip_id, pip_id in zip(finger_tips, finger_pips):
            tip = landmarks[tip_id]
            pip = landmarks[pip_id]
            fingers.append(1 if tip.y < pip.y else 0)
        
        return fingers
    
    def _is_pinch(self, hand_landmarks):
        """
        Detect pinch gesture (thumb and index finger close together)
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            bool: True if pinching
        """
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        # Calculate distance between thumb and index finger tips
        distance = math.sqrt(
            (thumb_tip.x - index_tip.x) ** 2 +
            (thumb_tip.y - index_tip.y) ** 2
        )
        
        return distance < 0.05
    
    def _is_thumbs_up(self, hand_landmarks):
        """
        Detect thumbs up gesture
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            bool: True if thumbs up
        """
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        
        # Thumb should be up and other fingers down
        fingers = self._count_fingers_up(hand_landmarks)
        thumb_is_up = thumb_tip.y < thumb_mcp.y - 0.1
        other_fingers_down = sum(fingers[1:]) == 0
        
        return thumb_is_up and other_fingers_down
    
    def _is_thumbs_down(self, hand_landmarks):
        """
        Detect thumbs down gesture
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            bool: True if thumbs down
        """
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[4]
        thumb_mcp = landmarks[2]
        
        # Thumb should be down and other fingers down
        fingers = self._count_fingers_up(hand_landmarks)
        thumb_is_down = thumb_tip.y > thumb_mcp.y + 0.1
        other_fingers_down = sum(fingers[1:]) == 0
        
        return thumb_is_down and other_fingers_down
    
    def get_finger_distance(self, hand_landmarks, finger1_id, finger2_id):
        """
        Calculate distance between two finger tips
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            finger1_id: First finger landmark ID
            finger2_id: Second finger landmark ID
            
        Returns:
            float: Normalized distance
        """
        if not hand_landmarks:
            return None
        
        landmarks = hand_landmarks.landmark
        finger1 = landmarks[finger1_id]
        finger2 = landmarks[finger2_id]
        
        distance = math.sqrt(
            (finger1.x - finger2.x) ** 2 +
            (finger1.y - finger2.y) ** 2
        )
        
        return distance
