import pictures_shop, regions, data
from observer import Observer
from ahk import AHK
from itertools import takewhile
from configparser import ConfigParser
from os import getcwd, path
from time import sleep

mythic_recipe = []
observer = Observer()
ahk = AHK()
builds = ConfigParser()

class Recipes(object):
    def find_recipe(self, mythicItem):
        method_name = str(mythicItem) + '_recipe'
        method = getattr(self, method_name, lambda :'Invalid')
        return method()

    def shieldbow_recipe(self):
        print("Using shieldbow recipe")
        mythic_recipe.append(pictures_shop.noonquiver)
        mythic_recipe.append(pictures_shop.vampiric_scepter)
        mythic_recipe.append(pictures_shop.cloak_of_agility)

    def krakenslayer_recipe(self):
        print("Using krakenslayer recipe")
        mythic_recipe.append(pictures_shop.noonquiver)
        mythic_recipe.append(pictures_shop.pickaxe)
        mythic_recipe.append(pictures_shop.cloak_of_agility)

    def ludens_recipe(self):
        print("Using ludens tempest recipe")
        mythic_recipe.append(pictures_shop.lost_chapter)
        mythic_recipe.append(pictures_shop.blasting_wand)
        mythic_recipe.append(pictures_shop.boots) # idk

class Shop(object):
    def execute(self, action):
        method = getattr(self, str(action), lambda :'Invalid')
        return method()
    
    def is_shop_available(self):
        if observer.find(pictures_shop.shop_is_available, regions.inventory, is_game=True, shop_file_path=True):
            return True
        return False
    
    def keypress(self):
        ahk.key_press('p')
        sleep(1)
    
    def check_inventory_for(self, item):
        if observer.find(item, regions.inventory, is_game=True, shop_file_path=True, conf=0.6):
            return True
        return False
    
    def setup_interface(self):
        observer.click_on(pictures_shop.all_items, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8)
        observer.click_on(pictures_shop.no_sort, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8)
    
    def identify_champion(self):
        if data.current_champion is None:
            for champion in observer.champions_list:
                print('?', champion)
                if observer.find(champion, regions.hud, is_game=True, conf=0.7):
                    champion_name = "".join(takewhile(lambda x: x!=".", champion))
                    data.current_champion = champion_name
                    return
                else:
                    data.current_champion = None
    
    def define_build(self):
        if data.current_champion is not None:
            builds.read(path.join(getcwd(), f"champions\\{data.current_champion}.ini"))
            build = builds['Build']
            data.build_firstItem = build['firstItem']
            data.build_potionsAmount = build.getint('potionsAmount')
            data.build_mythicItem = build['mythicItem']
            data.build_bootsItem = build['bootsItem']
            recipe.find_recipe(data.build_mythicItem)
    
    def buy_first(self):
        if data.current_champion is not None:
            if observer.click_on(f"{data.build_firstItem}.png", regions.shop_items, is_game=True, rightClick=True, shop_file_path=True, conf=0.8):
                if (data.build_potionsAmount is not 0):
                    for i in range(data.build_potionsAmount):
                        observer.click_on(pictures_shop.health_potion, regions.shop_utils, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
                        sleep(0.1)
                observer.click_on(pictures_shop.stealth_ward, regions.shop_utils, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
                return
            else:
                observer.click_on(pictures_shop.swap_shop, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8); sleep(1)
                self.buy_first()
        else:
            self.buy_recommended(stealthWard=True)
    
    def buy_recommended(self, stealthWard=False):
        observer.click_on(pictures_shop.recommended, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8)
        observer.click_on(pictures_shop.generally_good, regions.shop_items, is_game=True, rightClick=True, shop_file_path=True, delay=True, conf=0.8)
        if stealthWard:
            observer.click_on(pictures_shop.stealth_ward, regions.shop_utils, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)

    def select_mythic_item(self):
        if data.current_champion is not None:
            if not self.check_inventory_for(f"{data.build_mythicItem}.png"):
                if observer.click_on(f"{data.build_mythicItem}.png", regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, conf=0.8):
                    sleep(1)
                    pass
                else:
                    observer.click_on(pictures_shop.all_items, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8)
                    observer.click_on(pictures_shop.swap_shop, regions.shop_items, is_game=True, leftClick=True, shop_file_path=True, delay=True, conf=0.8)
                    sleep(1)
                    self.select_mythic_item()
    
    def buy_build(self):
        if data.current_champion is not None:
            if not self.check_inventory_for(f"{data.build_bootsItem}.png"):
                if not self.check_inventory_for(pictures_shop.boots): # Buy boots first
                    observer.click_on(pictures_shop.boots, None, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
            if not self.check_inventory_for(f"{data.build_mythicItem}.png"):
                if not self.check_inventory_for(mythic_recipe[0]):
                    observer.click_on(mythic_recipe[0], regions.shop_craft, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
                if not self.check_inventory_for(mythic_recipe[1]):
                    observer.click_on(mythic_recipe[1], regions.shop_craft, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
                if not self.check_inventory_for(mythic_recipe[2]):
                    observer.click_on(mythic_recipe[2], regions.shop_craft, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
                # Try buying mythic
                observer.click_on(f"{data.build_mythicItem}_buy.png", regions.shop_craft, is_game=True, rightClick=True, shop_file_path=True, conf=0.5)
            elif not self.check_inventory_for(f"{data.build_bootsItem}.png"): # Buy desired boots
                observer.click_on(f"{data.build_bootsItem}.png", regions.shop_boots, is_game=True, rightClick=True, shop_file_path=True, conf=0.8)
            else: self.buy_recommended()
        else: self.buy_recommended()

recipe = Recipes()
shop = Shop()

def shop_do(action):
    if shop.is_shop_available():
        shop.keypress()
        shop.execute(action)
        shop.keypress()