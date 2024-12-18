import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname="parking_db",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Database connection successful.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if self.cursor.description:  # If the query returns data
                return self.cursor.fetchall()
            else:  # If it's an INSERT/UPDATE/DELETE
                self.connection.commit()  # Commit the transaction
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()  # Rollback in case of error

    def commit(self):
        self.connection.commit()  # Commit the current transaction

    def close(self):
        self.cursor.close()
        self.connection.close()