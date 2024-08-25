import os
import sys
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, RedditPost, RedditComment
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def setup_database(recreate=False):
    connection = None
    try:
        connection = psycopg2.connect(
            user="postgres",
            password=POSTGRES_PASSWORD,
            host=HOST,
            port=PORT,
            database="postgres"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        if recreate:
            cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME};")
            print(f"Database {DATABASE_NAME} dropped successfully.")

        cursor.execute(f"CREATE DATABASE {DATABASE_NAME};")
        print(f"Database {DATABASE_NAME} created successfully.")

    except Exception as error:
        print("Error setting up the database:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def setup_sqlalchemy():
    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        print("All tables created successfully.")
    except Exception as e:
        print("Error setting up SQLAlchemy:", e)

if __name__ == "__main__":
    recreate = len(sys.argv) > 1 and sys.argv[1].lower() == 'r'
    setup_database(recreate=recreate)
    setup_sqlalchemy()
