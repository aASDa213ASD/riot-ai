import data, img, regions, utils
from shop import Shop, shop_do
from observer import Observer
from player import Player
from time import time, sleep, perf_counter

observer = Observer()
player = Player()
shop = Shop()

# GAMEPLAY TASKS:
# TODO: 1. Test for infinite cycle
#           1.1. [Fixed] Fix STUCK when the game ends and account levels up at the same time
#                it doesn't see the OK button and gets stuck
#           1.2. Sometimes LeagueClient is stopping responding and targets as the
#                main window which confuses the bot, makes it AFK and think that the game is still going
#           1.3. [Fixed] Sometimes when new lobby is created "Find match" button is gray and inactive, lobby is stuck
# 
# TODO: 2. Improve general gameplay mechanics {
#       Recall - should first check for enemies and recall after.
#       Because now it Recalls, checks for enemies -> run, recall - check for enemies
#       Should be like if enemies nearby - run until they are not (constantly check while recalling)
#       So there's no situations where the bot stops for recall while the enemy is running on him (high death chance)
#       }
# TODO: 3. Implement other champs from start pool
# TODO: 4. 
# SHOP TASKS:
# FIXME: 1. Rewrite ludens recipe in shop.py
# TODO: 2. Implement cookies usage
# GENERAL TASKS:
# TODO: Implement account_level_cap in settings
# TODO: Separate gameplay functions for different modes like PVP/COOP_VS_AI
# MISSION IMPOSSIBLE:
# FIXME: Add separate gameplay functions for certain champion to fully
#        abuse champion's mechanics, like Irelia's wave clear, draven axe catching, etc.

def run():
    observer.update_title()
    while True:
        time_start = perf_counter()
        time_idle_elapsed = time() - data.time_idle

        if observer.can_see_window('League of Legends (TM) Client'):
            play()
            data.time_idle = time()
        
        if observer.find(img.honor_a_teammate, regions.client_header):
            observer.honor_teammate(observer.get_coords('League of Legends'))

        if time_idle_elapsed >= data.time_max_idle:
            observer.handle_stuck()
            data.time_idle = time()

        observer.click_on(img.btn_ok, regions.client_footer, leftClick=True)
        observer.click_on(img.btn_close, regions.client_email_verification, leftClick=True)

        if observer.find(img.daily_play, None):
            observer.claim_daily_play()
        
        if (observer.click_on(img.btn_continue, regions.client_footer)
            or observer.click_on(img.btn_playagain, regions.client_footer)):
                observer.click_on(img.btn_close, regions.client_footer, leftClick=True, conf=0.7)
        
        observer.click_on(img.btn_play, regions.client_header, leftClick=True)
        observer.handle_lobby()
        observer.accept_game()
     
        time_end = perf_counter()
        print(f'<Client> {(time_end - time_start):.3f}')


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
                                if coordinates:
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
    observer.wait_for_client()
    
    if data.games_finished == data.games_to_play:
        observer.close_process('LeagueClient.exe')
        stop_bot()


def stop_bot():
    print('Bot has been stopped.')
    while True:
        sleep(3)
