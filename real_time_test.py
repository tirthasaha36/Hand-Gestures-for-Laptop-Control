import cv2
import mediapipe as mp
import numpy as np
import joblib
import os

def real_time_gesture_test():
    """Test your trained gestures in real-time with webcam"""
    
    # Load the trained model
    model_path = "models/gesture_model.pkl"
    if not os.path.exists(model_path):
        print("No trained model found. Please train a model first.")
        return
    
    model_data = joblib.load(model_path)
    model = model_data['model']
    gesture_classes = model_data['classes']
    
    print(f"Loaded model with gestures: {gesture_classes}")
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    
    # Try camera index 1 (your working camera)
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Camera index 1 not available, trying index 0...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open any camera.")
        return
    
    print("Real-time gesture recognition started!")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        gesture_name = "No hand"
        confidence = 0.0
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])
                
                # Predict gesture
                features = np.array(landmarks).flatten().reshape(1, -1)
                prediction = model.predict(features)[0]
                confidence = np.max(model.predict_proba(features))
                gesture_name = gesture_classes[prediction]
        
        # Display prediction
        text = f"{gesture_name} ({confidence:.2f})"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Display instructions
        cv2.putText(frame, "Press 'q' to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.imshow("Gesture Recognition Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Real-time test completed.")

if __name__ == "__main__":
    real_time_gesture_test()
