import vk_api
import logging
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from homework import hw_from_text, hw_list_to_str
from helpers import *


class Bot:

    def __init__(self, api_key, group_id, db):
        session = vk_api.VkApi(token=api_key)
        self.group_id = group_id
        self.api = session.get_api()
        self.longpoll = VkBotLongPoll(session, group_id)
        self.db = db
        logging.info('Bot initialized')

    # @:param msg - message containing deadline info
    def exec_get_by_deadline(self, msg, event):
        try:
            hw = self.db.get_by_deadline(int(msg))
            self.send_to_event_exciter(event, hw_list_to_str(hw) if hw else 'Нет актуальных дз')
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный дедлайн')

    # @:param msg - message containing subject info
    def exec_get_by_subject(self, msg, event):
        subjects = self.db.get_subjects()
        if msg not in subjects:
            self.send_to_event_exciter(event, 'Такого предмета нет')
            return
        hw = self.db.get_by_subject(msg)
        self.send_to_event_exciter(event, hw_list_to_str(hw) if hw else 'Нет актуальных дз')

    # @:param msg - message text after "get" command
    def exec_get(self, msg, event):
        if not msg:
            self.send_to_event_exciter(event, 'Некорректный формат ввода\n'
                                              'По предмету: get предмет\n'
                                              'По количеству дней до дедлайна: get deadline n\n'
                                              'Список доступных предметов доступен по сообщению help')
        elif msg.startswith('deadline'):
            self.exec_get_by_deadline(text_after_prefix('deadline', msg), event)
        else:
            self.exec_get_by_subject(msg, event)

    # @:param msg - message text after "add" command
    def exec_add_hw(self, msg, event):
        try:
            hw = hw_from_text(msg)
            self.db.add_homework(hw)
            self.send_to_event_exciter(event, 'ДЗ успешно добавлено')
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный формат')

    def exec_help(self, _, event):
        subjects = self.db.get_subjects()
        self.send_to_event_exciter(event, 'Получить домашки по кол-ву дней до дедлайна: get deadline days\n'
                                          'Пример: get deadline 3\n\n'
                                          'Получить домашки по названию предмета: get subject\n'
                                          'Пример: get веб\n\n'
                                          f"Список доступных предметов: {' '.join(subjects)}\n")

    def exec_add_subj(self, msg, _):
        subj = msg.strip()
        self.db.add_subject(subj)

    # @:param msg - message text with command
    def exec_if_command(self, msg, event):
        if msg.startswith('add_hw'):
            self.exec_add_hw(text_after_prefix('add_hw', msg), event)
        if msg.startswith('add_subj'):
            self.exec_add_subj(text_after_prefix('add_subj', msg), event)
        if msg.startswith('get'):
            self.exec_get(text_after_prefix('get', msg), event)
        if msg.startswith('help'):
            self.exec_help(msg, event)

    def exec(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_obj = event.obj['message']
            text = msg_obj['text'].strip()
            logging.info('\n===============================\n'
                         f"Message received: {text}\n"
                         f"from peer_id {msg_obj['peer_id']}\n"
                         '===============================\n')
            self.exec_if_command(text, event)

    def start(self):
        logging.info('Start listening')
        for event in self.longpoll.listen():
            self.exec(event)

    def send_to_event_exciter(self, event, message):
        self.api.messages.send(message=message, peer_id=event.obj['message']['peer_id'], random_id=0)
