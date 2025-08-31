import cv2
import mediapipe as mp
import numpy as np
import joblib
import os

def test_advanced_model():
    """Test the advanced trained model with multi-user data in real-time"""

    # Load the advanced trained model
    model_path = "models/advanced_gesture_model.pkl"
    if not os.path.exists(model_path):
        print("No advanced trained model found. Please train the model first using advanced_training.py")
        return

    model_data = joblib.load(model_path)
    model = model_data['model']
    gesture_classes = model_data['classes']

    print("=== Advanced Gesture Model Test ===")
    print(f"Loaded advanced model with {len(gesture_classes)} gestures: {gesture_classes}")
    print(f"Model trained on {model_data['total_samples']} samples from {model_data['num_users']} users")
    print(f"Training accuracy: {model_data['accuracy']:.4f}")
    print("\nStarting real-time gesture recognition...")
    print("Press 'q' to quit, 'c' to toggle confidence display")

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

    show_confidence = True
    confidence_threshold = 0.7

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        gesture_name = "No hand detected"
        confidence = 0.0
        status_color = (128, 128, 128)  # Gray for no hand

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

                if max_probability < confidence_threshold:
                    gesture_name = "unknown"
                    confidence = max_probability
                    status_color = (0, 0, 255)  # Red for unknown
                else:
                    gesture_name = gesture_classes[prediction]
                    confidence = max_probability
                    status_color = (0, 255, 0)  # Green for recognized

        # Display gesture prediction
        if show_confidence:
            text = f"{gesture_name} ({confidence:.2f})"
        else:
            text = f"{gesture_name}"

        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, status_color, 2, cv2.LINE_AA)

        # Display model info
        cv2.putText(frame, f"Advanced Model: {len(gesture_classes)} gestures", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        # Display instructions
        cv2.putText(frame, "Press 'q' to quit, 'c' to toggle confidence", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

        # Display confidence threshold info
        cv2.putText(frame, f"Confidence threshold: {confidence_threshold}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

        cv2.imshow("Advanced Gesture Recognition Test", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_confidence = not show_confidence
            print(f"Confidence display: {'ON' if show_confidence else 'OFF'}")

    cap.release()
    cv2.destroyAllWindows()
    print("Advanced model test completed.")

if __name__ == "__main__":
    test_advanced_model()
