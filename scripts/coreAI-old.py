import win32api, win32con, win32gui, pyautogui
import data
from time import sleep
from pywinauto.findwindows import find_window
from os import path

# Line 67 TypeError: 'bool' object is not subscriptable (coordinates)

class CoreAI:
    def __init__(self):
        pass

    def can_see_window(self, window: str):
        try:
            find_window(title = window)
            return True
        except Exception:
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
        
            if region is not None:
                start_x = rect[0] + region[0]
                start_y = rect[1] + region[1]
                width = rect[0] + region[2]
                height = rect[1] + region[3]
                rect = (start_x, start_y, width, height)
                coordinates = pyautogui.locateCenterOnScreen(picture, region=rect, confidence=conf)
            else:
                coordinates = pyautogui.locateCenterOnScreen(picture, confidence=conf)
            
            return coordinates
        except Exception as e:
            print(e)
        return False
    
    def click_on(self, picture, region, is_game=False, shop_file_path=False, leftClick=False, rightClick=False, x_align=0, y_align=0, delay=False, conf=0.95):
        coordinates = self.find(picture, region, is_game, shop_file_path, conf)
        if coordinates is not None:
            if leftClick:
                ...
                #self.click(coordinates[0] + x_align, coordinates[1] + y_align, lmb=True)
            elif rightClick:
                ...
                #self.click(coordinates[0] + x_align, coordinates[1] + y_align, rmb=True)
            if delay:   
                sleep(1)
            return True
        return False