from dataclasses import dataclass
from collections import namedtuple

Homework = namedtuple('Homework', ['subject', 'deadline', 'text'])


def hw_from_text(text):
    try:
        subject, deadline, text = map(lambda s: s.strip(), text.split(';'))
        return Homework(subject, deadline, text)
    except Exception:
        return None


def hw_list_to_str(hw_list):
    return '\n\n'.join(map(hw_str, hw_list))


def hw_str(hw):
    return f"""
    Предмет: {hw['subject']}
    Дедлайн: {hw['deadline']}
    Описание: {hw['text']}
    """.strip()
