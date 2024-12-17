import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="parking_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall() if self.cursor.description else None

    def close(self):
        self.cursor.close()
        self.connection.close()
