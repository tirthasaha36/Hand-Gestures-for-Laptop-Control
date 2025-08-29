import pyautogui
import time

class SystemController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_click_time = 0
        self.click_cooldown = 0.5  # seconds between clicks
        
    def move_cursor(self, x, y):
        """Move cursor to normalized coordinates (0-1 range)"""
        screen_x = int(x * self.screen_width)
        screen_y = int(y * self.screen_height)
        pyautogui.moveTo(screen_x, screen_y, duration=0.1)
        
    def left_click(self):
        """Perform left click with cooldown"""
        current_time = time.time()
        if current_time - self.last_click_time > self.click_cooldown:
            pyautogui.click()
            self.last_click_time = current_time
            return True
        return False
        
    def right_click(self):
        """Perform right click with cooldown"""
        current_time = time.time()
        if current_time - self.last_click_time > self.click_cooldown:
            pyautogui.rightClick()
            self.last_click_time = current_time
            return True
        return False
        
    def scroll(self, direction):
        """Scroll up or down"""
        if direction == "up":
            pyautogui.scroll(100)
        elif direction == "down":
            pyautogui.scroll(-100)
            
    def volume_up(self):
        """Increase system volume"""
        pyautogui.press('volumeup')
        
    def volume_down(self):
        """Decrease system volume"""
        pyautogui.press('volumedown')
        
    def play_pause(self):
        """Toggle play/pause media"""
        pyautogui.press('playpause')
        
    def next_track(self):
        """Skip to next track"""
        pyautogui.press('nexttrack')
        
    def previous_track(self):
        """Go to previous track"""
        pyautogui.press('prevtrack')
        
    def zoom_in(self):
        """Zoom in (Ctrl + Plus)"""
        pyautogui.hotkey('ctrl', '+')
        
    def zoom_out(self):
        """Zoom out (Ctrl + Minus)"""
        pyautogui.hotkey('ctrl', '-')
        
    def swipe_left(self):
        """Swipe left gesture (Alt + Left arrow)"""
        pyautogui.hotkey('alt', 'left')
        
    def swipe_right(self):
        """Swipe right gesture (Alt + Right arrow)"""
        pyautogui.hotkey('alt', 'right')
