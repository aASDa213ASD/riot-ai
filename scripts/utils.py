import data, requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from re import search
from os import path, getcwd
from time import time

settings = ConfigParser()
settings.read(path.join(getcwd(), "settings.ini"))
bot_settings = settings['Settings']


def read_settings():
    data.game_mode = bot_settings['game_mode']
    data.game_map = bot_settings['game_map']
    data.game_queue = bot_settings['game_queue']
    data.account_level_cap = bot_settings.getint('account_level_cap')
    data.random_champs = bot_settings.getboolean('random_champs')
    data.random_runes = bot_settings.getboolean('random_runes')
    if data.random_runes:
        data.random_summs = False
    else:
        data.random_summs = bot_settings.getboolean('random_summs')
    data.honor_teammates = bot_settings.getboolean('honor_teammates')


def get_account_level():
    url = f'https://www.leagueofgraphs.com/summoner/{data.summoner_region.lower()}/{data.summoner_name}'
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.104'
    }

    response = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(response.content, 'html.parser')
    find_level = soup.find('div', class_ = 'bannerSubtitle').get_text()
    level = int(search(r'\d+', find_level).group())
    
    data.account_level_last_check = time()
    data.account_level = level


def perform_setup():
    settings.read(path.join(getcwd(), "settings.ini"))
    read_settings()