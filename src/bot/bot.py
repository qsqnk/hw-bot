import vk_api
import logging
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from src.helpers import *
from src.model.homework import Homework
from src.repository.homework_repository import HomeworkRepository


class Bot:

    def __init__(self, api_key, group_id, repository: HomeworkRepository):
        self.group_id = group_id
        self.session = vk_api.VkApi(token=api_key)
        self.api = self.session.get_api()
        self.longpoll = VkBotLongPoll(self.session, group_id)
        self.repository = repository
        self.main_keyboard = self.generate_keyboard(self.repository.get_subjects())

        logging.info('Bot initialized')

    @staticmethod
    def generate_keyboard(subjects):
        keyboard = VkKeyboard(one_time=False)
        for i, subject in enumerate(subjects):
            keyboard.add_button(subject, color=VkKeyboardColor.POSITIVE)
            if i % 3 == 2:
                keyboard.add_line()
        keyboard.add_line()
        for text in ['На 1 день', 'На 7 дней', 'На 30 дней']:
            keyboard.add_button(text, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Все домашки', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    """

    Processing a request for getting homework with given deadline

    [msg] contains info about deadline in days

    """

    def exec_get_by_deadline(self, msg, event):
        try:
            hw_list = self.repository.get_by_deadline(int(msg))
            self.send_to_event_exciter(event, Homework.list_to_str(hw_list))
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный дедлайн')

    """

    Processing a request for adding new homework

    [msg] contains text representation of homework

    """

    def exec_add_hw(self, msg, event):
        try:
            self.repository.add_homework(Homework.from_text(msg))
            self.send_to_event_exciter(event, 'ДЗ успешно добавлено')
        except Exception as e:
            logging.error(e)
            self.send_to_event_exciter(event, 'Некорректный формат')

    """
        
    Processing a request for adding new subject
    
    [msg] contains info about subject
    
    """

    def exec_add_subj(self, msg, event):
        self.repository.add_subject(msg.strip())
        self.send_to_event_exciter(event, 'Предмет успешно добавлен')

    """

    Processing a request for command execution

    [msg] user message

    """

    def exec_if_command(self, msg, event):
        if msg.startswith('start'):
            self.send_to_event_exciter(event, 'Выберите действие')
        elif msg.startswith('add_hw'):
            self.exec_add_hw(text_after_prefix('add_hw', msg), event)
        elif msg.startswith('add_subj'):
            self.exec_add_subj(text_after_prefix('add_subj', msg), event)
        elif msg.startswith('на 1 день') or msg.startswith('на 7 дней') or msg.startswith('на 30 дней'):
            days = int(msg.split(' ')[1])
            self.send_to_event_exciter(event, Homework.list_to_str(self.repository.get_by_deadline(days)))
        elif msg.startswith('все домашки'):
            self.send_to_event_exciter(event, Homework.list_to_str(self.repository.get_all_homeworks()))
        elif msg in self.repository.get_subjects():
            self.send_to_event_exciter(event, Homework.list_to_str(self.repository.get_by_subject(msg)))
        else:
            self.send_to_event_exciter(event, 'Неизвестная команда')

    def exec_if_message(self, event):
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

                logging.info('Start listening')
                for event in self.longpoll.listen():
                    self.exec_if_message(event)

    def send_to_event_exciter(self, event, message):
        self.api.messages.send(message=message,
                               peer_id=event.obj['message']['peer_id'],
                               random_id=0,
                               keyboard=self.main_keyboard)