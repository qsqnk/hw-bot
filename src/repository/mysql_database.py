import logging

from mysql.connector import connect

from src.config import *


class MySQLDatabase:

    def __init__(self, user, password, host, name):
        self.user = user
        self.password = password
        self.host = host
        self.name = name

    def with_connection(self, f):
        def wrapper(*args, **kwargs):
            try:
                connection = connect(
                    host=self.host,
                    database=self.name,
                    user=self.user,
                    password=self.password
                )
                return f(*args, **kwargs, connection=connection)
            except Exception as e:
                logging.error(e)

        return wrapper

    @with_connection
    def execute(self, query, commit, fetch, connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute(str(query))
                result = cursor.fetchall() if fetch else None
            if commit:
                connection.commit()
            connection.close()
            return result
        except Exception as e:
            logging.error(e)

    def execute_and_fetch(self, query):
        return self.execute(query, commit=False, fetch=True)

    def execute_and_commit(self, query):
        return self.execute(query, query, commit=True, fetch=False)
