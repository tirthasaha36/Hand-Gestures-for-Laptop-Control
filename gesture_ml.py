import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import cv2
import mediapipe as mp

class GestureML:
    def __init__(self):
        self.data_dir = "gesture_data"
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        
        self.model = None
        self.gesture_classes = []

    def load_gesture_data(self):
        """Load all collected gesture data"""
        X = []
        y = []
        
        if not os.path.exists(self.data_dir):
            return X, y
        
        gestures = [d for d in os.listdir(self.data_dir) 
                   if os.path.isdir(os.path.join(self.data_dir, d))]
        
        self.gesture_classes = gestures
        
        for gesture_idx, gesture_name in enumerate(gestures):
            gesture_dir = os.path.join(self.data_dir, gesture_name)
            
            for filename in os.listdir(gesture_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(gesture_dir, filename)
                    
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Flatten landmarks into feature vector
                    landmarks = np.array(data['landmarks']).flatten()
                    X.append(landmarks)
                    y.append(gesture_idx)
        
        return np.array(X), np.array(y)

    def train_model(self):
        """Train machine learning model on collected data"""
        X, y = self.load_gesture_data()
        
        if len(X) == 0:
            print("No training data found. Please collect some gestures first.")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {accuracy:.2f}")
        
        # Save model
        model_path = os.path.join(self.model_dir, "gesture_model.pkl")
        joblib.dump({
            'model': self.model,
            'classes': self.gesture_classes
        }, model_path)
        
        print(f"Model saved to {model_path}")
        return True

    def load_model(self):
        """Load trained model"""
        model_path = os.path.join(self.model_dir, "gesture_model.pkl")
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.gesture_classes = data['classes']
            print(f"Model loaded with {len(self.gesture_classes)} gestures")
            return True
        else:
            print("No trained model found. Please train a model first.")
            return False

    def predict_gesture(self, landmarks, confidence_threshold=0.7):
        """Predict gesture from landmarks with confidence threshold"""
        if self.model is None:
            return "unknown", 0.0
        
        # Flatten landmarks
        features = np.array(landmarks).flatten().reshape(1, -1)
        
        # Predict
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        max_probability = np.max(probabilities)
        
        # Return "unknown" if confidence is below threshold
        if max_probability < confidence_threshold:
            return "unknown", max_probability
        
        gesture_name = self.gesture_classes[prediction]
        return gesture_name, max_probability

    def real_time_test(self):
        """Test the model in real-time with webcam"""
        if not self.load_model():
            return
        
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        print("Real-time gesture recognition started. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            gesture_name = "unknown"
            confidence = 0.0
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Extract landmarks
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append([lm.x, lm.y, lm.z])
                    
                    # Predict gesture with confidence threshold
                    gesture_name, confidence = self.predict_gesture(landmarks, confidence_threshold=0.7)
            
            # Display prediction
            text = f"{gesture_name} ({confidence:.2f})"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.imshow("Gesture Recognition", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    ml = GestureML()
    
    while True:
        print("\n=== Gesture Machine Learning ===")
        print("1. Train model on collected data")
        print("2. Test model in real-time")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            ml.train_model()
        
        elif choice == '2':
            ml.real_time_test()
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
