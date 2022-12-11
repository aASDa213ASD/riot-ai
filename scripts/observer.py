import psutil, ctypes
import data, pictures, regions, shop
from coreAI import CoreAI
from numpy import random
from time import sleep, perf_counter


class Observer(CoreAI):
    #pictures.ahri
    champions_list = [pictures.missfortune, pictures.ashe]
    summonerSpells_list = [pictures.summonerspell_barrier, pictures.summonerspell_cleanse,
                    pictures.summonerspell_exhaust, pictures.summonerspell_ghost,
                    pictures.summonerspell_heal, pictures.summonerspell_ignite]

    def __init__(self):
        pass

    def update_title(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
        f'Level {data.account_level}, Game {data.games_finished}/{data.games_to_play}'
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
        print("Claiming daily play reward")
        claiming_start_time = perf_counter()
        done = False
        while not done:
            sleep(3)
            if (perf_counter() - claiming_start_time) > 30:
                self.close_process('LeagueClientUxRender.exe')
                # FIXME: Kill all UX processes instead of 1
                claiming_start_time = perf_counter()
            self.click_on(pictures.daily_play_caitlyn, None, leftClick=True)
            self.click_on(pictures.daily_play_illaoi, None, leftClick=True)
            self.click_on(pictures.daily_play_ziggs, None, leftClick=True)
            self.click_on(pictures.daily_play_thresh, None, leftClick=True)
            self.click_on(pictures.daily_play_ekko, None, leftClick=True)
            self.click_on(pictures.select_daily, None, leftClick=True)
            done = self.click_on(pictures.ok_daily, None, leftClick=True)
        return
    
    def add_game(self):
        # Reset ingame vars
        data.ingame = 0
        data.prepared_to_fight = False
        # Reset shop vars
        data.current_champion = None
        shop.mythic_recipe.clear()
        data.games_finished += 1
        self.update_title()   

    def wait_until_client_is_visible(self):
        while not self.find(pictures.honor_a_teammate, regions.choose_champ):
            sleep(5)
            if self.find(pictures.continue_button, regions.find_match, leftClick=True):
                break
            if self.find(pictures.play_again, regions.find_match, leftClick=True):
                break
            if self.find(pictures.reconnect, regions.reconnect, leftClick=True):
                sleep(10)
                break
            if self.find(pictures.play_button, regions.play_button, leftClick=True):
                break
    
    def honor_teammate(self, rect):
        if self.find(pictures.honor_a_teammate, regions.choose_champ):
            teammate = random.randint(3)
            print(f'Honoring teammate {teammate + 1}')
            self.click(rect[0] + data.honor_coordinates[teammate], rect[1] + 370, lmb=True)

    def champ_select(self):
        print('Entering champ select')
        rect = self.get_coords('League of Legends')

        for champion in self.champions_list:
            print(champion)
            sleep(0.75)
            self.click_on(champion, regions.champ_select, leftClick=True)
            self.click_on(pictures.lockin, regions.lockin, leftClick=True)

        # Check if we are still in champ select
        if self.find(pictures.choose_champ, regions.choose_champ):
            print('Still in champ select')
            self.click_on(pictures.ok_champ_select_bug, None, leftClick=True)
            self.click_on(pictures.close_email, None, leftClick=True)
            champion_id = random.randint(6)
            x = rect[0] + data.random_champion[champion_id]; y = rect[1] + 167
            self.click(x, y, lmb=True)
            self.click_on(pictures.lockin, regions.lockin, leftClick=True)
            return

    def set_summoner_spells(self):
        print('Looking for summoner spells')
        coordinates = self.find(pictures.edit_runes, regions.summoner_spells)
        if coordinates is not None:
            # Select flash
            self.click(coordinates[0], coordinates[1], x_align=300, lmb=True)
            sleep(2) # Wait to load, delay is not enough
            self.click_on(pictures.summonerspell_flash, regions.summoner_spell_select, leftClick=True) 

            sleep(1)

            # Select random
            self.click(coordinates[0], coordinates[1], x_align=250, lmb=True)
            spell = random.randint(5)
            sleep(2)
            self.click_on(self.summonerSpells_list[spell], regions.summoner_spell_select, leftClick=True)
            data.prepared_to_fight = True
    
    # def open_client(self):
    #     try:
    #         subprocess.Popen(lol_client_path)
    #     except Exception:
    #         print("Couldn't open league client")
