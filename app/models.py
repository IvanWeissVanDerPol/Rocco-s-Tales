from sqlalchemy import Column, Integer, String, Text, JSON, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    author = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class CharacterVoice(Base):
    __tablename__ = 'character_voices'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id', ondelete='CASCADE'), nullable=False)
    voice_sample_path = Column(String(255), nullable=False)
    emotion_profile = Column(JSON)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    character = relationship("Character")

class Scene(Base):
    __tablename__ = 'scenes'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    scene_number = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    book = relationship("Book")

class ScenePart(Base):
    __tablename__ = 'scene_parts'
    id = Column(Integer, primary_key=True)
    scene_id = Column(Integer, ForeignKey('scenes.id', ondelete='CASCADE'), nullable=False)
    part_type = Column(String(50), nullable=False)  # Narration, Dialogue, SoundEffect
    content = Column(Text)
    character_id = Column(Integer, ForeignKey('characters.id'))
    sound_effect_path = Column(String(255))
    background_music_id = Column(Integer)
    order_in_scene = Column(Integer, nullable=False)
    timestamp = Column(Float)
    image_id = Column(Integer)
    voice_id = Column(Integer, ForeignKey('character_voices.id'))
    emotion_detected = Column(String(50))
    music_transition_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    scene = relationship("Scene")
    character = relationship("Character")
    voice = relationship("CharacterVoice")

class AudioFile(Base):
    __tablename__ = 'audio_files'
    id = Column(Integer, primary_key=True)
    scene_id = Column(Integer, ForeignKey('scenes.id', ondelete='CASCADE'), nullable=False)
    audio_type = Column(String(50), nullable=False)  # Narration, Dialogue, SoundEffect
    character_id = Column(Integer, ForeignKey('characters.id'))
    voice_id = Column(Integer, ForeignKey('character_voices.id'))
    file_path = Column(String(255), nullable=False)
    audio_position = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    scene = relationship("Scene")
    character = relationship("Character")
    voice = relationship("CharacterVoice")
