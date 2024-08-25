import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

connection_string = f"dbname='{DATABASE_NAME}' user='{USER}' host='{HOST}' password='{PASSWORD}' port='{PORT}'"

try:
    connection = psycopg2.connect(connection_string)
    print("Connection to the database was successful!")
    connection.close()
except Exception as e:
    print("Failed to connect to the database.")
    print("Error:", e)
