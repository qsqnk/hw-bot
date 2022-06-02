import logging

from mysql.connector import connect

from src.config import *


def with_connection(f):
    def wrapper(*args, **kwargs):
        try:
            connection = connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return f(*args, **kwargs, connection=connection)
        except Exception as e:
            logging.error(e)

    return wrapper


@with_connection
def execute(query, commit, fetch, connection):
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


def execute_and_fetch(query):
    return execute(query, commit=False, fetch=True)


def execute_and_commit(query):
    return execute(query, commit=True, fetch=False)
