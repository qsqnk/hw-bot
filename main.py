from src.bot.bot import Bot
from src.config import *
from src.repository.homework_repository import *

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    db = HomeworkRepository(credentials_path=DB_CREDENTIALS, url=DB_URL)
    bot = Bot(api_key=API_KEY, group_id=GROUP_ID, repository=db)
    bot.start()
