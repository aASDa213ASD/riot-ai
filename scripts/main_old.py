import data, utils, ctypes
from bot import run
from os import system

"""
PROCESSES ()
LeagueClient.exe
League of Legends.exe
LeagueClientUx.exe
LeagueClientUxRender.exe

WINDOWS()
'League of Legends (TM) Client'
'League of Legends'
'GPU Error'
"""

def main():
    system('cls')
    while True:
        try:
            data.games_to_play = int(input('Games to play: '))
            if data.games_to_play < 1:
                raise ValueError
            break
        except ValueError:
            print('The number must not be less than 1.')
    start()

def start():
    utils.setup()

    ctypes.windll.kernel32.SetConsoleTitleW(
        f'Level {data.account_level}, Game {data.games_finished}/{data.games_to_play}'
        )

    run()


if __name__ == '__main__':
    main()