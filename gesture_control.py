import math

class GestureRecognizer:
    def __init__(self):
        pass

    def distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def is_finger_up_screen_orientation(self, landmarks, finger_tip, finger_dip):
        """
        Check if a finger is up based on screen orientation (not camera orientation).
        For screen orientation, we compare x coordinates since the frame is flipped.
        """
        return landmarks[finger_tip][0] < landmarks[finger_dip][0]

    def recognize_gesture(self, landmarks):
        """
        Recognize gestures based on hand landmarks with screen orientation.
        landmarks: list of (x, y) tuples normalized [0,1]
        Returns a string representing the gesture.
        """
        finger_tips = [4, 8, 12, 16, 20]
        finger_dips = [3, 7, 11, 15, 19]

        fingers_up = []
        for tip, dip in zip(finger_tips, finger_dips):
            fingers_up.append(self.is_finger_up_screen_orientation(landmarks, tip, dip))

        # Check for open hand (all fingers up relative to screen)
        if all(fingers_up):
            return "open_hand"

        # Check for fist (all fingers down relative to screen)
        if not any(fingers_up):
            return "fist"

        # Check for pointing (only index finger up relative to screen)
        if fingers_up[1] and not any(fingers_up[0:1] + fingers_up[2:]):
            return "pointing"

        # Check for thumb up (thumb up relative to screen, others down)
        # Additional check: thumb should be significantly extended compared to other fingers
        if fingers_up[0] and not any(fingers_up[1:]):
            # Ensure thumb is clearly extended by checking distance from wrist
            thumb_tip = landmarks[4]
            wrist = landmarks[0]
            thumb_extension = self.distance(thumb_tip, wrist)
            
            # Check if thumb is extended enough (not just slightly up)
            if thumb_extension > 0.15:  # Adjust this threshold as needed
                return "thumb_up"

        # Check for pinch (distance between thumb tip and index tip)
        dist_thumb_index = self.distance(landmarks[4], landmarks[8])
        if dist_thumb_index < 0.05:
            return "pinch"

        return "unknown"
