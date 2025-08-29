import os
import shutil
import stat
import subprocess
import platform

def remove_readonly(func, path, _):
    """Remove readonly attribute from files before deletion"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_gesture(gesture_name):
    """Delete a gesture folder with comprehensive error handling"""
    gesture_dir = os.path.join("gesture_data", gesture_name)
    
    if not os.path.exists(gesture_dir):
        print(f"Gesture '{gesture_name}' not found.")
        return False
    
    # Check folder contents
    try:
        contents = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
        sample_count = len(contents)
        
        if sample_count == 0:
            print(f"Gesture '{gesture_name}' folder is empty.")
        else:
            print(f"Gesture '{gesture_name}' has {sample_count} samples.")
            
    except PermissionError:
        print(f"Cannot access '{gesture_name}' folder due to permissions.")
        sample_count = "unknown"
    except Exception as e:
        print(f"Error checking folder contents: {e}")
        sample_count = "unknown"
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete gesture '{gesture_name}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return False
    
    # Try multiple deletion methods
    methods = [
        _delete_with_shutil,
        _delete_with_powershell,
        _delete_with_os
    ]
    
    for method in methods:
        if method(gesture_dir):
            print(f"Gesture '{gesture_name}' successfully deleted using {method.__name__}.")
            return True
    
    print(f"Failed to delete gesture '{gesture_name}' using all methods.")
    return False

def _delete_with_shutil(gesture_dir):
    """Delete using shutil with error handler"""
    try:
        shutil.rmtree(gesture_dir, onerror=remove_readonly)
        return True
    except Exception as e:
        print(f"Shutil method failed: {e}")
        return False

def _delete_with_powershell(gesture_dir):
    """Delete using PowerShell for Windows permission handling"""
    if platform.system() != "Windows":
        return False
    
    try:
        result = subprocess.run([
            'powershell', '-Command', 
            f'Remove-Item -Path "{gesture_dir}" -Recurse -Force'
        ], capture_output=True, text=True, timeout=30)
        
        return result.returncode == 0
    except Exception as e:
        print(f"PowerShell method failed: {e}")
        return False

def _delete_with_os(gesture_dir):
    """Delete using os methods as last resort"""
    try:
        # First try to delete files
        for root, dirs, files in os.walk(gesture_dir, topdown=False):
            for name in files:
                try:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                    os.remove(os.path.join(root, name))
                except:
                    pass
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except:
                    pass
        # Then delete the main directory
        os.rmdir(gesture_dir)
        return True
    except Exception as e:
        print(f"OS method failed: {e}")
        return False

def list_gestures():
    """List all available gestures with sample counts"""
    data_dir = "gesture_data"
    
    if not os.path.exists(data_dir):
        print("No gesture data found.")
        return []
    
    gestures = []
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        if os.path.isdir(item_path):
            gestures.append(item)
    
    print("Available gestures:")
    for i, gesture in enumerate(gestures, 1):
        gesture_dir = os.path.join(data_dir, gesture)
        try:
            samples = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
            print(f"{i}. {gesture} ({len(samples)} samples)")
        except PermissionError:
            print(f"{i}. {gesture} (Permission denied)")
        except Exception as e:
            print(f"{i}. {gesture} (Error: {e})")
    
    return gestures

if __name__ == "__main__":
    print("Gesture Deletion Tool")
    print("=" * 20)
    print("Platform:", platform.system())
    print()
    
    gestures = list_gestures()
    
    if not gestures:
        print("No gestures to delete.")
        exit()
    
    try:
        choice = int(input("\nEnter the number of the gesture to delete (0 to cancel): "))
        if choice == 0:
            print("Cancelled.")
        elif 1 <= choice <= len(gestures):
            gesture_to_delete = gestures[choice - 1]
            delete_gesture(gesture_to_delete)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
