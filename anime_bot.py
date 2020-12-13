from instabot import Bot
from credentials  import get_password
from credentials import get_username


posting_bot = Bot()
posting_bot.login(username=get_username(), password=get_password())

def post(url, cap):
    posting_bot.upload_photo(url,cap)

