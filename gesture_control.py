import math

import numpy as np
import joblib
import os

class GestureRecognizer:
    def __init__(self):
        self.model_path = "models/advanced_gesture_model.pkl"
        self.model = None
        self.gesture_classes = []
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.gesture_classes = data['classes']
            print(f"Loaded advanced gesture model with {len(self.gesture_classes)} gestures")
        else:
            print("Advanced gesture model not found. Please train the model first.")

    def recognize_gesture(self, landmarks):
        if self.model is None:
            return "unknown"

        # Flatten landmarks with z included
        features = np.array(landmarks).flatten().reshape(1, -1)

        # Predict gesture
        prediction = self.model.predict(features)[0]
        gesture_name = self.gesture_classes[prediction]

        return gesture_name
