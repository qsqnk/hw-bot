import logging

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from src.helpers import text_after_prefix
from src.model.homework import Homework
from src.repository.homework_repository import HomeworkRepository


class Bot:

    def __init__(self, api_key, group_id, repository: HomeworkRepository):

        self._group_id = group_id
        self._session = vk_api.VkApi(token=api_key)
        self._api = self._session.get_api()
        self._longpoll = VkBotLongPoll(self._session, group_id)
        self._repository = repository
        self._main_keyboard = self._generate_keyboard(self._repository.get_subjects(), width=3)

        logging.info('Bot initialized')

    # Starts long polling
    def start(self):
        while True:
            try:
                logging.info('Start long polling')
                for event in self._longpoll.listen():
                    self._exec_if_message(event)
            except ConnectionError as connection_error:
                logging.error(connection_error)

    # Sends [message] to user who excited [event] by peer_id
    def _send_to_event_exciter(self, event, message):
        self._api.messages.send(
            message=message,
            peer_id=event.obj['message']['peer_id'],
            random_id=0,
            keyboard=self._main_keyboard
        )

    # Utility method for generating user keyboard
    # [width] means how many subjects will be in one row
    @staticmethod
    def _generate_keyboard(subjects, width):
        keyboard = VkKeyboard(one_time=False)
        for i, subject in enumerate(subjects):
            keyboard.add_button(subject, color=VkKeyboardColor.POSITIVE)
            if i % width == width - 1:
                keyboard.add_line()
        keyboard.add_line()
        for text in ['На 1 день', 'На 7 дней', 'На 30 дней']:
            keyboard.add_button(text, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Все домашки', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    # Processing a request for getting homework with given deadline
    # [msg] contains info about deadline in days
    def _exec_get_by_deadline(self, msg, event):
        try:
            hw_list = self._repository.get_by_deadline(int(msg))
            self._send_to_event_exciter(event, Homework.list_to_str(hw_list))
        except Exception as error:
            logging.error(error)
            self._send_to_event_exciter(event, 'Некорректный дедлайн')

    # Processing a request for adding new homework
    # [msg] contains text representation of homework
    def _exec_add_hw(self, msg, event):
        try:
            self._repository.add_homework(Homework.from_text(msg))
            self._send_to_event_exciter(event, 'ДЗ успешно добавлено')
        except Exception as error:
            logging.error(error)
            self._send_to_event_exciter(event, 'Некорректный формат')

    # Processing a request for adding new subject
    # [msg] contains info about subject
    def _exec_add_subj(self, msg, event):
        self._repository.add_subject(msg.strip())
        self._send_to_event_exciter(event, 'Предмет успешно добавлен')

    # Processing a request for command execution
    # [msg] user message
    def _exec_if_command(self, msg, event):
        if msg.startswith('start'):

            self._send_to_event_exciter(event, 'Выберите действие')

        elif msg.startswith('add_hw'):

            homework_text_repr = text_after_prefix('add_hw', msg)
            self._exec_add_hw(homework_text_repr, event)

        elif msg.startswith('add_subj'):

            subject = text_after_prefix('add_subj', msg)
            self._exec_add_subj(subject, event)

        elif any(map(msg.startswith, ['На 1 день', 'На 7 дней', 'На 30 дней'])):
            deadline_in_days = int(msg.split(' ')[1])
            actual_homeworks = Homework.list_to_str(
                self._repository.get_by_deadline(deadline_in_days)
            )
            self._send_to_event_exciter(event, actual_homeworks)

        elif msg.startswith('все домашки'):

            all_homeworks = Homework.list_to_str(self._repository.get_all_homeworks())
            self._send_to_event_exciter(event, all_homeworks)

        elif msg in self._repository.get_subjects():

            subject_homeworks = Homework.list_to_str(self._repository.get_by_subject(msg))
            self._send_to_event_exciter(event, subject_homeworks)

        else:
            self._send_to_event_exciter(event, 'Неизвестная команда')

    # Processing an even if it is new message to bot
    def _exec_if_message(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_obj = event.obj['message']
            text = msg_obj['text'].strip().lower()
            peer_id = msg_obj['peer_id']

            logging.info('\n===============================\n'
                         'Message received: %s\n'
                         'from peer_id %d\n'
                         '===============================\n', text, peer_id)

            self._exec_if_command(text, event)
