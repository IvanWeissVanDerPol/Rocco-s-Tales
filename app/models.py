from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Subreddits Table
class Subreddit(Base):
    __tablename__ = 'subreddits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)  # Name of the subreddit
    description = Column(Text)  # Description or sidebar content of the subreddit
    created_at = Column(DateTime, default=datetime.utcnow)
    subscribers = Column(Integer)  # Number of subscribers
    nsfw = Column(Boolean, default=False)  # Whether the subreddit is marked as NSFW
    icon_url = Column(String(255))  # URL of the subreddit’s icon or logo

    posts = relationship("RedditPost", back_populates="subreddit")


# Reddit Posts Table
class RedditPost(Base):
    __tablename__ = 'reddit_posts'
    id = Column(String(10), primary_key=True)  # Reddit post ID
    title = Column(String(300), nullable=False)
    content = Column(Text)
    author = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    post_url = Column(String(255))
    num_comments = Column(Integer)
    upvotes = Column(Integer)
    downvotes = Column(Integer)
    upvote_ratio = Column(Float)
    nsfw = Column(Boolean, default=False)
    spoiler = Column(Boolean, default=False)
    awards = Column(JSON)
    post_flair = Column(String(100))
    tts_audio_id = Column(Integer, ForeignKey('tts_audio.id'))  # Link to TTS audio
    image_id = Column(Integer, ForeignKey('generated_images.id'))  # Link to generated image
    subreddit_id = Column(Integer, ForeignKey('subreddits.id'))  # Foreign key to subreddits table

    comments = relationship("RedditComment", back_populates="post")
    subreddit = relationship("Subreddit", back_populates="posts")


# Reddit Comments Table
class RedditComment(Base):
    __tablename__ = 'reddit_comments'
    id = Column(String(10), primary_key=True)  # Reddit comment ID
    post_id = Column(String(10), ForeignKey('reddit_posts.id', ondelete='CASCADE'))
    content = Column(Text)
    author = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    comment_url = Column(String(255))
    upvotes = Column(Integer)
    downvotes = Column(Integer)
    is_op = Column(Boolean, default=False)  # Whether the comment is by the original poster
    edited = Column(Boolean, default=False)
    parent_id = Column(String(10))  # ID of the parent comment
    depth = Column(Integer)
    awards = Column(JSON)
    rating_id = Column(Integer, ForeignKey('content_ratings.id'))  # Link to rating
    tts_audio_id = Column(Integer, ForeignKey('tts_audio.id'))  # Link to TTS audio
    image_id = Column(Integer, ForeignKey('generated_images.id'))  # Link to generated image

    post = relationship("RedditPost", back_populates="comments")


# Content Ratings Table
class ContentRating(Base):
    __tablename__ = 'content_ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content_type = Column(String(50))  # 'post' or 'comment'
    content_id = Column(String(10))  # ID of the post or comment being rated
    rating = Column(Float, nullable=False)
    rating_type = Column(String(50))  # e.g., sentiment, quality, relevance
    rating_source = Column(String(100))  # e.g., user, algorithm
    rating_comment = Column(Text)  # Comments or notes associated with the rating
    rating_weight = Column(Float)  # Weight of the rating
    rated_at = Column(DateTime, default=datetime.utcnow)


# TTS Audio Table
class TTSAudio(Base):
    __tablename__ = 'tts_audio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)  # Path to the TTS audio file
    voice_used = Column(String(100))  # The voice model used for TTS
    generated_text = Column(Text, nullable=False)  # Text that was converted to TTS
    created_at = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)  # Duration of the TTS audio in seconds
    language = Column(String(50))
    accent = Column(String(50))
    gender = Column(String(50))  # Gender of the voice used for TTS
    voice_pitch = Column(Float)
    generation_method = Column(String(100))  # e.g., GPT-4, Google TTS
    usage_count = Column(Integer, default=0)
    post_id = Column(String(10), ForeignKey('reddit_posts.id', ondelete='CASCADE'))
    comment_id = Column(String(10), ForeignKey('reddit_comments.id', ondelete='CASCADE'))


# Generated Images Table
class GeneratedImage(Base):
    __tablename__ = 'generated_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)  # Path to the generated image
    description = Column(Text)  # Description or tags associated with the image
    created_at = Column(DateTime, default=datetime.utcnow)
    image_resolution = Column(String(50))  # e.g., 1024x768
    image_format = Column(String(10))  # e.g., JPEG, PNG
    color_palette = Column(String(50))  # e.g., monochrome, vibrant
    generation_method = Column(String(100))  # e.g., DALL-E, Stable Diffusion
    tags = Column(JSON)  # JSON field for tags associated with the image
    usage_count = Column(Integer, default=0)
    post_id = Column(String(10), ForeignKey('reddit_posts.id', ondelete='CASCADE'))
    comment_id = Column(String(10), ForeignKey('reddit_comments.id', ondelete='CASCADE'))


# Tags Table
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)  # Description or definition of the tag
    category = Column(String(50))  # Category of the tag (e.g., genre, sentiment)
    related_tags = Column(JSON)  # JSON field for related tags


# Content Tags Table
class ContentTag(Base):
    __tablename__ = 'content_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'))
    content_type = Column(String(50))  # 'post' or 'comment'
    content_id = Column(String(10))  # ID of the post or comment
    confidence_score = Column(Float)  # Confidence score if tags are assigned automatically
