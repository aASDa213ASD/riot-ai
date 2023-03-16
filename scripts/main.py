import data, utils
from os import system, path, getcwd
from bot import run

class Terminal:
    def __init__(self):
        data.picture_path = path.join(getcwd(), "images")
        data.shop_path = path.join(getcwd(), "images\\shop")
        self.commands = ['run', 'stop', 'settings', 'version', 'load', 'set']

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
        if (data.summoner_name is not None and data.games_to_play >= 1):
            run()
        else:
            print('Wrong setup.')
    
    def execute_stop(self):
        exit()
    
    def execute_settings(self):
        print(f'Games: {data.games_finished}/{data.games_to_play}')
        print(f'Account: {data.summoner_name}')
        print(f'Region: {data.summoner_region}')
        print(f'AccountLevelCap: {data.account_level_cap}')
        print(f'RandomChamps: {data.random_champions}')
        print(f'RandomRunesNSumms: {data.random_runes_summs}')
        print(f'RandomSumms: {data.random_summs}')
        print(f'HonorTeammates: {data.honor_teammates}')

    def execute_version(self):
        print('LEAGUE-AI Build 1.0 (03 Mar. 2023) // prxvatescrxpts')
    
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