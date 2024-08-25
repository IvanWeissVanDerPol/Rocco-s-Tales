import re

def detect_delimiters(text):
    """Detects potential delimiters for chapters, scenes, and parts within the text."""
    chapter_delimiter = "CAPÍTULO" if "CAPÍTULO" in text else None
    scene_delimiter = "ESCENA" if "ESCENA" in text else None
    
    part_delimiter = "\n\n"
    
    return chapter_delimiter, scene_delimiter, part_delimiter

def parse_text_into_chapters(full_text, chapter_delimiter):
    """Parses the text into chapters based on the detected chapter delimiter."""
    chapters = full_text.split(chapter_delimiter) if chapter_delimiter else [full_text]
    parsed_chapters = []
    for i, chapter in enumerate(chapters):
        chapter = chapter.strip()
        if chapter:
            parsed_chapters.append({
                'chapter_number': i + 1,
                'content': chapter
            })
    return parsed_chapters

def parse_chapter_into_scenes(chapter_content, scene_delimiter):
    """Parses a chapter into scenes based on the detected scene delimiter."""
    scenes = chapter_content.split(scene_delimiter) if scene_delimiter else [chapter_content]
    parsed_scenes = []
    for i, scene in enumerate(scenes):
        scene = scene.strip()
        if scene:
            parsed_scenes.append({
                'scene_number': i + 1,
                'content': scene
            })
    return parsed_scenes

def parse_chapters_into_scenes(chapters, scene_delimiter):
    """Parses chapters into scenes."""
    parsed_scenes = []
    for chapter in chapters:
        scenes = parse_chapter_into_scenes(chapter['content'], scene_delimiter)
        parsed_scenes.extend(scenes)
    return parsed_scenes

def parse_scene_into_parts(scene_content, part_delimiter):
    """Parses a scene into parts based on the detected part delimiter."""
    parts = []
    paragraphs = scene_content.split(part_delimiter)
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if paragraph:
            parts.append({
                'order_in_scene': i + 1,
                'content': paragraph,
                'part_type': 'narration'
            })
    return parts
