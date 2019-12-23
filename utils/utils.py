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
    def log(message: str):
        for line in message.split("\n"):
            print(f'[{datetime.now()}]', line)

    @staticmethod
    def warning(message: str):
        for line in message.split("\n"):
            print(f'{Colors.WARNING}[{datetime.now()}]', line)

    @staticmethod
    def error(message: str):
        for line in message.split("\n"):
            print(f'{Colors.FAIL}[{datetime.now()}]', line)


class CommandError(Exception):
    pass
