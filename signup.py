from PyQt5 import QtWidgets, QtCore
from database import cursor, mc, bc, db  


class SignUpWindow(QtWidgets.QMainWindow):
    def __init__(self, open_login_window):
        super().__init__()
        self.setObjectName("SignUp_Window")
        self.resize(350, 500)
        self.setStyleSheet("background: rgb(255, 213, 5);")
        self.open_login_window = open_login_window
        self.setupUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 351, 501))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Title
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet('font: 81 18pt "Plus Jakarta Sans ExtraBold";')
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        # Username Input
        self.label_username = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_username.setStyleSheet('font: 80 10pt "Plus Jakarta Sans Semibold";')
        self.label_username.setText("Username")
        self.verticalLayout.addWidget(self.label_username)

        self.lineEdit_username = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_username.setStyleSheet("background: rgb(255, 255, 255);")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.verticalLayout.addWidget(self.lineEdit_username)

        # Password Input
        self.label_password = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_password.setStyleSheet('font: 80 10pt "Plus Jakarta Sans Semibold";')
        self.label_password.setText("Password")
        self.verticalLayout.addWidget(self.label_password)

        self.lineEdit_password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_password.setStyleSheet("background: rgb(255, 255, 255);")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.verticalLayout.addWidget(self.lineEdit_password)

        # Confirm Password Input
        self.label_confirm_password = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_confirm_password.setStyleSheet('font: 80 10pt "Plus Jakarta Sans Semibold";')
        self.label_confirm_password.setText("Confirm Password")
        self.verticalLayout.addWidget(self.label_confirm_password)

        self.lineEdit_confirm_password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_confirm_password.setStyleSheet("background: rgb(255, 255, 255);")
        self.lineEdit_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirm_password.setObjectName("lineEdit_confirm_password")
        self.verticalLayout.addWidget(self.lineEdit_confirm_password)

        # Sign-Up Button
        self.pushButton_signup = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_signup.setText("Sign Up")
        self.pushButton_signup.setStyleSheet(
            "background: rgb(255, 255, 255);"
            "border-radius: 10px;"
            'font: 63 8pt "Plus Jakarta Sans SemiBold";'
        )
        self.pushButton_signup.clicked.connect(self.signup)
        self.verticalLayout.addWidget(self.pushButton_signup)

        # Back to Login Button
        self.pushButton_back = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_back.setText("Back to Login")
        self.pushButton_back.setStyleSheet(
            "background: rgb(255, 255, 255);"
            "border-radius: 10px;"
            'font: 63 8pt "Plus Jakarta Sans SemiBold";'
        )
        self.pushButton_back.clicked.connect(self.login)
        self.verticalLayout.addWidget(self.pushButton_back)

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def login(self):
       self.open_login_window()

    def retranslateUi(self, SignUp_Window):
        _translate = QtCore.QCoreApplication.translate
        SignUp_Window.setWindowTitle(_translate("SignUp_Window", "Sign Up"))
        self.label.setText(_translate("SignUp_Window", "SIGN UP"))

    def signup(self):
        # Get inputs
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()

        # Validate inputs
        if not username or not password or not confirm_password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        # Hash password and insert into database
        try:
            hashed_password = bc.hashpw(password.encode('utf-8'), bc.gensalt())
            cursor.execute(
                "INSERT INTO user (usernames, passwords, status) VALUES (%s, %s, %s)",
                (username, hashed_password.decode('utf-8'), 'user'),
            )
            db.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Account created successfully!")
            self.open_login_window()  # Go back to login
        except mc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            db.close()
