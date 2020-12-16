from instabot import Bot
import os
import credentials


posting_bot = Bot()
posting_bot.login(username=credentials.username, password=credentials.password)

def post(url, cap):
    posting_bot.upload_photo(url,cap)

