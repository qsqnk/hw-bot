from collections import namedtuple

from helpers import datetime_check_format

Homework = namedtuple('Homework', ['subject', 'deadline', 'text'])


def hw_from_text(text):
    subject, deadline, text = map(lambda s: s.strip(), text.split(';'))
    if not datetime_check_format(deadline):
        raise Exception
    return Homework(subject, deadline, text)


def hw_list_to_str(hw_list):
    return '\n\n'.join(map(hw_str, hw_list))


def hw_str(hw):
    return f"""
    Предмет: {hw['subject']}
    Дедлайн: {hw['deadline']}
    Описание: {hw['text']}
    """.strip()
