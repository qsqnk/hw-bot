import sys

sys.path.insert(0, '../src')

from src.hw_bot.helpers import datetime_check_format, text_after_prefix
from src.hw_bot.model.homework import Homework


def test_datetime_check_format():
    correct_date = '2019-12-31'
    incorrect_date = '2019/12/31'

    assert datetime_check_format(correct_date)
    assert not datetime_check_format(incorrect_date)


def test_text_after_prefix():
    text = 'hello exams'
    prefix = 'hello'

    assert text_after_prefix(prefix, text) == 'exams'


def test_homework_from_text():
    homework_text = 'диффур ; 2019-12-31 ; решить задачу из задачника'
    homework = Homework.from_text(homework_text)

    assert homework.subject == 'диффур'
    assert homework.deadline.day == 31
    assert homework.deadline.month == 12
    assert homework.deadline.year == 2019
    assert homework.text == 'решить задачу из задачника'


def test_homework_to_str():
    homework_text = 'диффур ; 2019-12-31 ; решить задачу из задачника'
    homework = Homework.from_text(homework_text)
    print(str(homework))
    assert str(homework) == f"""
            Предмет: диффур
            Дедлайн: 2019-12-31 00:00:00
            Описание: решить задачу из задачника
            """.strip()
