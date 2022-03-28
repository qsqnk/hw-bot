import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from homework import Homework, hw_from_text, hw_str, hw_list_to_str
from helpers import *


class Bot:

    def __init__(self, api_key, group_id, db):
        session = vk_api.VkApi(token=api_key)
        self.api = session.get_api()
        self.longpoll = VkBotLongPoll(session, group_id)
        self.db = db

    def process(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = text_after_prefix('[club211762649|Homework Bot] ', event.message.text.strip())
            print(text)
            if text.startswith('add'):
                hw = hw_from_text(text_after_prefix('add', text))
                if hw:
                    self.db.add_homework(hw)
                    self.send(event.chat_id, 'Success')
                else:
                    self.send(event.chat_id, 'Invalid format')
            if text.startswith('get'):
                subject = text_after_prefix('get', text)
                hw = self.db.get_by_subject(subject)
                self.send(event.chat_id, hw_list_to_str(hw) if hw else "Нет актуальных дз")

    def start(self):
        for event in self.longpoll.listen():
            self.process(event)

    def send(self, chat_id, message):
        self.api.messages.send(message=message, chat_id=chat_id, random_id=0)
