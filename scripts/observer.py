import psutil, ctypes
import data, regions, shop, img
from coreAI import CoreAI
from numpy import random
from time import sleep, perf_counter, time

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
        data.ingame = 0
        data.current_champion = None
        shop.mythic_recipe.clear()
        data.games_finished += 1
        self.update_title()

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
    
    def wait_for_client(self):
        while not self.find(img.honor_a_teammate, regions.client_header):
            sleep(5)
            if self.click_on(img.btn_continue, regions.client_footer, leftClick=True):
                break
            if self.click_on(img.btn_playagain, regions.client_footer, leftClick=True):
                break
            if self.click_on(img.btn_play, regions.client_header, leftClick=True):
                break
            if self.click_on(img.btn_ok, regions.client_footer):
                break
            if self.click_on(img.btn_reconnect, regions.client_body, leftClick=True):
                sleep(10)
                break
    
    def accept_game(self):
        while self.click_on(img.btn_close_rewards, regions.client_body, leftClick=True):
            self.say('Closing rewards windows')
            sleep(1)

        while not self.click_on(img.btn_accept, regions.client_body, leftClick=True):
            if not self.click_on(img.btn_findmatch, regions.client_footer, leftClick=True):
                if self.find(img.btn_inqueue, regions.client_footer):
                    continue
                elif self.find(img.pick_your_champion, regions.client_header):
                    self.champ_select()
                    self.set_runes_and_summs()
                else:
                    break
    
    def handle_lobby(self):
        if self.click_on(img.gamemode_training, None, leftClick=True):
            if data.game_mode == 'COOP_VS_AI':
                if self.click_on(img.gamemode_coopvsai, None, leftClick=True, delay=True):
                    if data.game_queue == 'INTRO':
                        if self.click_on(img.queue_intro, None, leftClick=True):
                            self.click_on(img.btn_confirm, None, leftClick=True)
                    elif data.game_queue == 'BEGINNER':
                        if self.click_on(img.queue_beginner, None, leftClick=True):
                            self.click_on(img.btn_confirm, None, leftClick=True)
                    elif data.game_queue == 'INTERMEDIATE':
                        if self.click_on(img.queue_intermediate, None, leftClick=True):
                            self.click_on(img.btn_confirm, None, leftClick=True)

            elif data.game_mode == 'PVP':
                if self.click_on(img.gamemode_pvp, None, leftClick=True, delay=True):
                    if data.game_map == 'ARAM':
                        if self.click_on(img.map_aram, None, leftClick=True):
                            self.click_on(img.btn_confirm, None, leftClick=True)
        
    def handle_stuck(self):
        self.say('Idle detected, restarting UX...')
        self.close_process('LeagueClientUx.exe')

        while not self.can_see_window('League of Legends'):
            sleep(10)
            
        self.click_on(img.btn_close, regions.client_email_verification, leftClick=True)
        self.click_on(img.btn_close, regions.client_footer, leftClick=True, conf=0.7)
