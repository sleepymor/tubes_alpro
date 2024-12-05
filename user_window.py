from PyQt5.QtWidgets import QMainWindow, QLabel


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 350, 550)
        self.initUI()

    def initUI(self):
        label = QLabel("Welcome, User!", self)
        label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        label.setGeometry(100, 200, 200, 50)
