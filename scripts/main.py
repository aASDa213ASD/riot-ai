import data, utils
from os import system, path, getcwd
from bot import run
from time import time

class Terminal:
    def __init__(self):
        data.picture_path = path.join(getcwd(), "dataset")
        data.shop_path = path.join(getcwd(), "dataset\\shop")
        self.commands = ['run', 'settings', 'version', 'load', 'set']

    def execute(self, command, args = None):
        cmd_to_execute = 'execute_' + str(command).lower()
        method = getattr(self, cmd_to_execute, lambda :'Invalid')
        if (args):
            return method(args)
        return method()

    def execute_help(self):
        print(f'Commands:', *self.commands)

    def execute_clear(self):
        system('cls')

    def execute_run(self):
        if (data.games_to_play >= 1):
            data.time_idle = time()
            run()
        else:
            print('Wrong setup.')
    
    def execute_settings(self):
        print(f'games: {data.games_finished}/{data.games_to_play}')
        print(f'account_level_cap: {data.account_level_cap}')
        print(f'random_champs: {data.random_champs}')
        print(f'random_runes: {data.random_runes}')
        print(f'random_summs: {data.random_summs}')
        print(f'honor_teammates: {data.honor_teammates}')

    def execute_version(self):
        print('LEAGUE-AI Build 1.3 (1 Apr. 2023) // prxvatescrxpts')
    
    def execute_load(self):
        utils.perform_setup()
    
    def execute_set_games(self, games: int):
        data.games_to_play = int(games)


def main():
    terminal = Terminal()
    terminal.execute('clear')
    while True:
        prompt = input('league-ai@BOT:~$ ')
        if (prompt in terminal.commands):
            terminal.execute(prompt)
        elif (prompt == 'help' or prompt == 'clear'):
            terminal.execute(prompt)
        elif (prompt.split(" ")[0] == 'set'):
            command = prompt.split(" ")
            terminal.execute(command[0] + '_' + command[1], args=command[2])
        else:
            print('Command not found')


if __name__ == '__main__':
    main()
