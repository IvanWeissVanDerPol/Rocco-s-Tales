import os
from app.database import SessionLocal, init_db
from app.models import Book, Character
from app.ai_utils import detect_emotion

def load_text_files():
    session = SessionLocal()

    # Initialize the database (run once)
    init_db()

    texts_dir = "texts"
    for filename in os.listdir(texts_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(texts_dir, filename)
            with open(filepath, 'r') as file:
                content = file.read()

            # Example: Process the file content with AI
            title = os.path.splitext(filename)[0]
            emotion = detect_emotion(content)

            # Create a new Book record
            new_book = Book(title=title, content=content, author="Unknown")
            session.add(new_book)
            session.commit()

            print(f"Loaded book '{title}' with detected emotion: {emotion}")

    session.close()

if __name__ == "__main__":
    load_text_files()
