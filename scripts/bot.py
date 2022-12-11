import data, utils, pictures, regions
from shop import Shop, shop_do
from observer import Observer
from player import Player
from time import time, sleep, perf_counter

observer = Observer()
player = Player()
shop = Shop()

# TODO: Rewrite ludens recipe in shop.py
# TODO: Add ahri in observer.championslist
# TODO: Set custom level in settings.ini (-1, 10, 30 was needed so far)


def run():
    while True:
        start = perf_counter()

        if time() - data.account_level_last_check > 3600:
            try:
                utils.get_account_level()
                observer.update_title()
            except Exception:
                pass

        if observer.can_see_window('League of Legends (TM) Client'):
            play()
            continue

        if data.level_check_flag: # TODO: Rewrite
            if observer.find(pictures.level_30, regions.account_level) is not None:
                print('Level 30 reached !')
                observer.close_process('League of Legends')
                stop_bot()

        if observer.find(pictures.daily_play, None) is not None:
            observer.claim_daily_play()

        observer.click_on(pictures.ok, regions.level_up_ok, leftClick=True)
        observer.click_on(pictures.close_email, regions.email_verification, leftClick=True)
        observer.click_on(pictures.close_challenges, regions.close_challenges, leftClick=True)

        if not observer.click_on(pictures.play_button, regions.play_button, leftClick=True, delay=True):
            observer.click_on(pictures.party, regions.play_button, leftClick=True, delay=True)

        if observer.click_on(
            pictures.players_are_not_ready, regions.lobby_status
            ) or observer.click_on(pictures.players_are_not_ready_2, regions.lobby_status):
            # Create new queue due to a bug with lane selection on intro bots
            observer.click_on(pictures.close_email, regions.lobby_status, leftClick=True, conf=0.7)

        observer.click_on(pictures.coop_vs_ai, regions.game_mode_select, leftClick=True, delay=True)

        if observer.click_on(pictures.intro_bots, regions.intro_bots, leftClick=True):
            observer.click_on(pictures.confirm, regions.confirm, leftClick=True)
        else:
            pass

        if observer.click_on(pictures.continue_button, regions.find_match, delay=True):
            # Create new queue due to a bug with lane selection on intro bots
            observer.click_on(pictures.close_email, regions.lobby_status, leftClick=True, conf=0.7)

        observer.click_on(pictures.play_again, regions.find_match, leftClick=True, delay=True) # Needed ?

        accept_game()

        end = perf_counter()
        print('[Client] %f' % (end - start))


def play():
    print('[Game] Loading screen...')
    while not player.find(pictures.settings, None, is_game=True, conf=0.7):
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
            if observer.click_on(pictures.gpu_error_ok, None, leftClick=True, conf=0.9):
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
                                coordinates = player.find(pictures.minion_hpbar, regions.enemy_location_nearby, is_game=True)
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
        print("[Game] %f" % (end - start))

    observer.add_game()

    # Wait until client is visible
    while not observer.find(pictures.honor_a_teammate, regions.choose_champ):
        sleep(5)
        if observer.click_on(pictures.continue_button, regions.find_match, leftClick=True):
            break
        if observer.click_on(pictures.play_again, regions.find_match, leftClick=True):
            break
        if observer.click_on(pictures.reconnect, regions.reconnect, leftClick=True):
            sleep(10)
            break
        if observer.click_on(pictures.play_button, regions.play_button, leftClick=True):
            break
    
    # Honor a teammate
    rect = observer.get_coords('League of Legends')
    observer.honor_teammate(rect)
    
    # Check if bot finished all games
    if data.games_finished == data.games_to_play:
        observer.close_process('LeagueClient.exe')
        stop_bot()


def accept_game():
    print('[Debug] accept_game')
    observer.click_on(pictures.close_challenges, regions.close_challenges, leftClick=True)

    while not observer.click_on(pictures.accept, regions.accept, leftClick=True):
        if not observer.click_on(pictures.find_match_hover, regions.find_match, leftClick=True):
            if observer.find(pictures.in_queue, regions.find_match) is not None:
                continue
            elif observer.find(pictures.choose_champ, regions.choose_champ) is not None:
                observer.champ_select()
                if data.prepared_to_fight is False:
                    observer.set_summoner_spells()
            else:
                break


def stop_bot():
    print('Bot has been stopped.')
    while True:
        sleep(3)