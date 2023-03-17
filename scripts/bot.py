import data, img, regions, utils
from shop import Shop, shop_do
from observer import Observer
from player import Player
from time import time, sleep, perf_counter

observer = Observer()
player = Player()
shop = Shop()

# TODO: Rewrite ludens recipe in shop.py
# TODO: Implement ahri as a champ, or any other mage like brand
# TODO: Implement account_level_cap in settings
# TODO: Test for infinity cycling

def run():
    observer.update_title()
    while True:
        time_start = perf_counter()
        if observer.can_see_window('League of Legends (TM) Client'):
            play()
        
        if observer.find(img.honor_a_teammate, regions.client_header):
            observer.honor_teammate(observer.get_coords('League of Legends'))
        
        observer.click_on(img.btn_ok, regions.client_footer, leftClick=True)
        observer.click_on(img.btn_close, regions.client_email_verification, leftClick=True)

        if observer.find(img.daily_play, None):
            observer.claim_daily_play()
        
        if (observer.click_on(img.btn_continue, regions.client_footer)
            or observer.click_on(img.btn_playagain, regions.client_footer)):
                observer.click_on(img.btn_close, regions.client_footer, leftClick=True, conf=0.7)
        
        observer.click_on(img.btn_play, regions.client_header, leftClick=True)
        handle_lobby()
        accept_game()
     
        time_end = perf_counter()
        print('<Client> %f' % (time_end - time_start))


def play():
    print('<Game> Loading screen...')
    
    while not player.find(img.interface_settings, None, is_game=True, conf=0.7):
        sleep(3)
    
    coordinates = None
    gametime = perf_counter()
    rect = player.get_coords('League of Legends (TM) Client')
    player.lock_screen()

    shop.identify_champion()
    shop.define_build()

    shop_do('setup_interface')
    shop_do('buy_first')
    shop_do('select_mythic_item')

    while True:
        start = perf_counter()

        if not observer.can_see_window('League of Legends (TM) Client'):
            break
        
        if observer.can_see_window('GPU Error'):
            sleep(2)
            if observer.click_on(img.btn_ok_gpu, None, leftClick=True, conf=0.9):
                sleep(5)
                observer.close_process('League of Legends (TM) Client')

        if not player.is_dead():
            if not player.needs_recall():
                if not player.is_in_turret_range(
                    regions.turret_1) and not player.is_in_turret_range(regions.turret_2):
                        if not player.has_enemy_nearby(rect):
                            if not player.has_minions_nearby():
                                if not player.minions_spawned(gametime):
                                    player.click_mid_safe(rect)
                                else:
                                    player.click_mid(rect)
                            else:
                                coordinates = player.find(img.healthbar_minion, regions.enemy_location_nearby, is_game=True)
                                if coordinates is not None:
                                    player.cast_skill(coordinates[0], coordinates[1] + 25)
                else:
                    player.kite_back(rect)
            else:
                player.panic(rect)
                player.recall(rect)
                shop_do('buy_build')
        else:
            player.click(rect[0] + 1240, rect[1] + 360)
            shop_do('buy_build')

        player.upgrade_skills()

        end = perf_counter()
        print("<Game> %f" % (end - start))

    observer.add_game()

    while not observer.find(img.honor_a_teammate, regions.client_header):
        sleep(5)
        if observer.click_on(img.btn_continue, regions.client_footer, leftClick=True):
            break
        if observer.click_on(img.btn_playagain, regions.client_footer, leftClick=True):
            break
        if observer.click_on(img.btn_reconnect, regions.client_body, leftClick=True):
            sleep(10)
            break
        if observer.click_on(img.btn_play, regions.client_header, leftClick=True):
            break
    
    if data.games_finished == data.games_to_play:
        observer.close_process('LeagueClient.exe')
        stop_bot()


def accept_game():
    while observer.click_on(img.btn_close_rewards, regions.client_body, leftClick=True):
        observer.say('Closing rewards windows')
        sleep(1)

    while not observer.click_on(img.btn_accept, regions.client_body, leftClick=True):
        if not observer.click_on(img.btn_findmatch, regions.client_footer, leftClick=True):
            if observer.find(img.btn_inqueue, regions.client_footer):
                continue
            elif observer.find(img.pick_your_champion, regions.client_header):
                observer.champ_select()
                observer.set_runes_and_summs()
            else:
                break


def handle_lobby():
    if observer.click_on(img.gamemode_training, None, leftClick=True):
        if data.game_mode == 'COOP_VS_AI':
            if observer.click_on(img.gamemode_coopvsai, None, leftClick=True, delay=True):
                if data.game_queue == 'INTRO':
                    if observer.click_on(img.queue_intro, None, leftClick=True):
                        observer.click_on(img.btn_confirm, None, leftClick=True)
                elif data.game_queue == 'BEGINNER':
                    if observer.click_on(img.queue_beginner, None, leftClick=True):
                        observer.click_on(img.btn_confirm, None, leftClick=True)
                elif data.game_queue == 'INTERMEDIATE':
                    if observer.click_on(img.queue_intermediate, None, leftClick=True):
                        observer.click_on(img.btn_confirm, None, leftClick=True)

        elif data.game_mode == 'PVP':
            if observer.click_on(img.gamemode_pvp, None, leftClick=True, delay=True):
                if data.game_map == 'ARAM':
                    if observer.click_on(img.map_aram, None, leftClick=True):
                        observer.click_on(img.btn_confirm, None, leftClick=True)


def stop_bot():
    print('Bot has been stopped.')
    while True:
        sleep(3)
