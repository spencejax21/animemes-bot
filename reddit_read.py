import praw
import os
from anime_bot import post
import urllib
from datetime import datetime
import psycopg2
import requests

DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(database = 'postgres', user='postgres', password='Airforce@2020', host='localhost')


reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('animemes')

def get_already_posted():
    
    #already_posted = []
    #if os.path.isfile("already_posted.txt"):
        #with open("already_posted.txt","r") as f:
            #already_posted = (f.read()).split("\n")
            #already_posted = list(filter(None, already_posted))
    #return already_posted
    already_posted = []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT post_id FROM posts")
        row = cur.fetchone()

        while row is not None:
            already_posted.append(row)
            print(already_posted)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return already_posted

def get_hot_posts(subreddit):

    hot_posts = []
    for submission in subreddit.hot(limit=10):
        post_data = []
        post_data.append(submission.id)
        post_data.append(submission.title)
        post_data.append(submission.url)
        post_data.append(submission.author.name)
        post_data.append(submission.is_self)
        post_data.append(submission.over_18)
        hot_posts.append(post_data)
    
    return hot_posts
    
def post_filter(hot_posts):

    fresh_posts = []
    already_posted = get_already_posted()
    for post in hot_posts:
        if(post[0] not in already_posted and not post[4] and not post[5]):
            fresh_posts.append(post)
            write_posted(post[0])
    
    return fresh_posts


def write_posted(post):

    #if os.path.isfile("already_posted.txt"):
        #with open("already_posted.txt","a") as f:
            #f.write("\n" + post)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("INSERT INTO posts (post_id) VALUES (%s) RETURNING post_number", (post,) )
    post_number = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
 
def get_post_url(post):
    
    print(post[2])


def upload(post_list):

    if(post_list):
        
        for x in post_list: 
            if(os.path.isfile(str(x[6]) + ".jpg")):
                print("Posting " + x[1] + "...")
                try:
                    post(str(x[6]) + ".jpg", x[1] + "\nOP: u/" + x[3] + "\n#animemes #anime #memes #funny #funnymemes")
                except RuntimeError:
                    print("Unsupported file format; could not complete process")
        else:
            print("Process complete.")
    
    #for file in os.listdir('./'): 
        #if (file.endswith('.jpg') or file.endswith('jpg.REMOVE_ME')):
            #os.remove(file)
            
def download_images(post_list):

    if(post_list):
        for x in post_list:
            print(x[2])
            number = get_post_number()
            try:
                urllib.request.urlretrieve(x[2], str(number) + ".jpg")
            except RuntimeError:
                print("Unsupported file format")

            x.append(number)

def get_post_number():

    number = 0
    if os.path.isfile("post_number.txt"):
        with open("post_number.txt","r") as f:
            number = int(f.read())
        with open("post_number.txt","w") as f:
            f.write(str(number+1))
    return number

def get_feed():    
    
    post_list = post_filter(get_hot_posts(subreddit))
    if(post_list):

        download_images(post_list)
        upload(post_list)
        
get_feed()