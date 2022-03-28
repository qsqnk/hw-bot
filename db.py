import firebase_admin
from firebase_admin import credentials, db

from homework import Homework


class DB:

    def __init__(self, credentials_path, url):
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {'databaseURL': url})
        self.root = db.reference()

    def add_homework(self, homework: Homework):
        homeworks = self.root.child('hw').get()
        if not homeworks:
            homeworks = []
        homeworks.append(homework._asdict())
        self.root.update({'hw': homeworks})

    def get_by_subject(self, subject):
        homeworks = self.get_all_homeworks()
        return [hw for hw in homeworks if hw['subject'] == subject]

    def get_all_homeworks(self):
        homeworks = self.root.child('hw').get()
        return homeworks or []
