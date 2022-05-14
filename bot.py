import vk_api
import logging
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from homework import hw_from_text, hw_list_to_str
from helpers import *


class Bot:

    def __init__(self, api_key, group_id, db):
        self.session = vk_api.VkApi(token=api_key)
        self.group_id = group_id
        self.api = self.session.get_api()
        self.longpoll = VkBotLongPoll(self.session, group_id)
        self.subjects = db.get_subjects()
        self.db = db

        keyboard = VkKeyboard(one_time=False)

        for i, subject in enumerate(self.subjects):
            keyboard.add_button(subject, color=VkKeyboardColor.POSITIVE)
            if i % 3 == 2:
                keyboard.add_line()

        keyboard.add_line()
        keyboard.add_button('На 1 день', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('На 7 дней', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('На 30 дней', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Все домашки', color=VkKeyboardColor.NEGATIVE)

        self.main_keyboard = keyboard.get_keyboard()

        logging.info('Bot initialized')

    # @:param msg - message containing deadline info
    def exec_get_by_deadline(self, msg, event):
        try:
            hw = self.db.get_by_deadline(int(msg))
            self.send_to_event_exciter(event, hw_list_to_str(hw) if hw else 'Нет актуальных дз')
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный дедлайн')

    # @:param msg - message text after "add" command
    def exec_add_hw(self, msg, event):
        try:
            hw = hw_from_text(msg)
            self.db.add_homework(hw)
            self.send_to_event_exciter(event, 'ДЗ успешно добавлено')
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный формат')

    def exec_add_subj(self, msg, _):
        subj = msg.strip()
        self.db.add_subject(subj)

    # @:param msg - message text with command
    def exec_if_command(self, msg, event):
        if msg.startswith('start'):
            self.send_to_event_exciter(event, 'Выберите действие')
        elif msg.startswith('add_hw'):
            self.exec_add_hw(text_after_prefix('add_hw', msg), event)
        elif msg.startswith('add_subj'):
            self.exec_add_subj(text_after_prefix('add_subj', msg), event)
        elif msg.startswith('на 1 день') or msg.startswith('на 7 дней') or msg.startswith('на 30 дней'):
            days = int(msg.split(' ')[1])
            homeworks = self.db.get_by_deadline(days)
            self.send_to_event_exciter(event, 'Нет актуальных дз' if not homeworks else hw_list_to_str(homeworks))
        elif msg.startswith('все домашки'):
            homeworks = self.db.get_all_homeworks()
            self.send_to_event_exciter(event, 'Нет актуальных дз' if not homeworks else hw_list_to_str(homeworks))
        elif msg in self.subjects:
            homeworks = self.db.get_by_subject(msg)
            self.send_to_event_exciter(event, 'Нет актуальных дз' if not homeworks else hw_list_to_str(homeworks))
        else:
            self.send_to_event_exciter(event, 'Неизвестная команда')


    def exec(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_obj = event.obj['message']
            text = msg_obj['text'].strip().lower()
            logging.info('\n===============================\n'
                         f"Message received: {text}\n"
                         f"from peer_id {msg_obj['peer_id']}\n"
                         '===============================\n')
            self.exec_if_command(text, event)

    def start(self):
        while True:
            try:
                logging.info('Start listening')
                for event in self.longpoll.listen():
                    self.exec(event)
            except Exception as e:
                logging.error(e)

    def send_to_event_exciter(self, event, message):
        self.api.messages.send(message=message,
                               peer_id=event.obj['message']['peer_id'],
                               random_id=0,
                               keyboard=self.main_keyboard)
