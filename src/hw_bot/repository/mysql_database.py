import logging

from mysql.connector import connect


class MySQLDatabase:

    def __init__(self, user, password, host, name):
        self._user = user
        self._password = password
        self._host = host
        self._name = name

    # Wrapper for processing methods with an established connection
    # [decorated] - function which takes a connection as a parameter
    def with_connection(self, decorated):
        def wrapper(*args, **kwargs):
            try:
                connection = connect(
                    host=self._host,
                    database=self._name,
                    user=self._user,
                    password=self._password
                )
                return decorated(*args, **kwargs, connection=connection)
            except Exception as connection_error:
                logging.error(connection_error)
                return None

        return wrapper

    # Executes query with established connection and closes a connection
    # if [fetch] is true then returns cursor fetchall (read query)
    # if [commit] is true then connection commits changes (write query)
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
            return None

    # Executes [query] and returns cursor fetch
    def execute_and_fetch(self, query):
        return self.execute(query, commit=False, fetch=True)

    # Executes [query] and commits changes
    def execute_and_commit(self, query):
        return self.execute(query, query, commit=True, fetch=False)
