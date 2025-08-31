import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_simple_model():
    """Train a simple ML model without MediaPipe dependency"""
    data_dir = "advanced_gesture_data"
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    X = []
    y = []
    gesture_classes = []
    
    # Load data from your collected gestures
    gestures = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d)) and d != "click"]  # Skip empty click folder
    
    for gesture_idx, gesture_name in enumerate(gestures):
        gesture_dir = os.path.join(data_dir, gesture_name)
        samples = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
        
        if len(samples) > 0:
            gesture_classes.append(gesture_name)
            
            for filename in samples:
                filepath = os.path.join(gesture_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Flatten landmarks into feature vector
                landmarks = np.array(data['landmarks']).flatten()
                X.append(landmarks)
                y.append(gesture_idx)
    
    if len(X) == 0:
        print("No training data found.")
        return
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"Training on {len(X)} samples from {len(gesture_classes)} gestures:")
    for i, gesture in enumerate(gesture_classes):
        count = np.sum(y == i)
        print(f"  {gesture}: {count} samples")
    
    # Check if we have enough samples for good training
    min_samples_per_class = 500
    for i, gesture in enumerate(gesture_classes):
        count = np.sum(y == i)
        if count < min_samples_per_class:
            print(f"⚠️  Warning: {gesture} has only {count} samples (recommended: {min_samples_per_class}+ for optimal performance)")
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel accuracy: {accuracy:.2f}")
    
    # Save model
    model_data = {
        'model': model,
        'classes': gesture_classes
    }
    
    model_path = os.path.join(model_dir, "simple_gesture_model.pkl")
    joblib.dump(model_data, model_path)
    print(f"Model saved to {model_path}")
    
    # Show some predictions
    print("\nSample predictions:")
    for i in range(min(5, len(X_test))):
        true_gesture = gesture_classes[y_test[i]]
        pred_gesture = gesture_classes[y_pred[i]]
        confidence = np.max(model.predict_proba([X_test[i]]))
        print(f"  True: {true_gesture} -> Predicted: {pred_gesture} ({confidence:.2f})")

if __name__ == "__main__":
    train_simple_model()
