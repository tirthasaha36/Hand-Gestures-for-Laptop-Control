import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_advanced_model():
    """Train ML model with data from multiple users"""
    data_dir = "advanced_gesture_data"
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    X = []
    y = []
    gesture_classes = []
    user_ids = []
    
    # Load data from advanced directory structure
    if not os.path.exists(data_dir):
        print("No advanced training data found.")
        return
    
    gestures = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d))]
    
    for gesture_idx, gesture_name in enumerate(gestures):
        gesture_dir = os.path.join(data_dir, gesture_name)
        
        # Get all user directories for this gesture
        users = [d for d in os.listdir(gesture_dir) 
                if os.path.isdir(os.path.join(gesture_dir, d))]
        
        if users:
            gesture_classes.append(gesture_name)
            
            for user in users:
                user_dir = os.path.join(gesture_dir, user)
                samples = [f for f in os.listdir(user_dir) if f.endswith('.json')]
                
                for filename in samples:
                    filepath = os.path.join(user_dir, filename)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Flatten landmarks into feature vector
                    landmarks = np.array(data['landmarks']).flatten()
                    X.append(landmarks)
                    y.append(gesture_idx)
                    user_ids.append(data.get('user_id', 'unknown'))
    
    if len(X) == 0:
        print("No training data found.")
        return
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"Training on {len(X)} samples from {len(gesture_classes)} gestures")
    print(f"Data collected from {len(set(user_ids))} different users")
    
    # Show detailed statistics
    print("\n=== Detailed Statistics ===")
    for i, gesture in enumerate(gesture_classes):
        gesture_mask = (y == i)
        gesture_samples = np.sum(gesture_mask)
        gesture_users = len(set(np.array(user_ids)[gesture_mask]))
        
        print(f"{gesture}: {gesture_samples} samples from {gesture_users} users")
    
    # Check if we have enough samples for good training
    min_samples_per_class = 1000
    for i, gesture in enumerate(gesture_classes):
        count = np.sum(y == i)
        if count < min_samples_per_class:
            print(f"⚠️  Warning: {gesture} has only {count} samples (recommended: {min_samples_per_class}+)")
    
    # Split data - use stratification to maintain class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest classifier with more trees for larger dataset
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel accuracy: {accuracy:.4f}")
    
    # Detailed classification report
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=gesture_classes))
    
    # Save model
    model_data = {
        'model': model,
        'classes': gesture_classes,
        'accuracy': accuracy,
        'total_samples': len(X),
        'num_users': len(set(user_ids))
    }
    
    model_path = os.path.join(model_dir, "advanced_gesture_model.pkl")
    joblib.dump(model_data, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Show confidence distribution
    print("\n=== Confidence Analysis ===")
    probabilities = model.predict_proba(X_test)
    confidences = np.max(probabilities, axis=1)
    
    print(f"Average confidence: {np.mean(confidences):.4f}")
    print(f"Minimum confidence: {np.min(confidences):.4f}")
    print(f"Maximum confidence: {np.max(confidences):.4f}")
    print(f"Samples with confidence < 0.7: {np.sum(confidences < 0.7)}")
    print(f"Samples with confidence < 0.5: {np.sum(confidences < 0.5)}")

def analyze_user_performance():
    """Analyze model performance per user"""
    data_dir = "advanced_gesture_data"
    model_path = "models/advanced_gesture_model.pkl"
    
    if not os.path.exists(model_path):
        print("No trained model found.")
        return
    
    # Load model
    model_data = joblib.load(model_path)
    model = model_data['model']
    gesture_classes = model_data['classes']
    
    # Load test data with user information
    X_test_user = []
    y_test_user = []
    user_ids_test = []
    
    gestures = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d))]
    
    for gesture_idx, gesture_name in enumerate(gestures):
        if gesture_name not in gesture_classes:
            continue
            
        gesture_dir = os.path.join(data_dir, gesture_name)
        users = [d for d in os.listdir(gesture_dir) 
                if os.path.isdir(os.path.join(gesture_dir, d))]
        
        for user in users:
            user_dir = os.path.join(gesture_dir, user)
            samples = [f for f in os.listdir(user_dir) if f.endswith('.json')]
            
            # Use 20% of each user's data for testing
            test_samples = samples[:len(samples)//5]
            
            for filename in test_samples:
                filepath = os.path.join(user_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                landmarks = np.array(data['landmarks']).flatten()
                X_test_user.append(landmarks)
                y_test_user.append(gesture_idx)
                user_ids_test.append(data.get('user_id', 'unknown'))
    
    if not X_test_user:
        print("No test data found for user analysis.")
        return
    
    X_test_user = np.array(X_test_user)
    y_test_user = np.array(y_test_user)
    
    # Predict and analyze by user
    print("\n=== User Performance Analysis ===")
    unique_users = sorted(set(user_ids_test))
    
    for user in unique_users:
        user_mask = np.array(user_ids_test) == user
        if np.any(user_mask):
            user_X = X_test_user[user_mask]
            user_y = y_test_user[user_mask]
            
            user_pred = model.predict(user_X)
            user_accuracy = accuracy_score(user_y, user_pred)
            
            print(f"User {user}: {np.sum(user_mask)} samples, Accuracy: {user_accuracy:.4f}")

if __name__ == "__main__":
    while True:
        print("\n=== Advanced Gesture Training ===")
        print("1. Train model with multi-user data")
        print("2. Analyze user performance")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            train_advanced_model()
        elif choice == '2':
            analyze_user_performance()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
