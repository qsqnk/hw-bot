import logging

from mysql.connector import connect


class MySQLDatabase:

    def __init__(self, user, password, host, name):
        self.user = user
        self.password = password
        self.host = host
        self.name = name

    def with_connection(self, decorated):
        def wrapper(*args, **kwargs):
            try:
                connection = connect(
                    host=self.host,
                    database=self.name,
                    user=self.user,
                    password=self.password
                )
                return decorated(*args, **kwargs, connection=connection)
            except Exception as connection_error:
                logging.error(connection_error)

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
        except Exception as execution_error:
            logging.error(execution_error)

    def execute_and_fetch(self, query):
        return self.execute(query, commit=False, fetch=True)

    def execute_and_commit(self, query):
        return self.execute(query, query, commit=True, fetch=False)
