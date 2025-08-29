import cv2
import mediapipe as mp
import numpy as np
import os
import json
from datetime import datetime

class GestureTrainer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Create data directory if it doesn't exist
        self.data_dir = "gesture_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.current_gesture = None
        self.recording = False
        self.samples_collected = 0
        self.max_samples = 30  # Samples per gesture

    def collect_gesture_data(self, gesture_name):
        """Collect training data for a specific gesture"""
        self.current_gesture = gesture_name
        self.recording = True
        self.samples_collected = 0
        
        # Create directory for this gesture
        gesture_dir = os.path.join(self.data_dir, gesture_name)
        os.makedirs(gesture_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(1)  # Use camera index 1
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        print(f"Recording gesture: {gesture_name}")
        print("Press 's' to start/stop recording, 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            landmarks_data = None
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Extract landmark coordinates
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append([lm.x, lm.y, lm.z])
                    landmarks_data = landmarks
            
            # Display status
            status_text = f"Gesture: {gesture_name} - Samples: {self.samples_collected}/{self.max_samples}"
            if self.recording:
                status_text += " - RECORDING"
            
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.imshow("Gesture Trainer", frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):  # Start/stop recording
                self.recording = not self.recording
                if self.recording:
                    print("Recording started...")
                else:
                    print("Recording paused...")
            
            elif key == ord('q'):  # Quit
                break
            
            # Record data if recording is active and landmarks are detected
            if self.recording and landmarks_data and self.samples_collected < self.max_samples:
                # Save landmark data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(gesture_dir, f"{timestamp}.json")
                
                with open(filename, 'w') as f:
                    json.dump({
                        'gesture': gesture_name,
                        'landmarks': landmarks_data,
                        'timestamp': timestamp
                    }, f)
                
                self.samples_collected += 1
                print(f"Sample {self.samples_collected}/{self.max_samples} saved")
                
                if self.samples_collected >= self.max_samples:
                    self.recording = False
                    print(f"Finished collecting {self.max_samples} samples for {gesture_name}")
        
        cap.release()
        cv2.destroyAllWindows()

    def list_gestures(self):
        """List all collected gestures"""
        if os.path.exists(self.data_dir):
            gestures = [d for d in os.listdir(self.data_dir) 
                       if os.path.isdir(os.path.join(self.data_dir, d))]
            return gestures
        return []

def main():
    trainer = GestureTrainer()
    
    while True:
        print("\n=== Gesture Trainer ===")
        print("1. Collect new gesture data")
        print("2. List collected gestures")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            gesture_name = input("Enter gesture name: ").strip()
            if gesture_name:
                trainer.collect_gesture_data(gesture_name)
            else:
                print("Gesture name cannot be empty.")
        
        elif choice == '2':
            gestures = trainer.list_gestures()
            if gestures:
                print("Collected gestures:")
                for gesture in gestures:
                    print(f" - {gesture}")
            else:
                print("No gestures collected yet.")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
