from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)


class LoginWindow(QMainWindow):
    def __init__(self, open_admin_window, open_user_window):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 350, 550)
        self.open_admin_window = open_admin_window
        self.open_user_window = open_user_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Login")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(self.label)

        # Username Field
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        layout.addWidget(self.username)

        # Password Field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Main Widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if username == "admin" and password == "admin123":
            QMessageBox.information(self, "Success", "Logged in as Admin")
            self.open_admin_window()
        elif username == "user" and password == "user123":
            QMessageBox.information(self, "Success", "Logged in as User")
            self.open_user_window()
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password")
