from app.database import init_db
from app.text_loader import load_text_files

def main():
    # Initialize the database and load text files
    init_db()
    load_text_files()

if __name__ == "__main__":
    main()
