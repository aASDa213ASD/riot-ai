import psutil, ctypes
import data, regions, shop, img
from coreAI import CoreAI
from numpy import random
from time import sleep, perf_counter


class Observer(CoreAI):
    champions_list = [img.missfortune, img.ashe]
    summonerSpells_list = [img.summonerspell_barrier, img.summonerspell_cleanse,
                    img.summonerspell_exhaust, img.summonerspell_ghost,
                    img.summonerspell_heal, img.summonerspell_ignite]

    def __init__(self):
        pass
    
    def say(self, message: str):
        print('<Observer>', message)
    
    def update_title(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Game {data.games_finished}/{data.games_to_play}'
        )
    
    def close_process(self, process: str):
        # Might need a small fixes due to the "while.can_see_window('League of Legends')
        if self.can_see_window('League of Legends'):
            try:
                for proc in psutil.process_iter():
                    if proc.name() == process:
                        proc.kill()
                        break
            except Exception as e:
                print(e)
            while self.can_see_window('League of Legends'):
                sleep(1)

    def claim_daily_play(self):
        self.say('Claiming daily play reward')
        claiming_start_time = perf_counter()
        done = False
        while not done:
            sleep(3)
            if (perf_counter() - claiming_start_time) > 30:
                self.close_process('LeagueClientUxRender.exe')
                # FIXME: Kill all UX processes instead of 1
                claiming_start_time = perf_counter()
            self.click_on(img.daily_play_caitlyn, None, leftClick=True)
            self.click_on(img.daily_play_illaoi, None, leftClick=True)
            self.click_on(img.daily_play_ziggs, None, leftClick=True)
            self.click_on(img.daily_play_thresh, None, leftClick=True)
            self.click_on(img.daily_play_ekko, None, leftClick=True)
            self.click_on(img.btn_select, None, leftClick=True)
            done = self.click_on(img.btn_ok, None, leftClick=True)
        return
    
    def add_game(self):
        # Reset ingame vars
        data.ingame = 0
        # Reset shop vars
        data.current_champion = None
        shop.mythic_recipe.clear()
        data.games_finished += 1
        self.update_title()

    def wait_until_client_is_visible(self):
        while not self.find(img.honor_a_teammate, regions.client_header):
            sleep(5)
            if self.find(img.btn_continue, regions.client_footer, leftClick=True):
                break
            if self.find(img.btn_playagain, regions.client_footer, leftClick=True):
                break
            if self.find(img.btn_reconnect, regions.client_body, leftClick=True):
                sleep(10)
                break
            if self.find(img.btn_play, regions.client_header, leftClick=True):
                break
    
    def honor_teammate(self, rect):
        if data.honor_teammates:
            if self.find(img.honor_a_teammate, regions.client_header):
                teammate = random.randint(3)
                self.say(f'Honoring teammate {teammate + 1}')
                self.click(rect[0] + data.honor_coordinates[teammate], rect[1] + 370, lmb=True)

    def champ_select(self):
        self.say('Selecting champion')
        rect = self.get_coords('League of Legends')

        if data.random_champs:
            champion_id = random.randint(6)
            x = rect[0] + data.random_champion[champion_id]; y = rect[1] + 167
            self.click(x, y, lmb=True)
            self.click_on(img.btn_lockin, regions.client_body, leftClick=True)
            return
        
        for champion in self.champions_list:
            print(f'<Debug> {champion}')
            sleep(0.75)
            self.click_on(champion, regions.client_champlist, leftClick=True)
            self.click_on(img.btn_lockin, regions.client_body, leftClick=True)

        # Check if we are still in champ select
        if self.find(img.pick_your_champion, regions.client_header):
            self.say('Stack, choosing random champion')
            self.click_on(img.btn_ok_bug, None, leftClick=True)
            champion_id = random.randint(6)
            x = rect[0] + data.random_champion[champion_id]; y = rect[1] + 167
            self.click(x, y, lmb=True)
            self.click_on(img.btn_lockin, regions.client_body, leftClick=True)
            return

    def set_runes_and_summs(self):
        if data.random_runes:
            self.say('Setting runes')
            rect = self.get_coords('League of Legends')
            coordinates = self.find(img.btn_newrunes, regions.client_footer)
            if coordinates is not None:
                # Open runes
                self.click(coordinates[0], coordinates[1], lmb=True)
                sleep(2) # Wait to load, delay is not enough
                x = rect[0] + data.random_rune[random.randint(3)]; y = rect[1] + 326
                self.click(x, y, lmb=True)
                sleep(1)
                self.click_on(img.btn_close, regions.client_close_runes, leftClick=True) 
        else:
            self.set_summoner_spells()

    def set_summoner_spells(self):
        if data.random_summs:
            self.say('Setting summs')
            coordinates = self.find(img.btn_editrunes, regions.client_footer)
            if coordinates is not None:
                # Select flash
                self.click(coordinates[0], coordinates[1], x_align=300, lmb=True)
                sleep(2) # Wait to load, delay is not enough
                self.click_on(img.summonerspell_flash, regions.summoner_spell_select, leftClick=True, delay=True)
                # Select random
                self.click(coordinates[0], coordinates[1], x_align=250, lmb=True)
                spell = random.randint(5)
                sleep(2)
                self.click_on(self.summonerSpells_list[spell], regions.summoner_spell_select, leftClick=True)
