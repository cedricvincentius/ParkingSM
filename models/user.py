import bcrypt  # Make sure to install bcrypt library
from db.database_manager import DatabaseManager

class User:
    VALID_ROLES = ['admin', 'user']  # Define valid roles

    def __init__(self, db_manager, name, role, password=None):
        if role not in User.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Valid roles are: {User .VALID_ROLES}")
        self.db_manager = db_manager
        self.name = name
        self.role = role
        self.password = password  # This should be the plain text password when creating a user

    def verify_password(self, password):
        # Verify the password against the stored hashed password
        if isinstance(self.password, str):
            stored_password_bytes = self.password.encode('utf-8')
        else:
            stored_password_bytes = self.password

        return bcrypt.checkpw(password.encode('utf-8'), stored_password_bytes)

    @staticmethod
    def fetch_users(db_manager):
        query = "SELECT name, role, login_time FROM users"
        return db_manager.execute(query)

    @staticmethod
    def is_valid_role(role):
        return role in User.VALID_ROLES

    @staticmethod
    def login_user(name, role, password):
        db_manager = DatabaseManager()
        query = "SELECT password FROM users WHERE name = %s AND role = %s"
        result = db_manager.execute(query, (name, role))

        if result:
            stored_hashed_password = result[0]['password']
            user = User(db_manager, name, role, stored_hashed_password)

            if user.verify_password(password):
                print(f"Login successful! Welcome, {name}!")
                return True  # Indicate successful login
            else:
                print("Invalid password. Please try again.")
        else:
            print("User  not found. Please register first.")
        return False  # Indicate failed login