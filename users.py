import hashlib

class UserManager:
    def __init__(self):
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        # Для простоты, пользователи хранятся в словаре
        users = {
            'admin': {
                'password': hashlib.sha256('adminpass'.encode()).hexdigest(),
                'role': 'admin'
            },
            'analyst': {
                'password': hashlib.sha256('analystpass'.encode()).hexdigest(),
                'role': 'analyst'
            }
        }
        return users

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user['password']:
                self.current_user = {'username': username, 'role': user['role']}
                return True
        return False
