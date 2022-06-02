from pypika import Query, Column, MySQLQuery

from src.bot.bot import Bot
from src.config import *
from src.repository.homework_repository import HomeworkRepository
from src.repository.mysql_database import *

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    database = MySQLDatabase(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        name=DB_NAME
    )
    bot = Bot(
        api_key=API_KEY,
        group_id=GROUP_ID,
        repository=HomeworkRepository(database)
    )
    bot.start()
