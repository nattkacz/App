import psycopg2
from psycopg2 import sql, connect
from psycopg2.errors import DuplicateDatabase, DuplicateTable, OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

def create_database():
    try:
        cnx =connect(dbname= "postgres", user = os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
        cnx.autocommit = True
        cursor = cnx.cursor()

        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv("DB_NAME"))))
            print(f"Database '{os.getenv('DB_NAME')}' created successfully.")
        except DuplicateDatabase:
            print(f"Database '{os.getenv('DB_NAME')}' already exists.")
        finally:
            cursor.close()
            cnx.close()
    except OperationalError:
        print("Error connecting to the database")

def create_tables():
    try:
        cnx = connect(dbname= os.getenv("DB_NAME"), user = os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))

        cursor = cnx.cursor()

        try:
            cursor.execute("""CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        hashed_password VARCHAR(80) NOT NULL)
                        """)
            print("Table 'users' created successfully")
        except DuplicateTable:
            print("Table 'users' already exist.")

        try:
            cursor.execute("""CREATE TABLE messages(
                        id SERIAL PRIMARY KEY,
                        from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        text VARCHAR(255) NOT NULL)
                        """)
            print("Table 'messages' created successfully")
        except DuplicateTable:
            print("Table 'messages' already exist.")

        cnx.commit()
    except OperationalError:
        print("Error connecting to the database")
    finally:
        cursor.close()
        cnx.close()





if __name__ == "__main__":
    create_database()
    create_tables()