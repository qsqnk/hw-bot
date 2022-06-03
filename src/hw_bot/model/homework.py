from datetime import datetime

from src.hw_bot.helpers import datetime_check_format, datetime_from_str


class Homework:

    def __init__(self, subject: str, deadline: datetime, text: str):
        self.subject = subject
        self.deadline = deadline
        self.text = text

    # Transforms text representation to homework object
    # Format: subject ; year-month-day ; description
    @staticmethod
    def from_text(text: str):
        subject, deadline, text = map(lambda s: s.strip(), text.split(';'))
        if not datetime_check_format(deadline):
            raise Exception
        return Homework(subject, datetime_from_str(deadline), text)

    # Transforms list of homeworks to pretty str representation
    @staticmethod
    def list_to_str(hw_list):
        return '\n\n'.join(map(str, hw_list)) if hw_list else 'Нет актуальных дз'

    def __str__(self):
        return f"""
            Предмет: {self.subject}
            Дедлайн: {self.deadline}
            Описание: {self.text}
            """.strip()
