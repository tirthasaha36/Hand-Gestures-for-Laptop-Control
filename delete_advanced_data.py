import os
import shutil

def list_gestures_and_users():
    """List all collected gestures and their users"""
    data_dir = "advanced_gesture_data"
    
    if not os.path.exists(data_dir):
        print("No advanced gesture data found.")
        return {}
    
    data_structure = {}
    gestures = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d))]
    
    for gesture in gestures:
        gesture_dir = os.path.join(data_dir, gesture)
        users = [d for d in os.listdir(gesture_dir) 
                if os.path.isdir(os.path.join(gesture_dir, d))]
        
        user_samples = {}
        for user in users:
            user_dir = os.path.join(gesture_dir, user)
            samples = [f for f in os.listdir(user_dir) if f.endswith('.json')]
            user_samples[user] = len(samples)
        
        data_structure[gesture] = user_samples
    
    return data_structure

def handle_remove_readonly(func, path, exc_info):
    """Error handler for shutil.rmtree to handle read-only files on Windows"""
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def manual_delete_directory(path):
    """Manually delete directory by changing permissions and removing files recursively"""
    import stat
    
    if not os.path.exists(path):
        return True
    
    try:
        # First try the normal way
        shutil.rmtree(path, onerror=handle_remove_readonly)
        return True
    except Exception as e:
        print(f"Standard deletion failed for {path}: {e}")
        print("Attempting manual deletion...")
    
    try:
        # Manual recursive deletion - ensure all files and subdirectories are removed
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    # Change permissions and delete file
                    os.chmod(file_path, stat.S_IWRITE)
                    os.unlink(file_path)
                except Exception as e:
                    print(f"Could not delete file {file_path}: {e}")
                    # Try to force delete by changing permissions
                    try:
                        os.chmod(file_path, stat.S_IWRITE)
                        os.unlink(file_path)
                    except:
                        # If still can't delete, try to rename and delete on next run
                        try:
                            temp_name = file_path + ".deleteme"
                            os.rename(file_path, temp_name)
                        except:
                            pass
            
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    # Change permissions and delete directory
                    os.chmod(dir_path, stat.S_IWRITE)
                    # Try to remove directory (will fail if not empty)
                    try:
                        os.rmdir(dir_path)
                    except OSError:
                        # Directory not empty, continue and it will be handled in next iteration
                        pass
                except Exception as e:
                    print(f"Could not delete directory {dir_path}: {e}")
        
        # Finally delete the main directory and all parent directories if they become empty
        try:
            os.chmod(path, stat.S_IWRITE)
            os.rmdir(path)
            
            # Also try to clean up parent directories if they become empty
            parent_dir = os.path.dirname(path)
            while parent_dir and os.path.exists(parent_dir) and not os.listdir(parent_dir):
                os.rmdir(parent_dir)
                parent_dir = os.path.dirname(parent_dir)
                
        except OSError:
            # Directory might not be empty, that's okay
            pass
            
        return True
        
    except Exception as e:
        print(f"Manual deletion failed for {path}: {e}")
        return False

def delete_specific_data(gesture_name=None, user_id=None):
    """Delete specific gesture data by gesture name and/or user ID"""
    data_dir = "advanced_gesture_data"
    
    if not os.path.exists(data_dir):
        print("No advanced gesture data found.")
        return False
    
    gestures_to_delete = []
    users_to_delete = []
    
    # Get all gestures and users
    all_data = list_gestures_and_users()
    
    if gesture_name and user_id:
        # Delete specific user's specific gesture
        user_dir_name = f"user_{user_id}"
        target_dir = os.path.join(data_dir, gesture_name, user_dir_name)
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir, onerror=handle_remove_readonly)
                print(f"✅ Deleted {gesture_name} data for user {user_id}")
                return True
            except Exception as e:
                print(f"❌ Error deleting data: {e}")
                return False
        else:
            print(f"❌ No data found for {gesture_name} - user {user_id}")
            return False
    
    elif gesture_name:
        # Delete all data for a specific gesture
        target_dir = os.path.join(data_dir, gesture_name)
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir, onerror=handle_remove_readonly)
                print(f"✅ Deleted all data for gesture: {gesture_name}")
                return True
            except Exception as e:
                print(f"❌ Error deleting data: {e}")
                return False
        else:
            print(f"❌ No data found for gesture: {gesture_name}")
            return False
    
    elif user_id:
        # Delete all data for a specific user across all gestures
        user_dir_name = f"user_{user_id}"
        deleted_any = False
        for gesture in all_data:
            target_dir = os.path.join(data_dir, gesture, user_dir_name)
            if os.path.exists(target_dir):
                try:
                    shutil.rmtree(target_dir, onerror=handle_remove_readonly)
                    print(f"✅ Deleted {gesture} data for user {user_id}")
                    deleted_any = True
                except Exception as e:
                    print(f"❌ Error deleting {gesture} data for user {user_id}: {e}")
        return deleted_any
    
    else:
        print("❌ Please specify at least a gesture name or user ID")
        return False

