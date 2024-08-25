from reddit.reddit import fetch_post
from app.inserter import process_and_store_post, handle_low_rating_post, select_content_for_video
from app.database import get_db

def main():
    db_session = next(get_db())
    subreddit_name = "AskReddit"  # Change to your desired subreddit
    post_id = "your_post_id_here"  # Change to the specific post ID you want to process

    post = fetch_post(subreddit_name, post_id)
    process_and_store_post(post, db_session)

    if post.rating < 2.0:
        handle_low_rating_post(post.id, db_session)
    else:
        select_content_for_video(post.id, db_session)

if __name__ == "__main__":
    main()
