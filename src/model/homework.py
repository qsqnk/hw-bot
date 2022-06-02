from datetime import datetime

from src.helpers import *


class Homework:

    def __init__(self, subject: str, deadline: datetime, text: str):
        self.subject = subject
        self.deadline = deadline
        self.text = text

    """
    
    Returns dict representation of homework
    
    """

    def as_dict(self):
        return {
            'subject': self.subject,
            'deadline': datetime_to_str(self.deadline),
            'text': self.text
        }

    """
    
    Transforms text representation to homework object
    
    Format: {subject} ; day/month/year hours:minutes ; description
    
    """

    @staticmethod
    def from_text(text: str):
        subject, deadline, text = map(lambda s: s.strip(), text.split(';'))
        if not datetime_check_format(deadline):
            raise Exception
        return Homework(subject, datetime_from_str(deadline), text)

    """

    Transforms dict representation to homework object

    Format: { 'subject' ..., 'deadline': ..., 'text':... }

    """

    @staticmethod
    def from_dict(dictionary: dict):
        return Homework(
            dictionary['subject'],
            datetime_from_str(dictionary['deadline']),
            dictionary['text']
        )

    """
    
    Transforms list of homeworks to pretty str representation
    
    """

    @staticmethod
    def list_to_str(hw_list):
        return '\n\n'.join(map(str, hw_list)) if hw_list else 'Нет актуальных дз'

    def __str__(self):
        return f"""
            Предмет: {self.subject}
            Дедлайн: {self.deadline}
            Описание: {self.text}
            """.strip()