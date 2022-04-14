import firebase_admin
import logging
from firebase_admin import credentials, db

from helpers import datetime_from_str, difference_in_days, current_time
from homework import Homework


class DB:

    def __init__(self, credentials_path, url):
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {'databaseURL': url})
        self.root = db.reference()
        logging.info('Database initialized')

    def add_homework(self, homework: Homework):
        homeworks = self.get_all_homeworks()
        homeworks.append(homework._asdict())
        self.root.update({'hw': homeworks})

    def remove_with_expired_deadline(self):
        homeworks = self.get_all_homeworks_without_update()
        actual = [hw for hw in homeworks if current_time().time() <= datetime_from_str(hw['deadline']).time()]
        self.root.child('hw').set(actual)

    def add_subject(self, subject):
        subjects = self.get_subjects()
        subjects.append(subject)
        self.root.update({'subjects': subjects})

    def get_subjects(self):
        return self.root.child('subjects').get() or []

    def get_by_deadline(self, deadline):
        homework = self.get_all_homeworks()

        def check(hw):
            datetime = datetime_from_str(hw['deadline'])
            return difference_in_days(datetime, datetime.now()) <= deadline

        return [hw for hw in homework if check(hw)]

    def get_by_subject(self, subject):
        homeworks = self.get_all_homeworks()
        return [hw for hw in homeworks if hw['subject'] == subject]

    def get_all_homeworks(self):
        self.remove_with_expired_deadline()
        return self.get_all_homeworks_without_update()

    def get_all_homeworks_without_update(self):
        homeworks = self.root.child('hw').get()
        return homeworks or []
