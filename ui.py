from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QTimer
from data_collector import DataCollector
from email_sender import send_error_email
from encryption import EncryptionManager
import threading

class LoginWindow(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация")

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.user_manager.authenticate(username, password):
            self.main_window = MainWindow(self.user_manager.current_user)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.data_collector = DataCollector()
        self.encryption_manager = EncryptionManager()
        self.init_ui()
        self.start_data_collection()

    def init_ui(self):
        self.setWindowTitle(f"Главное окно - {self.user['role'].capitalize()}")

        self.data_table = QTableWidget()
        self.setCentralWidget(self.data_table)

        self.refresh_button = QPushButton("Обновить данные")
        self.refresh_button.clicked.connect(self.load_data)

        layout = QVBoxLayout()
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.data_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_data_collection(self):
        self.collection_thread = threading.Thread(target=self.collect_data)
        self.collection_thread.daemon = True
        self.collection_thread.start()

    def collect_data(self):
        try:
            while True:
                data = self.data_collector.fetch_data()
                encrypted_data = self.encryption_manager.encrypt_data(data)
                with open("data.enc", "wb") as f:
                    f.write(encrypted_data)
        except Exception as e:
            send_error_email(str(e))

    def load_data(self):
        try:
            with open("data.enc", "rb") as f:
                encrypted_data = f.read()
            data = self.encryption_manager.decrypt_data(encrypted_data)
            # Разграничение доступа
            if self.user['role'] == 'analyst':
                data = data[:int(len(data)*0.2)]  # 20% данных
            self.display_data(data)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные")
            send_error_email(str(e))

    def display_data(self, data):
        self.data_table.clear()
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.data_table.setItem(i, j, QTableWidgetItem(str(value)))
