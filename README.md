# Hand Gestures for Laptop Control

A Python-based system that enables touchless laptop control using hand gestures captured through a webcam. The system uses computer vision (OpenCV, MediaPipe) to detect hand movements and maps them to various system actions.

## Project Files Overview

### Core Application Files

1. **main.py** - Main application script
   - Captures webcam video feed
   - Detects hand landmarks using MediaPipe
   - Recognizes gestures using gesture_control.py
   - Maps gestures to system control actions

2. **gesture_control.py** - Gesture recognition logic
   - Determines which fingers are up/down
   - Classifies gestures (open hand, fist, pointing, thumb up, pinch)
   - Uses hand landmark positions for gesture detection

3. **system_control.py** - System control functions
   - Mouse cursor movement and clicks
   - Volume and media playback control
   - Scroll and swipe gestures
   - Zoom in/out functionality

### Machine Learning & Data Collection

4. **gesture_trainer.py** - Basic data collection utility
   - Records custom gesture samples from webcam
   - Saves hand landmark data in JSON format
   - Creates organized folders for each gesture type

5. **advanced_gesture_trainer.py** - Advanced multi-user data collection
   - Supports 5000 samples per gesture from 5 different users
   - 0.05s capture gap for efficient data collection
   - User-specific data organization
   - High-volume gesture training capability

6. **gesture_ml.py** - Machine learning integration
   - Trains Random Forest classifier on collected data
   - Real-time gesture recognition using trained model
   - Model saving/loading functionality
   - Confidence threshold (0.7) for "unknown" gesture detection

7. **simple_train.py** - Simplified ML training
   - Trains model without MediaPipe dependency
   - Evaluates model accuracy
   - Saves trained model for deployment

### Advanced Training & Utilities

8. **advanced_training.py** - Advanced ML training
   - Trains models on multi-user advanced gesture data
   - Supports large datasets (5000 samples per gesture)
   - Enhanced model evaluation and testing
   - Cross-validation and performance metrics

9. **delete_advanced_data.py** - Advanced data management
   - Selective deletion of advanced gesture data
   - Delete by gesture name, user ID, or both
   - Statistics and user listing functionality
   - Robust Windows permission handling
   - Manual recursive deletion for stubborn files

### Testing & Utilities

10. **test_gestures.py** - Data verification
    - Lists collected gestures and sample counts
    - Verifies data structure and quality
    - Checks if enough data exists for training

11. **real_time_test.py** - Real-time testing
    - Tests trained model with live webcam feed
    - Displays recognized gestures and confidence scores
    - Camera index handling for different setups

12. **test_camera.py** - Camera testing
    - Checks available camera indices
    - Tests camera functionality
    - Shows live camera feed

13. **delete_gesture.py** - Basic gesture management
    - Lists all available gestures with sample counts
    - Safely deletes gesture folders and their samples
    - Handles Windows permission issues automatically
    - Multiple deletion methods for robustness

14. **requirements.txt** - Dependencies
    - Python package requirements
    - OpenCV, MediaPipe, pyautogui, scikit-learn, etc.

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Collect gesture data:**
   ```bash
   python gesture_trainer.py
   ```

3. **Train the model:**
   ```bash
   python simple_train.py
   ```

4. **Test real-time recognition:**
   ```bash
   python real_time_test.py
   ```

5. **Manage gestures (optional):**
   ```bash
   python delete_gesture.py
   ```

6. **Run full application:**
   ```bash
   python main.py
   ```

## Gesture Mappings

- **Open hand**: Mouse cursor movement
- **Fist**: Left click
- **Pointing**: Right click
- **Thumb up**: Volume up
- **Pinch**: Volume down

## Features

- Touchless laptop control
- Custom gesture training
- Real-time hand tracking
- Machine learning-based recognition
- Multiple system control actions
- Webcam compatibility testing
