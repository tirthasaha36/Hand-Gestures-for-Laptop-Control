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

4. **advanced_gesture_trainer.py** - Multi-user data collection
   - Supports collecting data from multiple users
   - User-specific data organization
   - High-volume gesture training capability

5. **advanced_training.py** - Advanced ML training
   - Trains models on multi-user advanced gesture data
   - Supports large datasets (1500 samples per gesture)
   - Enhanced model evaluation and testing
   - Cross-validation and performance metrics

6. **test_advanced_model.py** - Advanced model testing
   - Tests trained model with multi-user data in real-time
   - Displays recognized gestures and confidence scores
   - Camera index handling for different setups

### Data Management & Utilities

7. **delete_advanced_data.py** - Advanced data management
   - Selective deletion of advanced gesture data
   - Delete by gesture name, user ID, or both
   - Statistics and user listing functionality
   - Robust Windows permission handling
   - Manual recursive deletion for stubborn files

8. **delete_gesture.py** - Basic gesture management
   - Lists all available gestures with sample counts
   - Safely deletes gesture folders and their samples
   - Handles Windows permission issues automatically
   - Multiple deletion methods for robustness

### Testing & Utilities

9. **test_camera.py** - Camera testing
    - Checks available camera indices
    - Tests camera functionality
    - Shows live camera feed

10. **requirements.txt** - Dependencies
    - Python package requirements
    - OpenCV, MediaPipe, pyautogui, scikit-learn, etc.

### Deprecated Files

- **gesture_ml.py** - Legacy machine learning integration (superseded by advanced_training.py)
- **test_gestures.py** - Legacy data verification (superseded by advanced_training.py and test_advanced_model.py)
- **real_time_test.py** - Legacy real-time testing (superseded by test_advanced_model.py)
- **gesture_trainer.py** - Legacy data collection (superseded by advanced_gesture_trainer.py)
- **simple_train.py** - Legacy training (superseded by advanced_training.py)

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Collect gesture data:**
   ```bash
   python advanced_gesture_trainer.py
   ```

3. **Train the model:**
   ```bash
   python advanced_training.py
   ```

4. **Test real-time recognition:**
   ```bash
   python test_advanced_model.py
   ```

5. **Manage gestures (optional):**
   ```bash
   python delete_advanced_data.py
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
