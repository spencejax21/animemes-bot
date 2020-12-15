import praw
import os
from anime_bot import post
import urllib
from datetime import datetime
import psycopg2
import requests

DATABASE_URL = os.environ['DATABASE_URL']

#connects with subreddit using praw credentials
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('Animemes')

#returns list containing ids of posts that have already been posted
def get_already_posted():
    

    already_posted = []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT post_id FROM posts")
        row = cur.fetchone()

        while row is not None:
            already_posted.append(row[0])
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return already_posted

#returns a list of the 10 hottest posts from the subreddit
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
    
#returns a filtered version of the hot posts list
#excludes posts that have already been posted, aren't images, or are NSFW
def post_filter(hot_posts):

    fresh_posts = []
    already_posted = get_already_posted()
    for post in hot_posts:
        if(post[0] not in already_posted and not post[4] and not post[5]):
            fresh_posts.append(post)
            write_posted(post[0])
    
    return fresh_posts


#writes the newly posted posts' ids to the database
def write_posted(post):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("INSERT INTO posts (post_id) VALUES (%s)", (post,) )

    conn.commit()
    cur.close()
    conn.close()
 
#gets the url of the post
def get_post_url(post):
    
    print(post[2])

#uploads each post on the list to Instagram
def upload(post_list):

    if(post_list):
        
        for x in post_list: 
            if(os.path.isfile(str(x[0]) + ".jpg")):
                print("Posting " + x[1] + "...")
                try:
                    post(str(x[0]) + ".jpg", x[1] + "\nOP: u/" + x[3] + "\n#animemes #anime #memes #funny #funnymemes")
                except RuntimeError:
                    print("Unsupported file format; could not complete process")
        else:
            print("Process complete.")
    
    #Note: this function is only necessary if running locally; with Heroku's ephemeral drive it is unecessary
    #for file in os.listdir('./'): 
        #if (file.endswith('.jpg') or file.endswith('jpg.REMOVE_ME')):
            #os.remove(file)
            
#downloads the images to the hard drive (using Heroku, the hard drive is ephemeral and these are lost once the session ends)
def download_images(post_list):

    if(post_list):
        for x in post_list:
            print(x[2])
            try:
                urllib.request.urlretrieve(x[2], x[0] + ".jpg")
            except RuntimeError:
                print("Unsupported file format")


#executes the program and posts the images
def get_feed():    
    
    post_list = post_filter(get_hot_posts(subreddit))
    if(post_list):

        download_images(post_list)
        upload(post_list)
        
get_feed()

