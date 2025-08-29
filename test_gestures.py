import os
import json
import numpy as np

def test_collected_gestures():
    """Test the gestures you've collected by listing and analyzing them"""
    data_dir = "gesture_data"
    
    if not os.path.exists(data_dir):
        print("No gesture data found. Please collect some gestures first using gesture_trainer.py")
        return
    
    # List all collected gestures
    gestures = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d))]
    
    print("=== Collected Gestures ===")
    for gesture in gestures:
        gesture_dir = os.path.join(data_dir, gesture)
        samples = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
        print(f"Gesture: {gesture} - Samples: {len(samples)}")
        
        # Show sample data structure
        if samples:
            sample_file = os.path.join(gesture_dir, samples[0])
            with open(sample_file, 'r') as f:
                data = json.load(f)
            print(f"  Landmarks shape: {np.array(data['landmarks']).shape}")
            print(f"  Sample timestamp: {data['timestamp']}")
    
    print(f"\nTotal gestures collected: {len(gestures)}")
    
    # Check if we have enough data for training
    if len(gestures) >= 2:
        print("\n✅ You have collected enough gestures for training!")
        print("You can proceed to train the ML model when the MediaPipe issue is resolved.")
    else:
        print("\n❌ You need at least 2 different gestures to train a model.")

def verify_gesture_samples(gesture_name):
    """Verify samples for a specific gesture"""
    gesture_dir = os.path.join("gesture_data", gesture_name)
    
    if not os.path.exists(gesture_dir):
        print(f"Gesture '{gesture_name}' not found.")
        return
    
    samples = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
    print(f"\n=== Verification for '{gesture_name}' ===")
    print(f"Number of samples: {len(samples)}")
    
    if samples:
        # Check a few samples
        for i, sample_file in enumerate(samples[:3]):  # Check first 3 samples
            filepath = os.path.join(gesture_dir, sample_file)
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"Sample {i+1}: {data['timestamp']} - {len(data['landmarks'])} landmarks")

if __name__ == "__main__":
    print("Testing your collected gesture data...")
    test_collected_gestures()
    
    # If you want to verify specific gestures, uncomment and modify:
    # verify_gesture_samples("your_gesture_name_here")
    # verify_gesture_samples("another_gesture_name_here")
