import cv2
import mediapipe as mp
import numpy as np
import os
import json
from datetime import datetime
import time

class AdvancedGestureTrainer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Create data directory structure
        self.data_dir = "advanced_gesture_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.current_gesture = None
        self.current_user = None
        self.recording = False
        self.samples_collected = 0
        self.max_samples = 1500  # 1500 samples per user per gesture

    def collect_gesture_data(self, gesture_name, user_id):
        """Collect training data for a specific gesture from a specific user"""
        self.current_gesture = gesture_name
        self.current_user = user_id
        self.recording = True
        self.samples_collected = 0
        
        # Create directory structure: gesture_data/gesture_name/user_id/
        gesture_dir = os.path.join(self.data_dir, gesture_name)
        user_dir = os.path.join(gesture_dir, f"user_{user_id}")
        os.makedirs(user_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        print(f"Recording gesture: {gesture_name} for user: {user_id}")
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
            status_text = f"Gesture: {gesture_name} - User: {user_id}"
            status_text += f" - Samples: {self.samples_collected}/{self.max_samples}"
            if self.recording:
                status_text += " - RECORDING"
            
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.imshow("Advanced Gesture Trainer", frame)
            
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
                # Add small time gap between captures
                time.sleep(0.05)
                
                # Save landmark data with user information
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(user_dir, f"{timestamp}.json")
                
                with open(filename, 'w') as f:
                    json.dump({
                        'gesture': gesture_name,
                        'user_id': user_id,
                        'landmarks': landmarks_data,
                        'timestamp': timestamp
                    }, f)
                
                self.samples_collected += 1
                if self.samples_collected % 100 == 0:  # Print progress every 100 samples
                    print(f"Sample {self.samples_collected}/{self.max_samples} saved")
                
                if self.samples_collected >= self.max_samples:
                    self.recording = False
                    print(f"Finished collecting {self.max_samples} samples for {gesture_name} (user {user_id})")
        
        cap.release()
        cv2.destroyAllWindows()

    def list_gestures_and_users(self):
        """List all collected gestures and their users"""
        if not os.path.exists(self.data_dir):
            return {}
        
        data_structure = {}
        gestures = [d for d in os.listdir(self.data_dir) 
                   if os.path.isdir(os.path.join(self.data_dir, d))]
        
        for gesture in gestures:
            gesture_dir = os.path.join(self.data_dir, gesture)
            users = [d for d in os.listdir(gesture_dir) 
                    if os.path.isdir(os.path.join(gesture_dir, d))]
            
            user_samples = {}
            for user in users:
                user_dir = os.path.join(gesture_dir, user)
                samples = [f for f in os.listdir(user_dir) if f.endswith('.json')]
                user_samples[user] = len(samples)
            
            data_structure[gesture] = user_samples
        
        return data_structure

    def get_data_statistics(self):
        """Get comprehensive statistics about collected data"""
        stats = self.list_gestures_and_users()
        
        print("\n=== Data Collection Statistics ===")
        total_samples = 0
        total_users = 0
        
        for gesture, users in stats.items():
            gesture_samples = sum(users.values())
            total_samples += gesture_samples
            total_users += len(users)
            
            print(f"\nGesture: {gesture}")
            print(f"  Total samples: {gesture_samples}")
            print(f"  Users: {len(users)}")
            for user, count in users.items():
                print(f"    {user}: {count} samples")
        
        print(f"\nOverall Statistics:")
        print(f"Total gestures: {len(stats)}")
        print(f"Total users: {total_users}")
        print(f"Total samples: {total_samples}")
        
        return stats

def main():
    trainer = AdvancedGestureTrainer()
    
    while True:
        print("\n=== Advanced Gesture Trainer ===")
        print("1. Collect new gesture data (with user ID)")
        print("2. View data statistics")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            gesture_name = input("Enter gesture name: ").strip()
            user_id = input("Enter user ID (1-5 for different people): ").strip()
            
            if gesture_name and user_id:
                try:
                    user_id = int(user_id)
                    trainer.collect_gesture_data(gesture_name, user_id)
                except ValueError:
                    print("User ID must be a number.")
            else:
                print("Gesture name and user ID cannot be empty.")
        
        elif choice == '2':
            trainer.get_data_statistics()
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
