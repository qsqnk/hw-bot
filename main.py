from pypika import Query, Column, MySQLQuery

from src.bot.bot import Bot
from src.config import *
from src.repository.database import *
from src.repository.homework_repository import *

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    db = HomeworkRepository()
    bot = Bot(api_key=API_KEY, group_id=GROUP_ID, repository=db)
    bot.start()
