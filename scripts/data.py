# Bot setup vars
games_to_play = -1  # default to -1 to tell the robot and listener threads to wait
games_finished = 0

# Account-related vars
account_level = 0
account_level_last_check = 0
level_check_flag = 0

# Path vars
lol_client_path = None
picture_path = None
shop_path = None
champion_typelist = None
files_to_replace = ['game.cfg', 'input.ini']

# Thread variables
listener_thread = None # ?
listener_thread_id = None # ?
bot_thread = None # ?

# Client variables
honor_coordinates = [273, 597, 909, 1230]
random_champion = [386, 486, 588, 692, 790, 893]

# Numerical variables
go_flag = 1
stop_flag = 0
time_since_last_click = 0
ingame = 0
prepared_to_fight = False

# String variables
last_status = None
available_champions = []

# File variables
lol_client_path = None
picture_path = None
shop_path = None
champion_typelist = None
files_to_replace = ['game.cfg', 'input.ini']

# Game variables
dead = None
current_champion = None

# Shop variables
build_firstItem = None
build_potionsAmount = 0
build_bootsItem = None
build_mythicItem = None