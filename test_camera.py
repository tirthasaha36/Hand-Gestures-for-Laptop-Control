import cv2
import mediapipe as mp

def test_camera_availability():
    """Test which camera indices are available"""
    print("Testing camera availability...")
    
    # Try different camera indices
    for camera_index in [0, 1, 2]:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            print(f"Camera index {camera_index}: AVAILABLE")
            ret, frame = cap.read()
            if ret:
                print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
        else:
            print(f"Camera index {camera_index}: NOT AVAILABLE")

def simple_camera_test():
    """Simple camera test to verify webcam works"""
    print("\nTesting camera feed...")
    
    # Try camera index 0 first
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera index 0 not available, trying index 1...")
        cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("No camera found!")
        return
    
    print("Camera found! Press 'q' to exit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Camera Test - Press 'q' to exit", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera test completed.")

if __name__ == "__main__":
    test_camera_availability()
    simple_camera_test()
