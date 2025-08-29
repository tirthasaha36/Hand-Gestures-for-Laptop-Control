import cv2
import mediapipe as mp
from gesture_control import GestureRecognizer
from system_control import SystemController

def main():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    # Initialize gesture and system controllers
    gesture_recognizer = GestureRecognizer()
    system_controller = SystemController()

    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for natural interaction
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on frame
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract normalized landmark coordinates
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x, lm.y))

                # Recognize gesture
                gesture = gesture_recognizer.recognize_gesture(landmarks)

                # Map gestures to system control
                if gesture == "open_hand":
                    # Move cursor to index finger tip position
                    x, y = landmarks[8]
                    system_controller.move_cursor(x, y)
                elif gesture == "fist":
                    system_controller.left_click()
                elif gesture == "pointing":
                    system_controller.right_click()
                elif gesture == "thumb_up":
                    system_controller.volume_up()
                elif gesture == "pinch":
                    system_controller.volume_down()

                # Display gesture on frame
                cv2.putText(frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Hand Gesture Control", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
