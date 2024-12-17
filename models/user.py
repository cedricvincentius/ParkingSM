class User:
    def __init__(self, db, name, role):
        self.db = db
        self.name = name
        self.role = role

    def create_user(self):
        query = "INSERT INTO users (name, role) VALUES (%s, %s) RETURNING id"
        return self.db.execute(query, (self.name, self.role))

    @staticmethod
    def fetch_users(db):
        query = "SELECT * FROM users"
        return db.execute(query)
