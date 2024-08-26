import os
import sys
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)

def recreate_database():
    # Drop all tables
    Base.metadata.drop_all(engine)
    print("All tables dropped successfully.")

    # Recreate all tables
    Base.metadata.create_all(engine)
    print("All tables created successfully.")

def setup_database():
    # Create all tables
    Base.metadata.create_all(engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'r':
        recreate_database()
    else:
        setup_database()
