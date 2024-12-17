class User:
    def __init__(self, db, name, role):
        self.db = db
        self.name = name
        self.role = role

    def create_user(self):
        query = "INSERT INTO users (name, role, login_time) VALUES (%s, %s, NOW()) RETURNING id"
        return self.db.execute(query, (self.name, self.role))

    def update_login_time(self):
        query = "UPDATE users SET login_time = NOW() WHERE name = %s AND role = %s"
        self.db.execute(query, (self.name, self.role))

    @staticmethod
    def fetch_users(db):
        query = "SELECT name, role, login_time FROM users"
        return db.execute(query)
