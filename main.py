# Main file. Main page and all pop up windows are defined here.

from asyncio.windows_events import NULL
from sqlite3 import Cursor
import sys
import requests
import json
import signin
import pprint
from customWidgets import movieWidget
from PyQt5.QtWidgets import (QApplication, QScrollArea, QLabel, QVBoxLayout, QMainWindow, QStatusBar, QToolBar, QLineEdit, QGridLayout, QWidget, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
import firebase_admin
import algorithm
from UserDataFirebase import FirestoreDataAccess
from firebase_admin import credentials
from firebase_admin import auth
cred = credentials.Certificate("aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json")
mainApp = firebase_admin.initialize_app(cred)

#Main window, loaded on application start. All widgets and popups stem from here.
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("AIMMBOT")
        self.setGeometry(100, 100, 1500, 800)
        self.logoText = QLabel("AIMMBOT", parent=self)
        self.logoText.move(10, 30)
        
        self.scroll = QScrollArea()
        container = QWidget()
        containerLayout = QVBoxLayout()
        container.setLayout(containerLayout)

        searchBar = QLabel('<font size="4"> Put Search Bar Here </font>')
        containerLayout.addWidget(searchBar)

        algoOne = QLabel('<font size="4"> Movies for users like you </font>')
        containerLayout.addWidget(algoOne)
        algoOneCall = algorithm.get_top_n(FirestoreDataAccess.getFavs(FirestoreDataAccess(app=mainApp), "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ"), n=5)
        top5 = algoOneCall[0]
        for movie in top5:
            widgey = movieWidget(movie, 'aimmbotlogo.png')
            self.vbox.addWidget(widgey)

        movie = movieWidget('Testing', 'aimmbotlogo.png')
        containerLayout.addWidget(movie)
        self.setCentralWidget(container)
        self.createToolBar()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        #self.scroll.setWidget(self.container)

    def createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        tools.addAction("Login", self.logWindow)
        tools.addAction("Register", self.regWindow)
        tools.addAction("My Favorites", self.favWindow)
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
    
    def favWindow(self):
        self.rf = favoritesWindow()
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

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.updateUser)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        button_exit = QPushButton('Return')
        button_exit.clicked.connect(window.show)
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit, 3, 0, 1, 2)

        self.setLayout(layout)

    def updateUser(self):

        currentUser = signin.sign_in_with_email_and_password(email=self.lineEdit_username.text(), password=self.lineEdit_password.text())
        
        msg = QMessageBox()
        try:
            returnStr = currentUser['error']['message']
            if(returnStr == 'INVALID_PASSWORD'):
                returnStr = "Invalid Password"
            if(returnStr == 'INVALID_EMAIL'):
                returnStr = "Email Not Recognized"
            msg.setText(returnStr)
            msg.exec()
        except:
            msg.setText("Logged In Succesfully")
            msg.exec_()
            msg.hide()
            self.hide()
            window.show()
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

        button_reg = QPushButton('Register')
        button_reg.clicked.connect(self.register_user)
        layout.addWidget(button_reg, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        button_exit = QPushButton('Return')
        button_exit.clicked.connect(window.show)
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit, 3, 0, 1, 2)

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

#window that allows users to add a favourite movie
class favoritesWindow(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("My Favorites")
        self.resize(1500, 800)
        layout = QGridLayout()

        button_exit = QPushButton('Return')
        button_exit.clicked.connect(window.show)
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit, 0, 0)
        
        userFavs = FirestoreDataAccess.getFavs(FirestoreDataAccess(app=mainApp), "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ") #Need to get the uid

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout() 

        for movie in userFavs:
            widgey = movieWidget(movie, 'aimmbotlogo.png')
            self.vbox.addWidget(widgey)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        layout.addWidget(self.scroll)

        self.setLayout(layout)
  
    
if __name__ == "__main__":
    currentUser = NULL
    app = QApplication([])
    app.setStyle('Oxygen')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())