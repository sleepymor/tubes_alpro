import sys
from PyQt5.QtWidgets import QApplication
from Login import Login_Window
from user_window import UserWindow
from admin_window import AdminWindow
# from signup import SignUp_Window


def main():

    app = QApplication(sys.argv)
    
  
    admin_window = AdminWindow()
    user_window = UserWindow()
    # singup_window = SignUp_Window()


    def open_admin_window():
        admin_window.show()

    def open_user_window():
        user_window.show()

    def open_signup_window():
        user_window.show()

    login_window = Login_Window(open_admin_window, open_user_window, open_signup_window)
    login_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()  
#     sys.exit(app.exec_())

