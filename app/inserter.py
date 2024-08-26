from sqlalchemy.orm import sessionmaker
from models import RedditPost, RedditComment
from database import get_db
from ai_utils import rate_content, generate_tts_for_post, generate_image_for_post

def process_and_store_post(post, db_session):
    reddit_post = RedditPost(
        id=post.id,
        title=post.title,
        content=post.selftext,
        author=post.author.name,
        rating=rate_content(post.title + " " + post.selftext)
    )
    db_session.add(reddit_post)
    db_session.commit()

    for comment in post.comments:
        if isinstance(comment, praw.models.Comment):  # Check if it is a comment and not MoreComments
            reddit_comment = RedditComment(
                id=comment.id,
                post_id=post.id,
                content=comment.body,
                author=comment.author.name,
                rating=rate_content(comment.body)
            )
            db_session.add(reddit_comment)
    db_session.commit()

def handle_low_rating_post(post_id, db_session):
    post = db_session.query(RedditPost).get(post_id)
    if post.rating < 2.0:  # Example threshold for low rating
        post.summary = f"Summary: {post.title[:100]}..."  # Keep a brief summary
        db_session.commit()
        # Now, delete the post details but keep the summary
        db_session.query(RedditComment).filter_by(post_id=post_id).delete()
        post.content = None
        db_session.commit()

def select_content_for_video(post_id, db_session):
    post = db_session.query(RedditPost).get(post_id)
    if post.rating >= 4.0:  # Example threshold for good rating
        generate_tts_for_post(post)
        generate_image_for_post(post)
        post.processed = True
        db_session.commit()
