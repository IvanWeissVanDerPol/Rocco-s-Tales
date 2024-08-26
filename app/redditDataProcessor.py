import json
from sqlalchemy.orm import sessionmaker
from database import engine
from models import RedditPost, RedditComment, Subreddit, ContentRating

# Load JSON data
with open('app/reddit_data.json', 'r') as file:
    data = json.load(file)

# Create a new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

def process_and_store_post(post_data, db_session):
    # Check if the post already exists
    existing_post = db_session.query(RedditPost).filter_by(id=post_data['id']).first()
    if existing_post:
        print(f"Post with id {post_data['id']} already exists in the database.")
        return  # Skip insertion for this post

    # Handle Subreddit
    subreddit_name = post_data.get('subreddit')
    subreddit = db_session.query(Subreddit).filter_by(name=subreddit_name).first()
    if not subreddit:
        subreddit = Subreddit(
            name=subreddit_name,
            description="Example subreddit description",  # Fetch real description if needed
            subscribers=1000,  # Placeholder for subscribers count
            nsfw=post_data.get('nsfw', False)
        )
        db_session.add(subreddit)
        db_session.commit()

    # Insert the new post
    reddit_post = RedditPost(
        id=post_data['id'],
        title=post_data['title'],
        content=post_data['selftext'],
        author=post_data['author'],
        created_at=post_data['created_at'],
        post_url=post_data['post_url'],
        num_comments=post_data['num_comments'],
        upvotes=post_data['upvotes'],
        downvotes=post_data['downvotes'],
        upvote_ratio=post_data['upvote_ratio'],
        nsfw=post_data['nsfw'],
        spoiler=post_data['spoiler'],
        awards=post_data['awards'],
        post_flair=post_data['post_flair'],
        subreddit_id=subreddit.id
    )
    db_session.add(reddit_post)
    db_session.commit()

    # Insert comments for the post
    for comment_data in post_data['comments']:
        reddit_comment = RedditComment(
            id=comment_data['id'],
            post_id=post_data['id'],
            content=comment_data['content'],
            author=comment_data['author'],
            created_at=comment_data['created_at'],
            comment_url=comment_data['comment_url'],
            upvotes=comment_data['upvotes'],
            downvotes=comment_data['downvotes'],
            awards=comment_data['awards']
        )
        db_session.add(reddit_comment)
    db_session.commit()

# Process each post in the JSON data
for post_data in data['posts']:
    process_and_store_post(post_data, db_session)

# Close the session
db_session.close()

print("Data processed and stored successfully.")
