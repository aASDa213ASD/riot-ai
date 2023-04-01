import win32api, win32con, win32gui, mss, cv2
import numpy as np
import data
from time import sleep
from os import path

class CoreAI:
    def __init__(self):
        pass
    
    def locate(self, image, region, confidence=0.95):
        x = y = 0
        image = cv2.imread(image)

        with mss.mss() as sct:
            if region:
                screen = sct.grab(monitor=region)
                x += region[0]
                y += region[1]
            else:
                monitor = {"top": 0, "left": 0, "width": 1280, "height": 1024}  
                screen = sct.grab(monitor=monitor)
            screen = np.array(screen)

        if image.shape[0] > screen.shape[0] or image.shape[1] > screen.shape[1]:
            return None

        image_height, image_width, _ = image.shape

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < confidence:
            return None
        
        x += max_loc[0] + image_width // 2
        y += max_loc[1] + image_height // 2
        return x, y

    def can_see_window(self, window: str):
        hwnd = win32gui.FindWindow(None, window)
        if hwnd:
            return True
        return False

    def get_coords(self, window: str):
        hwnd = win32gui.FindWindow(None, window)
        rect = win32gui.GetWindowRect(hwnd)
        return rect

    def click(self, x, y, x_align=0, y_align=0, lmb=False, rmb=False):
        win32api.SetCursorPos((x + x_align, y + y_align))
        if (lmb):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x + x_align, y, 0, 0)
            sleep(0.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x + y_align, y, 0, 0)
        elif (rmb):
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x + x_align, y, 0, 0)
            sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x + y_align, y, 0, 0)
    
    def find(self, picture, region, is_game=False, shop_file_path=False, conf=0.95):
        if shop_file_path:
            picture = path.join(data.shop_path, picture)
        else:
            picture = path.join(data.picture_path, picture)
        
        try:
            if is_game:
                rect = self.get_coords('League of Legends (TM) Client')
            else:
                rect = self.get_coords('League of Legends') 
            
            if region:
                start_x = rect[0] + region[0]
                start_y = rect[1] + region[1]
                width = rect[0] + region[2]
                height = rect[1] + region[3]
                rect = (start_x, start_y, width, height)
                coordinates = self.locate(picture, rect, conf)
            else:
                coordinates = self.locate(picture, rect, conf)
            
            return coordinates
        except Exception as e:
            print(e)
        return False
    
    def click_on(self, picture, region, is_game=False, shop_file_path=False, leftClick=False, rightClick=False, x_align=0, y_align=0, delay=False, conf=0.95):
        coordinates = self.find(picture, region, is_game, shop_file_path, conf)
        if coordinates:
            if leftClick:
                self.click(coordinates[0] + x_align, coordinates[1] + y_align, lmb=True)
            elif rightClick:
                self.click(coordinates[0] + x_align, coordinates[1] + y_align, rmb=True)
            if delay:   
                sleep(1)
            return True
        return False
