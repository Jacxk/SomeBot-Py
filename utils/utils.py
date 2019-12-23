from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    @staticmethod
    def log(message):
        print(f'[{datetime.now()}]', message)

    @staticmethod
    def warning(message):
        print(f'{Colors.WARNING}[{datetime.now()}] WARNING!', message)

    @staticmethod
    def error(message):
        print(f'{Colors.FAIL}[{datetime.now()}] ERROR!', message)


class CommandError(Exception):
    pass
