import asyncio
import datetime
import json
import logging
import threading
import time

import requests
from urllib.parse import quote

from doot.command_handler import CommandHandler, DefaultCommandHandler
from doot.exception import CommandProcessingError, MessageProcessingError
from doot.message import Mapper, Update
from doot.message_handler import MessageHandler, DefaultMessageHandler


class Bot:

    def __init__(self, token: str):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__base_url = f'https://api.telegram.org/bot{token}'
        self.__send_msg_url = f'{self.__base_url}/sendMessage'
        self.__get_updates_url = f'{self.__base_url}/getUpdates'
        self.__next_update_id = -1

        self.command_handler: CommandHandler = DefaultCommandHandler()
        self.message_handler: MessageHandler = DefaultMessageHandler()

    def send_notification(self, message: str, chat_id: int,
                          disable_web_page_preview: bool = False,
                          parse_mode: str = 'HTML'):

        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': str(disable_web_page_preview)
        }
        try:
            response = requests.post(self.__send_msg_url, params=params, timeout=5)
            response.raise_for_status()  # Raise an error if response status code is not 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")
            else:
                logging.info("Message sent successfully.")

    def _fetch_updates(self):
        params = {
            'offset': self.__next_update_id
        }
        try:
            response = requests.post(self.__get_updates_url, params=params, timeout=5)
            response.raise_for_status()  # Raise an error if response status code is not 200
            resp_dict = json.loads(response.content)
            updates = Mapper().map(resp_dict['result'])
            if len(updates) > 0:
                self.__next_update_id = updates[len(updates) - 1].update_id + 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending message: {e}")
            raise e
        else:
            if response.status_code != 200:
                logging.error(f"Error: {response.text}")
            else:
                logging.info("Message sent successfully.")
        return updates

    def _process_command(self, update: Update):
        args = []
        for e in update.message.text.split(' '):
            if e != '':
                args.append(e)
        command = args.pop(0)

        try:
            reply = self.command_handler.handle_command(command, args)
            self.send_notification(reply, update.message.chat.id)
        except Exception as e:
            raise CommandProcessingError(e)

    def _process_message(self, update: Update):
        try:
            reply = self.message_handler.handle_message(update.message.text)
            self.send_notification(reply, update.message.chat.id)
        except Exception as e:
            raise MessageProcessingError(e)

    def __drive(self, poll_delay: float):
        while True:
            try:

                updates = self._fetch_updates()
                for u in updates:
                    try:
                        if u.message.text is not None and u.message.text.startswith('/'):
                            self._process_command(u)
                        else:
                            self._process_message(u)
                    except MessageProcessingError as e:
                        self.__logger.error(f'Exception in processing update: {e}:\n{u}',
                                            stack_info=True, exc_info=True)
                        # just so we can move on
                        self.send_notification('Error in processing', u.message.chat.id)
                    time.sleep(poll_delay)

            except (ConnectionError, TimeoutError) as e:
                self.__logger.error(f'Error ==> {e}', stack_info=True, exc_info=True)
                time.sleep(15)  # To let systems recover
            except Exception as e:
                self.__logger.error(f'Error ==> {e}', stack_info=True, exc_info=True)

    def start(self, poll_delay: float = 5):
        my_thread = threading.Thread(target=self.__drive, args=[poll_delay])
        my_thread.start()
