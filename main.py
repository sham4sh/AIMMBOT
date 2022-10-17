# Main file. Main page and all pop up windows are defined here.

import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QStatusBar, QToolBar, QLineEdit, QGridLayout, QWidget, QPushButton, QMessageBox)
from sqlalchemy import false
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
cred = credentials.Certificate("aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json")
firebase_admin.initialize_app(cred)

#Main window, loaded on application start. All widgets and popups stem from here.
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("AIMMBOT")
        self.setGeometry(100, 100, 1500, 800)
        self.logoText = QLabel("AIMMBOT", parent=self)
        self.logoText.move(10, 30)
        self.setCentralWidget(QLabel("CENTRAL WIDGET REQUIRED FOR RENDERING. REPLACE ME LATER"))
        self.createToolBar()

    

    def createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        tools.addAction("Login", self.logWindow)
        tools.addAction("Register", self.regWindow)
        tools.setMovable(False)
        self.addToolBar(tools)

    def logWindow(self):
        self.lf = LoginWindow()
        self.lf.show()
        self.hide()

    def regWindow(self):
        self.rf = RegisterWindow()
        self.rf.show()
        self.hide()

#Window that allows existing users to log in to their account
class LoginWindow(QWidget):

	def __init__(self):

		super().__init__()
		self.setWindowTitle('Login Form')
		self.resize(500, 120)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		layout.addWidget(label_password, 1, 0)
		layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Register')
		button_login.clicked.connect(self.check_password)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(2, 75)

		self.setLayout(layout)

	def check_password(self):

		msg = QMessageBox()

		if self.lineEdit_username.text() == 'Username' and self.lineEdit_password.text() == '000':
			msg.setText('Success')
			msg.exec_()
			msg.hide()
			self.hide()
			window.show()
		else:
			msg.setText('Incorrect Password')
			msg.exec_()

#Window that allows new users to register via Firebase
class RegisterWindow(QWidget):

	def __init__(self):

		super().__init__()
		self.setWindowTitle('Registration Form')
		self.resize(500, 120)

		layout = QGridLayout()

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Please enter your username (must be a valid email address)')
		layout.addWidget(label_name, 0, 0)
		layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Please enter your password')
		layout.addWidget(label_password, 1, 0)
		layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.clicked.connect(self.register_user)
		layout.addWidget(button_login, 2, 0, 1, 2)
		layout.setRowMinimumHeight(2, 75)

		self.setLayout(layout)

	def register_user(self):

		msg = QMessageBox()

		try:
			user = auth.create_user(email=self.lineEdit_username.text(), password=self.lineEdit_password.text())
			msg.setText("Account Created Succesfully")
			msg.exec_()
			msg.hide()
			self.hide()
			window.show()
		except:
			msg.setText("Username Already Exists")
			msg.exec()

    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())