import sys
from PyQt5.QtWidgets import QApplication
from Login import Login_Window
from user_window import UserWindow
from admin_window import AdminWindow
from database import db
from signup import SignUpWindow


def main():

    app = QApplication(sys.argv)
    

    
    def open_login_window():
        login_window.show()

    admin_window = AdminWindow(db)
    user_window = UserWindow()
    singup_window = SignUpWindow(open_login_window)

    def open_admin_window():
        admin_window.show()

    def open_user_window():
        user_window.show()

    def open_signup_window():
        singup_window.show()

    login_window = Login_Window(open_admin_window, open_user_window, open_signup_window)
    login_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