def show_data_statistics():
    """Show current data statistics"""
    data = list_gestures_and_users()
    
    if not data:
        print("No data available.")
        return
    
    print("\n=== Current Data Statistics ===")
    total_samples = 0
    total_users = set()
    
    for gesture, users in data.items():
        gesture_samples = sum(users.values())
        total_samples += gesture_samples
        total_users.update(users.keys())
        
        print(f"\nGesture: {gesture}")
        print(f"  Total samples: {gesture_samples}")
        print(f"  Users: {len(users)}")
        for user, count in users.items():
            print(f"    {user}: {count} samples")
    
    print(f"\nOverall Statistics:")
    print(f"Total gestures: {len(data)}")
    print(f"Total unique users: {len(total_users)}")
    print(f"Total samples: {total_samples}")

def list_all_users():
    """List all unique users across all gestures"""
    data = list_gestures_and_users()
    users = set()
    
    for gesture, user_data in data.items():
        users.update(user_data.keys())
    
    return sorted(list(users))

def list_user_data(user_id):
    """List all data for a specific user"""
    data = list_gestures_and_users()
    user_dir_name = f"user_{user_id}"
    user_data = {}
    
    for gesture, user_data_dict in data.items():
        if user_dir_name in user_data_dict:
            user_data[gesture] = user_data_dict[user_dir_name]
    
    return user_data

def main():
    print("=== Selective Data Deletion ===")
    
    while True:
        print("\nOptions:")
        print("1. Show current data statistics")
        print("2. List all users")
        print("3. List data for specific user")
        print("4. Delete data for specific gesture and user")
        print("5. Delete all data for a specific gesture")
        print("6. Delete all data for a specific user")
        print("7. Delete ALL advanced gesture data")
        print("8. Exit")
        
        choice = input("\nChoose an option (1-8): ").strip()
        
        if choice == '1':
            show_data_statistics()
        
        elif choice == '2':
            users = list_all_users()
            if users:
                print("\n=== All Users ===")
                for user in users:
                    print(f"  {user}")
                print(f"\nTotal users: {len(users)}")
            else:
                print("No users found.")
        
        elif choice == '3':
            user_id = input("Enter user ID to list data for: ").strip()
            if user_id:
                user_data = list_user_data(user_id)
                if user_data:
                    print(f"\n=== Data for user_{user_id} ===")
                    total_samples = 0
                    for gesture, count in user_data.items():
                        print(f"  {gesture}: {count} samples")
                        total_samples += count
                    print(f"Total samples: {total_samples}")
                else:
                    print(f"No data found for user_{user_id}")
            else:
                print("❌ User ID is required")
        
        elif choice == '4':
            gesture = input("Enter gesture name to delete: ").strip()
            user = input("Enter user ID to delete: ").strip()
            if gesture and user:
                delete_specific_data(gesture_name=gesture, user_id=user)
            else:
                print("❌ Both gesture name and user ID are required")
        
        elif choice == '5':
            gesture = input("Enter gesture name to delete: ").strip()
            if gesture:
                delete_specific_data(gesture_name=gesture)
            else:
                print("❌ Gesture name is required")
        
        elif choice == '6':
            user = input("Enter user ID to delete: ").strip()
            if user:
                delete_specific_data(user_id=user)
            else:
                print("❌ User ID is required")
        
        elif choice == '7':
            confirmation = input("Delete ALL advanced gesture data? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                data_dir = "advanced_gesture_data"
                if os.path.exists(data_dir):
                    try:
                        # Use manual deletion to ensure all directories are removed
                        success = manual_delete_directory(data_dir)
                        if success:
                            print("✅ Deleted ALL advanced gesture data")
                        else:
                            print("❌ Failed to delete all advanced gesture data")
                    except Exception as e:
                        print(f"❌ Error deleting data: {e}")
                else:
                    print("❌ No advanced gesture data found")
            else:
                print("Operation cancelled.")
        
        elif choice == '8':
            print("Exiting...")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
