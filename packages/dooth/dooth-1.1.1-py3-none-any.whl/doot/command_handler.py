from abc import ABC, abstractmethod

from doot.response import HandlerResponse


class CommandHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def handle_command(self, command: str, args: list) -> HandlerResponse:
        pass


class DefaultCommandHandler(CommandHandler):

    def handle_command(self, command: str, args: list) -> HandlerResponse:
        return HandlerResponse(message=f'Command: {command}\nArgs: {args}')
