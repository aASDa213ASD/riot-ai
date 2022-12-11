import data, requests
from configparser import ConfigParser
from bs4 import BeautifulSoup
from re import search
from os import path, getcwd
from time import time

# Vars declaration
settings = ConfigParser()
settings.read(path.join(getcwd(), "settings.ini"))
bot_settings = settings['Settings']


def get_check_lvl_flag():
    data.level_check_flag = bot_settings.getint('CheckAccountLevel')


def get_account_level():
    summoner_name = bot_settings['Name']
    account_region = bot_settings['Region']

    url = f'https://www.leagueofgraphs.com/summoner/{account_region.lower()}/{summoner_name}'
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.104'
    }

    response = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(response.content, 'html.parser')
    find_level = soup.find('div', class_ = 'bannerSubtitle').get_text()
    level = int(search(r'\d+', find_level).group())
    
    data.account_level_last_check = time()
    data.account_level = level


def setup():
    data.picture_path = path.join(getcwd(), "images")
    data.shop_path = path.join(getcwd(), "images\\shop")
    get_check_lvl_flag()
    get_account_level()