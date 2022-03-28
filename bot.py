import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from homework import hw_from_text, hw_list_to_str
from helpers import *


class Bot:
    # must be obtained using group_id
    BOT_APPEAL = '[club211762649|Homework Bot]'

    def __init__(self, api_key, group_id, db):
        session = vk_api.VkApi(token=api_key)
        self.api = session.get_api()
        self.longpoll = VkBotLongPoll(session, group_id)
        self.db = db

    def process_add(self, hw_text, event):
        hw = hw_from_text(hw_text)
        if hw:
            self.db.add_homework(hw)
            self.send(event.chat_id, 'Success')
        else:
            self.send(event.chat_id, 'Invalid format')

    def process_get(self, subject, event):
        hw = self.db.get_by_subject(subject)
        self.send(event.chat_id, hw_list_to_str(hw) if hw else "Нет актуальных дз")

    def process_if_command(self, text, event):
        if text.startswith('add'):
            self.process_add(hw_text=text_after_prefix('add', text), event=event)
        if text.startswith('get'):
            self.process_get(subject=text_after_prefix('get', text), event=event)

    def process_if_to_me(self, text, event):
        if text.startswith(self.BOT_APPEAL):
            trimmed = text_after_prefix(self.BOT_APPEAL, text)
            self.process_if_command(text=trimmed, event=event)

    def process(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.message.text.strip()
            self.process_if_to_me(text, event)

    def start(self):
        for event in self.longpoll.listen():
            self.process(event)

    def send(self, chat_id, message):
        self.api.messages.send(message=message, chat_id=chat_id, random_id=0)
