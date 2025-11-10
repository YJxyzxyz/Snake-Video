#!/usr/bin/env python3
"""
Quick Start Script for Hand-Gesture Snake Game
This script performs a quick check before starting the game
"""

import sys
import subprocess


def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy'
    }
    
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages detected!")
        print("Please install them using:")
        print(f"    pip install {' '.join(missing)}")
        print("\nOr install all dependencies:")
        print("    pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies are installed!")
    return True


def check_camera():
    """Check if camera is available"""
    print("\nChecking camera availability...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera is available")
            cap.release()
            return True
        else:
            print("✗ Cannot open camera")
            print("  Please check if:")
            print("  - Your camera is connected")
            print("  - Camera permissions are granted")
            print("  - No other application is using the camera")
            return False
    except Exception as e:
        print(f"✗ Error checking camera: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Hand-Gesture Controlled Snake Game - Quick Start")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first!")
        sys.exit(1)
    
    # Check camera
    if not check_camera():
        print("\n⚠️  Camera issue detected. The game may not work properly.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
    
    # Start the game
    print("\n" + "=" * 60)
    print("Starting the game...")
    print("=" * 60)
    print()
    print("📋 Quick Instructions:")
    print("  • Move your hand in front of the camera")
    print("  • Point your INDEX FINGER where you want the snake to go")
    print("  • Keep your hand within the game grid area")
    print("  • Press 'R' to restart | Press 'Q' to quit")
    print()
    print("Starting in 3 seconds...")
    print()
    
    import time
    time.sleep(3)
    
    # Import and run the game
    try:
        from main import main as run_game
        run_game()
    except Exception as e:
        print(f"\n❌ Error starting game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
