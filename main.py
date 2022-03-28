from bot import Bot
from config import *
from db import *

if __name__ == '__main__':
    db = DB(credentials_path=DB_CREDENTIALS, url=DB_URL)
    bot = Bot(api_key=API_KEY, group_id=GROUP_ID, db=db)
    bot.start()
