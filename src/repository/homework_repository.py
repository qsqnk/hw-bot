from typing import List

import firebase_admin
import logging
from firebase_admin import credentials, db

from src.helpers import datetime_from_str, difference_in_days, utc_current_time, to_utc
from src.model.homework import Homework


class HomeworkRepository:

    def __init__(self, credentials_path, url):
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {'databaseURL': url})
        self.root = db.reference()
        logging.info('Database initialized')

    """
    
    Adds homework to database
    
    """

    def add_homework(self, homework: Homework) -> None:
        self.root.child('hw').set(self.get_all_homeworks() + homework.as_dict())

    """
    
    Removes non actual homeworks from database
    
    """

    def remove_with_expired_deadline(self) -> None:
        def check(homework):
            return utc_current_time() <= to_utc(homework.deadline)

        self.root.child('hw').set([
            *filter(check, self.get_all_homeworks_without_update())
        ])

    """
    
    Adds subject to database
    
    """

    def add_subject(self, subject) -> None:
        self.root.child('subjects').set(self.get_subjects() + subject)

    """
    
    Returns all subjects
    
    """

    def get_subjects(self) -> List[str]:
        return self.root.child('subjects').get() or []

    """
    
    Return homeworks which deadline is before [deadline_in_days]
    
    
    """

    def get_by_deadline(self, deadline_in_days) -> List[Homework]:
        def check(hw):
            datetime = datetime_from_str(hw.deadline)
            return difference_in_days(datetime, datetime.now()) <= deadline_in_days

        return [*filter(check, self.get_all_homeworks())]

    """
    
    Returns homeworks which subject is equal to given
    
    """

    def get_by_subject(self, subject) -> List[Homework]:
        return [*filter(lambda homework: homework.subject == subject, self.get_all_homeworks())]

    """
    
    Removes expired homeworks and return actual
    
    """

    def get_all_homeworks(self) -> List[Homework]:
        self.remove_with_expired_deadline()
        return self.get_all_homeworks_without_update()

    """
    
    Returns all homeworks from database
    
    """

    def get_all_homeworks_without_update(self) -> List[Homework]:
        homeworks = self.root.child('hw').get()
        return [*map(Homework.from_dict, homeworks)] if homeworks else []
