import datetime
from abc import ABC, abstractmethod

from doot.response import HandlerResponse


class MessageHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def handle_message(self, message_text: str) -> HandlerResponse:
        pass


class DefaultMessageHandler(MessageHandler):

    def handle_message(self, message_text: str) -> HandlerResponse:
        return HandlerResponse(message=f'Echo: {message_text}')
