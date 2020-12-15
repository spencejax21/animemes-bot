from instabot import Bot
import os


posting_bot = Bot()
posting_bot.login(username=os.environ('ACCOUNT_USERNAME'), password=os.environ('ACCOUNT_PASSWORD'))

def post(url, cap):
    posting_bot.upload_photo(url,cap)

