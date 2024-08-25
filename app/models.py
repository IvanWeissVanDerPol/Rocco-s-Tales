from sqlalchemy import Column, Integer, String, Text, JSON, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class RedditPost(Base):
    __tablename__ = 'reddit_posts'
    id = Column(String(10), primary_key=True)  # Reddit post ID
    title = Column(String(300))
    content = Column(Text)
    author = Column(String(255))
    rating = Column(Float)
    summary = Column(Text)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    comments = relationship("RedditComment", back_populates="post")

class RedditComment(Base):
    __tablename__ = 'reddit_comments'
    id = Column(String(10), primary_key=True)  # Reddit comment ID
    post_id = Column(String(10), ForeignKey('reddit_posts.id', ondelete='CASCADE'))
    content = Column(Text)
    author = Column(String(255))
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    post = relationship("RedditPost", back_populates="comments")
