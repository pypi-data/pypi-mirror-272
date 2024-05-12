import datetime
from abc import ABC, abstractmethod


class MessageHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def handle_message(self, message_text: str) -> str:
        pass


class DefaultMessageHandler(MessageHandler):

    def handle_message(self, message_text: str) -> str:
        return f'Echo: {message_text}'
