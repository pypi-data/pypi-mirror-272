import datetime
from abc import ABC, abstractmethod


class CommandHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def handle_command(self, command: str, args: list) -> str:
        pass


class DefaultCommandHandler(CommandHandler):

    def handle_command(self, command: str, args: list):
        return f'Command: {command}\nArgs: {args}'
