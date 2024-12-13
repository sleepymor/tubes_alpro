from PyQt5 import QtCore, QtGui, QtWidgets
from database import cursor, mc, bc


class Login_Window(QtWidgets.QMainWindow):
    def __init__(self, open_admin_window, open_user_window, open_signup_window):
        super().__init__()
        self.setObjectName("Login_Window")
        self.resize(350, 500)
        self.setStyleSheet("background: rgb(255, 213, 5);")
        self.open_admin_window = open_admin_window
        self.open_user_window = open_user_window
        self.open_signup_window = open_signup_window
        self.setupUi()

    def setupUi(self):

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 351, 501))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet('font: 81 18pt "Plus Jakarta Sans ExtraBold";')
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setStyleSheet('font: 80 10pt "Plus Jakarta Sans Semibold";')
        self.label_3.setObjectName("label_3")

        self.verticalLayout_3.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setStyleSheet("background: rgb(255, 255, 255)")
        self.lineEdit.setObjectName("lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setStyleSheet('font: 80 10pt "Plus Jakarta Sans Semibold";')
        self.label_2.setObjectName("label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setStyleSheet("background: rgb(255, 255, 255)")
        self.lineEdit_2.setObjectName("lineEdit_2")


        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem4)


        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.clicked.connect(self.signup)
        self.pushButton_2.setStyleSheet(
            "background: rgb(255, 255, 255);\n"
            "border-radius: 10px;\n"
            "padding: 8px;\n"
            "width: 50px;\n"
            'font: 63 8pt "Plus Jakarta Sans SemiBold";\n'
            "hover: { \n"
            "    background: rgb(212, 212, 212);\n"
            "    scale: 115%;\n"
            "}"
        )
        self.pushButton_2.setObjectName("pushButton_2")


        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.login)
        self.pushButton.setEnabled(True)
        self.pushButton.setStyleSheet(
            "background: rgb(255, 255, 255);\n"
            'font: 63 8pt "Plus Jakarta Sans SemiBold";\n'
            "border-radius: 10px;\n"
            "padding: 8px;\n"
            "width: 50px;\n"
            "hover: { \n"
            "    background: rgb(212, 212, 212);\n"
            "    scale: 115%;\n"
            "}"
        )
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem8)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Login_Window):
        _translate = QtCore.QCoreApplication.translate
        Login_Window.setWindowTitle(_translate("Login_Window", "Login_Window"))
        self.label.setText(_translate("Login_Window", "LOGIN"))
        self.label_3.setText(_translate("Login_Window", "Login"))
        self.label_2.setText(_translate("Login_Window", "Password"))
        self.pushButton_2.setText(_translate("Login_Window", "SignUp"))
        self.pushButton.setText(_translate("Login_Window", "Login"))

    def login(self):
        usernames = self.lineEdit.text()
        raw_password = self.lineEdit_2.text()
        try:
            cursor.execute(
                "SELECT passwords as passwords, status as status FROM user WHERE usernames = %s",
                (usernames,),
            )
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                if bc.checkpw(
                    raw_password.encode("utf-8"), stored_password.encode("utf-8")
                ):
                    if result[1] == "admin":
                        self.open_admin_window()
                    else:
                        self.open_user_window()
                else:
                    print("Invalid password.")
            else:
                print("Username not found.")
        except mc.Error as e:
            print(f"Error: {e}")

    def signup(self):
        self.open_signup_window()


# if __name__ == "__main__":
#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     Login_Window = QtWidgets.QLogin_window()
#     ui = Login_Window()
#     ui.setupUi(Login_Window)
#     Login_Window.show()  # Add this line to show the window
#     sys.exit(app.exec_())
