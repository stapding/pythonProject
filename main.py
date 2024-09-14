import sys
from PyQt5.QtWidgets import QApplication
from ui import LoginWindow
from users import UserManager
import traceback
from email_sender import send_error_email

def main():
    try:
        app = QApplication(sys.argv)
        user_manager = UserManager()
        login_window = LoginWindow(user_manager)
        login_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"Произошла ошибка: {error_message}")
        send_error_email(error_message)

if __name__ == "__main__":
    main()
