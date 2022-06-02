from typing import List

import logging
from pypika import MySQLQuery, CustomFunction, Table

from src.model.homework import Homework
from src.repository.database import execute_and_commit, execute_and_fetch

current_time = 'CURTIME()'
homeworks_t = Table('homeworks')
subjects_t = Table('subjects')
DateDiff = CustomFunction('DATEDIFF', ['deadline', 'current'])


class HomeworkRepository:

    def __init__(self):
        logging.info('Database initialized')

    """
    
    Adds homework to database
    
    """

    def add_homework(self, homework: Homework) -> None:
        query = MySQLQuery.into(homeworks_t).insert(
            homework.subject, homework.deadline, homework.text
        )
        execute_and_commit(query)

    """
    
    Removes non actual homeworks from database
    
    """

    def remove_with_expired_deadline(self) -> None:
        query = MySQLQuery.from_(homeworks_t).delete().where(
            DateDiff(homeworks_t.deadline, 'CURTIME()') < 0
        )
        execute_and_commit(query)

    """
    
    Adds subject to database
    
    """

    def add_subject(self, subject) -> None:
        query = MySQLQuery.into(subjects_t).insert(subject)
        execute_and_commit(query)

    """
    
    Returns all subjects
    
    """

    def get_subjects(self) -> List[str]:
        query = MySQLQuery.from_(subjects_t).select(subjects_t.star)
        subj = execute_and_fetch(query)
        return [x[0] for x in subj] or []

    """
    
    Return homeworks which deadline is before [deadline_in_days]
    
    
    """

    def get_by_deadline(self, deadline_in_days) -> List[Homework]:
        query = MySQLQuery.from_(homeworks_t).select(homeworks_t.star).where(
            DateDiff(homeworks_t.deadline, 'CURTIME()') < deadline_in_days
        )
        return self.process_get_homeworks_query(query)

    """
    
    Returns homeworks which subject is equal to given
    
    """

    def get_by_subject(self, subject) -> List[Homework]:
        query = MySQLQuery.from_(homeworks_t).select(homeworks_t.star).where(
            homeworks_t.subject == subject
        )
        return self.process_get_homeworks_query(query)

    """
    
    Removes expired homeworks and return actual
    
    """

    def get_all_homeworks(self) -> List[Homework]:
        self.remove_with_expired_deadline()
        query = MySQLQuery.from_(homeworks_t).select(homeworks_t.star)
        return self.process_get_homeworks_query(query)

    """
    
    Returns all homeworks from database
    
    """

    def get_all_homeworks_without_update(self) -> List[Homework]:
        query = MySQLQuery.from_(homeworks_t).select(homeworks_t.star)
        return self.process_get_homeworks_query(query)

    @staticmethod
    def process_get_homeworks_query(query) -> List[Homework]:
        query_result = execute_and_fetch(query)
        return [Homework(*h) for h in query_result] if query_result else []
