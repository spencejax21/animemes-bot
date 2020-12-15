from instabot import Bot
import os


posting_bot = Bot()
posting_bot.login(username='reddit_animemes', password='seoul@2023')

def post(url, cap):
    posting_bot.upload_photo(url,cap)

