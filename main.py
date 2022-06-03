from src.hw_bot.bot.bot import Bot
from src.hw_bot.config import *
from src.hw_bot.repository.homework_repository import HomeworkRepository
from src.hw_bot.repository.mysql_database import *

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
