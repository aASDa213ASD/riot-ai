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

def get_account_info():
    data.summoner_name = bot_settings['Name']
    data.summoner_region = bot_settings['Region']


def get_level_cap():
    data.account_level_cap = bot_settings.getint('AccountLevelCap')
    if (data.account_level_cap != 0):
        data.account_level_flag = True


def get_runes_n_summs():
    data.random_runes_summs = bot_settings.getint('RandomRunesNSumms')
    data.random_summs = bot_settings.getint('RandomSumms')
    if (data.random_runes_summs):
        data.random_summs = 0


def get_champion_setting():
    data.random_champions = bot_settings.getint('RandomChamps')

def get_honor_setting():
    data.honor_teammates = bot_settings.getint('HonorTeammates')

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
    get_account_info()
    get_account_level()
    get_level_cap()
    get_runes_n_summs()
    get_champion_setting()
    get_honor_setting()