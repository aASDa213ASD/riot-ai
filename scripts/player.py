import win32api, win32con
import regions, pictures
from pictures_shop import health_potion
from coreAI import CoreAI
from time import sleep, perf_counter
from numpy import random
from ahk import AHK
from random import randint

ahk = AHK()

class Player(CoreAI):
    skills = ['q', 'w', 'e', 'r']
    levelup_skills = ['v', 'x', 'z', 'c']
    clicks_amount = clicks_made = 0
    x = y = 0

    def __init__(self):
        pass

    def click_mid(self, rect):
        # Blue side mid coordinates
        self.x = rect[0] + 1241
        self.y = rect[1] + 596
        self.clicks_amount = random.randint(1, 4)
        self.clicks_made = 0
        ahk.key_down('Shift')
        win32api.SetCursorPos((self.x, self.y))
        while self.clicks_made < self.clicks_amount:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.x, self.y, 0, 0)
            sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.x, self.y, 0, 0)
            self.clicks_made += 1
            sleep(self.clicks_made/100)
        ahk.key_up('Shift')
    
    def click_mid_safe(self, rect):
        random_coordinate = randint(1, 5)
        self.x = rect[0] + 1190
        self.y = rect[1] + 648 - random_coordinate
        self.click(self.x, self.y, rmb=True)

    def is_in_turret_range(self, region_turret):
        if self.find(pictures.turret, region_turret, is_game=True, conf=0.9) is not None:
            print("Turret aware")
            return True
        return False

    def kite_back(self, rect, attackmove=False):
        # Blue mapside kiting coordinates
        self.x = rect[0] + 495
        self.y = rect[1] + 460
        win32api.SetCursorPos((self.x, self.y))
        if attackmove:
            ahk.key_down('Shift')
            self.click(self.x, self.y, rmb=True)
            ahk.key_up('Shift')
        self.click(self.x, self.y, rmb=True)

    def cast_skill(self, x, y):
        desire = random.randint(10)
        skill_id = random.randint(3)

        if desire > 4:
            win32api.SetCursorPos((x, y))
            ahk.key_down(self.skills[skill_id])
            sleep(0.1)
            ahk.key_up(self.skills[skill_id])
            return True # Do I really need to return anything?
        return False # Do I really need to return anything?

    def lock_screen(self):
        self.click_on(pictures.cam, None, is_game=True, leftClick=True)

    def is_dead(self):
        if self.find(pictures.death, regions.health_bar, is_game=True):
            return False
        return True

    def needs_recall(self):
        if self.find(pictures.low_hp, regions.hud, is_game=True) is None:
            return True
        return False

    def panic(self, rect):
        self.x = rect[0] + 341
        self.y = rect[1] + 561
        self.click(self.x, self.y, rmb=True)
        self.use_summoner_spell('f')

        if self.find(pictures.heal, regions.hud, is_game=True, conf=0.7):
            self.use_summoner_spell('d')
        elif self.find(health_potion, regions.inventory, is_game=True, shop_file_path=True, conf=0.7):
            self.use_health_potion()

    def recall(self, rect):
        # Kiting back to safe distance
        for i in range(3):
            self.click(self.x, self.y, rmb = True)
            sleep(1.5)
        # Recalling and looking for enemies
        if not self.is_dead():
            print('Recall')
            recall_start_time = perf_counter()
            ahk.key_press('b')
            while not perf_counter() - recall_start_time > 12:
                sleep(0.5)
                if self.find(pictures.enemy_hpbar, regions.enemy_location_far, is_game=True, conf=0.9):
                    self.recall(rect)
            self.click(rect[0] + 1240, rect[1] + 360)

    def use_health_potion(self):
        self.click_on(health_potion, regions.inventory, is_game=True, leftClick=True, shop_file_path=True, conf=0.7)
        sleep(0.25)
        return True

    def use_summoner_spell(self, key):
        ahk.key_press(key)
        return True

    def has_enemy_nearby(self, rect):
        while self.find(pictures.enemy_hpbar, regions.enemy_location_far, is_game=True, conf=0.9):
            if self.is_dead():
                break
            print('Spacegliding')
            if not self.needs_recall():
                self.kite_back(rect, attackmove=True)
                sleep(0.3)
            self.kite_back(rect)
            sleep(0.3)
        return False

    def has_minions_nearby(self):
        if self.click_on(pictures.minion_hpbar, regions.enemy_location_far, is_game=True, rightClick=True, y_align=25):
            return True
        return False

    def minions_spawned(self, gametime):
        if perf_counter() - gametime > 97:
            return True
        return False

    def upgrade_skills(self):
        for i in self.levelup_skills:
            ahk.key_press(i)
            sleep(0.05)
