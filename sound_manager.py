"""
Sound Manager Module
Handles sound effects and background music using simple beep tones
"""

import threading
import time
import sys


class SoundManager:
    """Manages game sound effects"""
    
    def __init__(self, enabled=True):
        """
        Initialize sound manager
        
        Args:
            enabled: Whether sounds are enabled
        """
        self.enabled = enabled
        self._playing = False
        
    def play_eat_sound(self):
        """Play sound when snake eats food"""
        if not self.enabled:
            return
        
        # Non-blocking sound play
        thread = threading.Thread(target=self._beep, args=(800, 0.1))
        thread.daemon = True
        thread.start()
    
    def play_game_over_sound(self):
        """Play sound when game is over"""
        if not self.enabled:
            return
        
        thread = threading.Thread(target=self._play_game_over_sequence)
        thread.daemon = True
        thread.start()
    
    def play_level_up_sound(self):
        """Play sound when reaching milestones"""
        if not self.enabled:
            return
        
        thread = threading.Thread(target=self._play_level_up_sequence)
        thread.daemon = True
        thread.start()
    
    def play_menu_sound(self):
        """Play sound for menu selection"""
        if not self.enabled:
            return
        
        thread = threading.Thread(target=self._beep, args=(1000, 0.05))
        thread.daemon = True
        thread.start()
    
    def _beep(self, frequency, duration):
        """
        Play a beep sound
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
        """
        try:
            # Try different methods based on platform
            if sys.platform == 'win32':
                import winsound
                winsound.Beep(frequency, int(duration * 1000))
            elif sys.platform == 'darwin':
                # macOS
                import os
                os.system(f'afplay /System/Library/Sounds/Tink.aiff &')
            else:
                # Linux - using system beep
                print('\a', end='', flush=True)
        except Exception as e:
            # Silently fail if sound doesn't work
            pass
    
    def _play_game_over_sequence(self):
        """Play descending tone sequence for game over"""
        frequencies = [800, 600, 400, 200]
        for freq in frequencies:
            self._beep(freq, 0.15)
            time.sleep(0.05)
    
    def _play_level_up_sequence(self):
        """Play ascending tone sequence for level up"""
        frequencies = [400, 600, 800, 1000]
        for freq in frequencies:
            self._beep(freq, 0.1)
            time.sleep(0.05)
    
    def set_enabled(self, enabled):
        """
        Enable or disable sounds
        
        Args:
            enabled: Boolean to enable/disable sounds
        """
        self.enabled = enabled
