from typing import List
from pypika import MySQLQuery, CustomFunction, Table
from src.hw_bot.model.homework import Homework

HOMEWORKS = Table('homeworks')
SUBJECTS = Table('subjects')
DATE_DIFF = CustomFunction('DATEDIFF', ['deadline', 'current'])


class HomeworkRepository:

    def __init__(self, database):
        self.database = database

    # Adds homework to database
    def add_homework(self, homework: Homework) -> None:
        query = MySQLQuery.into(HOMEWORKS).insert(
            homework.subject, homework.deadline, homework.text
        )
        self.database.execute_and_commit(query)

    # Removes non actual homeworks from database
    def remove_with_expired_deadline(self) -> None:
        query = MySQLQuery.from_(HOMEWORKS).delete().where(
            DATE_DIFF(HOMEWORKS.deadline, 'CURTIME()') < 0
        )
        self.database.execute_and_commit(query)

    # Adds subject to database
    def add_subject(self, subject) -> None:
        query = MySQLQuery.into(SUBJECTS).insert(subject)
        self.database.execute_and_commit(query)

    # Returns all subjects
    def get_subjects(self) -> List[str]:
        query = MySQLQuery.from_(SUBJECTS).select(SUBJECTS.star)
        subj = self.database.execute_and_fetch(query)
        return [s for (s,) in subj] or []

    # Return homeworks which deadline is before [deadline_in_days]
    def get_by_deadline(self, deadline_in_days) -> List[Homework]:
        query = MySQLQuery.from_(HOMEWORKS).select(HOMEWORKS.star).where(
            DATE_DIFF(HOMEWORKS.deadline, 'CURTIME()') < deadline_in_days
        )
        return self.process_get_homeworks_query(query)

    # Returns homeworks which subject is equal to given
    def get_by_subject(self, subject) -> List[Homework]:
        query = MySQLQuery.from_(HOMEWORKS).select(HOMEWORKS.star).where(
            HOMEWORKS.subject == subject
        )
        return self.process_get_homeworks_query(query)

    # Removes homeworks with expired deadline and returns actual
    def get_all_homeworks(self) -> List[Homework]:
        self.remove_with_expired_deadline()
        query = MySQLQuery.from_(HOMEWORKS).select(HOMEWORKS.star)
        return self.process_get_homeworks_query(query)

    # Returns all homeworks from database
    def get_all_homeworks_without_update(self) -> List[Homework]:
        query = MySQLQuery.from_(HOMEWORKS).select(HOMEWORKS.star)
        return self.process_get_homeworks_query(query)

    def process_get_homeworks_query(self, query) -> List[Homework]:
        query_result = self.database.execute_and_fetch(query)
        return [Homework(*h) for h in query_result] if query_result else []
