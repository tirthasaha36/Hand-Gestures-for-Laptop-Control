import math

class GestureRecognizer:
    def __init__(self):
        pass

    def distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def is_finger_up(self, landmarks, finger_tip, finger_dip):
        """Check if a finger is up by comparing y coordinates of tip and dip"""
        return landmarks[finger_tip][1] < landmarks[finger_dip][1]

    def recognize_gesture(self, landmarks):
        """
        Recognize gestures based on hand landmarks.
        landmarks: list of (x, y) tuples normalized [0,1]
        Returns a string representing the gesture.
        """
        # Example gestures:
        # - Open hand (all fingers up)
        # - Fist (all fingers down)
        # - Pointing (index finger up, others down)
        # - Thumb up
        # - Pinch (distance between thumb and index finger small)
        
        finger_tips = [4, 8, 12, 16, 20]
        finger_dips = [3, 7, 11, 15, 19]

        fingers_up = []
        for tip, dip in zip(finger_tips, finger_dips):
            fingers_up.append(self.is_finger_up(landmarks, tip, dip))

        # Check for open hand
        if all(fingers_up):
            return "open_hand"

        # Check for fist
        if not any(fingers_up):
            return "fist"

        # Check for pointing (only index finger up)
        if fingers_up[1] and not any(fingers_up[0:1] + fingers_up[2:]):
            return "pointing"

        # Check for thumb up (thumb up, others down)
        if fingers_up[0] and not any(fingers_up[1:]):
            return "thumb_up"

        # Check for pinch (distance between thumb tip and index tip)
        dist_thumb_index = self.distance(landmarks[4], landmarks[8])
        if dist_thumb_index < 0.05:
            return "pinch"

        return "unknown"
