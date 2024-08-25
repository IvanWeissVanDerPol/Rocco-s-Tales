import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def fetch_post(subreddit_name, post_id):
    subreddit = reddit.subreddit(subreddit_name)
    post = subreddit.submission(id=post_id)
    return post
