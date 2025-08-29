import cv2
import mediapipe as mp
import numpy as np
import joblib
import os

def debug_gesture_recognition():
    """Debug gesture recognition to see what's happening"""
    
    # Load the trained model
    model_path = "models/gesture_model.pkl"
    if not os.path.exists(model_path):
        print("No trained model found.")
        return
    
    model_data = joblib.load(model_path)
    model = model_data['model']
    gesture_classes = model_data['classes']
    
    print(f"Loaded model with gestures: {gesture_classes}")
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Debug mode started! Press 'q' to quit")
    print("Press 'd' to see detailed prediction info")
    
    show_details = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        gesture_name = "No hand"
        confidence = 0.0
        detailed_info = ""
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])
                
                # Predict gesture with confidence threshold
                features = np.array(landmarks).flatten().reshape(1, -1)
                probabilities = model.predict_proba(features)[0]
                max_probability = np.max(probabilities)
                prediction = model.predict(features)[0]
                confidence_threshold = 0.7
                
                if show_details:
                    detailed_info = f"Top predictions:\n"
                    sorted_indices = np.argsort(probabilities)[::-1]
                    for i in range(min(3, len(probabilities))):
                        idx = sorted_indices[i]
                        detailed_info += f"  {gesture_classes[idx]}: {probabilities[idx]:.3f}\n"
                
                if max_probability < confidence_threshold:
                    gesture_name = "unknown"
                    confidence = max_probability
                else:
                    gesture_name = gesture_classes[prediction]
                    confidence = max_probability
        
        # Display prediction
        text = f"{gesture_name} ({confidence:.2f})"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)
        
        if show_details and detailed_info:
            y_offset = 60
            for line in detailed_info.split('\n'):
                cv2.putText(frame, line, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 1, cv2.LINE_AA)
                y_offset += 20
        
        cv2.putText(frame, "Press 'q' to quit, 'd' for details", (10, frame.shape[0] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow("Gesture Debug", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('d'):
            show_details = not show_details
            print(f"Detailed info: {'ON' if show_details else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("Debug completed.")

if __name__ == "__main__":
    debug_gesture_recognition()
