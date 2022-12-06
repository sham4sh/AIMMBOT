# Main file. Main page and all pop up windows are defined here.

from asyncio.windows_events import NULL
from sqlite3 import Cursor
import sys
import requests
import json
import signin
import keywordSearch
import pprint
import random
from PyQt5.QtWidgets import (QApplication, QScrollArea, QLabel, QVBoxLayout, QMainWindow, QStatusBar, QToolBar, QLineEdit, QGridLayout, QWidget, QPushButton, QMessageBox, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QSize
import pandas as pd
import numpy as np
import firebase_admin
from algorithms.primaryAlgorithm import (PrimaryAlgorithm)
from algorithms.secondaryAlgorithm import (SecondaryAlgorithm)
from UserDataFirebase import FirestoreDataAccess
from Cinemagoer import CinemagoerMovie
from firebase_admin import credentials
from firebase_admin import auth
import currentData
cred = credentials.Certificate("aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json")
mainApp = firebase_admin.initialize_app(cred)
FDA = FirestoreDataAccess(mainApp)
cur = currentData.currentData()

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

        label_searchBar = QLabel('<font size="4"> Search: </font>')
        self.lineEdit_searchBar = QLineEdit()
        self.lineEdit_searchBar.setPlaceholderText('Enter a keyword')
        containerLayout.addWidget(label_searchBar)
        containerLayout.addWidget(self.lineEdit_searchBar)

        button_search = QPushButton('Go!')
        button_search.clicked.connect(self.srchWindow)
        containerLayout.addWidget(button_search)

        algoOne = QLabel('<font size="4"> Movies for users like you </font>')
        containerLayout.addWidget(algoOne)
        a1=PrimaryAlgorithm()
        df = a1.processData(cur.getUser())
        top10 = a1.get_top_n(cur.getUser(), FDA.getFavs(cur.getUser()))
        for movie in top10:
            id = movie.item()
            widget = movieWidget(str(id))
            containerLayout.addWidget(widget)

        #userFavs = FirestoreDataAccess.getFavs(FirestoreDataAccess(app=mainApp), cur.getUser())
        #randMovie = random.choice(list(userFavs.items()))
        #algoTwo = QLabel('<font size="4"> Movies like %s</font>'%randMovie[0])
        #containerLayout.addWidget(algoTwo)
        '''df = pd.read_csv('data/links.csv')
        assert 'movieId' in df.columns and 'imdbId' in df.columns
        ind = df[df['imdbId']==randMovie[0]].index.values
        mid = df.loc[ind,'movieId'].values[1]
        a2 = SecondaryAlgorithm()
        a2Recommends = a2.get_top_n(mid)
        for movie in a2Recommends:
            widget = customWidgets.movieWidget(str(movie))             
            containerLayout.addWidget(widget)'''

    
        container.setLayout(containerLayout)


        self.setCentralWidget(self.scroll)
        self.createToolBar()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(container)

    def createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        tools.addAction("Login", self.logWindow)
        tools.addAction("Register", self.regWindow)
        tools.addAction("Watchlist", self.favWindow)
        tools.addAction("Refresh", self.refresh)
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
        self.ff = favoritesWindow()
        self.ff.show()
        self.hide()
    def srchWindow(self):
        cur.updateKeyword(self.lineEdit_searchBar.text())
        self.sf = searchWindow()
        self.sf.show()
        self.hide()
    def refresh(self):
        #cur.updateUser('testUser')
        self.newWin = MainWindow()
        self.newWin.show()
        self.close()


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
            cur.updateUser(currentUser['localId'])
            #print(cur.getUser())
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
            currentUser = signin.sign_in_with_email_and_password(email=self.lineEdit_username.text(), password=self.lineEdit_password.text())
            cur.updateUser(currentUser['localId'])
            msg.setText("Account Created Succesfully! Add some movies to your watchlist and get started!")
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
        self.setWindowTitle("My Watchlist")
        self.resize(1500, 800)
        layout = QGridLayout()

        button_exit = QPushButton('Return')
        button_exit.clicked.connect(window.show)
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit, 0, 0)
        
        userFavs = FirestoreDataAccess.getFavs(FirestoreDataAccess(app=mainApp), cur.getUser()) #Need to get the uid

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout() 

        for movie in userFavs:
            widgey = movieWidget(movie)
            self.vbox.addWidget(widgey)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        layout.addWidget(self.scroll)

        self.setLayout(layout)

class searchWindow(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Search")
        self.resize(1500, 800)
        layout = QGridLayout()

        button_exit = QPushButton('Return')
        button_exit.clicked.connect(window.show)
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit)


        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout() 

        self.populate(cur.getKeyword())

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        layout.addWidget(self.scroll)

        self.setLayout(layout)

    def populate(self, input):
        df = pd.read_csv('data/movies_detailed.csv')
        for ind in df.index:
            if (input.upper() in str(df['plot'][ind]).upper() or input.upper() in str(df['title'][ind]).upper()):
                widget = movieWidget(df['imdbId'][ind])
                self.vbox.addWidget(widget)

class movieWidget(QWidget):

    def __init__(self, name):
        super(movieWidget, self).__init__()

        self.is_on = False # Current state (true=ON, false=OFF)
        self.title = "Hot Tub Time Machine"
        self.id = 1231587
        im = 'hottubtimemachine.png'

        df = pd.read_csv('data/movies_detailed.csv')

        for ind in df.index:
            if (str(name) == str(df['imdbId'][ind])):
                self.title = df['title'][ind]
                self.id = name
                im = QImage()
                im.loadFromData(requests.get(df['coverURL'][ind]).content)

        self.lbl = QLabel(self.title)    #  The widget label
        self.btn = QPushButton(self.title)     

        self.btn.clicked.connect(self.movWin)
        

        self.pixmap = QPixmap(im)

        # adding image to label
        self.lbl.setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        self.lbl.resize(self.pixmap.width(),
                          self.pixmap.height())
 

        self.hbox = QHBoxLayout()       # A horizontal layout to encapsulate the above
        self.hbox.addWidget(self.lbl)   # Add the label to the layout
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)

    def movWin(self):
        self.win = movieWindow()
        self.win.fillWindow(int(self.id))
        self.win.show()

        



class movieWindow(QWidget):

    def __init__(self): 
        super().__init__()
        #self.db = firestore.Client(credentials=credentials.Certificate("aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json"))
        cred = credentials.Certificate("aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json")
        self.mainApp = firebase_admin.initialize_app(cred, name=str(random.randint(0, 1000)))
        self.FDA = FirestoreDataAccess(self.mainApp)

        


    def activated(self, index):

        values = self.FDA.getFavs(cur.getUser())
        if(index == 6):
            self.FDA.removeFav(cur.getUser(), str(self.id))
        if(index > 0 and index < 6):
            values = self.FDA.addFav(cur.getUser(), str(self.id), index)
    
    def fillWindow(self, imdbId):
        title = ''
        url = ''
        plot = ''
        year = ''
        self.id = imdbId

        df = pd.read_csv('data/movies_detailed.csv')
        for ind in df.index:
            if (imdbId == df['imdbId'][ind]):
                title = df['title'][ind]
                url = df['coverURL'][ind]
                year = df['year'][ind]
                plot = df['plot'][ind]

        try:
            im = QImage()
            im.loadFromData(requests.get(url).content)
        except:
            im = 'aimmbotlogo.png'
        
        self.setWindowTitle(title)
        self.resize(1200, 600)
        layout = QGridLayout()

        self.cover = QLabel(title)  
        self.info = QLabel(title +", " + str(year))
        self.info.setFont(QFont('Arial', 20))
        self.plotlbl = QLabel(str(plot))
        self.plotlbl.setGeometry(200, 200, 200, 200)
        self.plotlbl.setWordWrap = False
        self.plotlbl.setFont(QFont('Arial', 15))
        #self.plotlbl.setStyleSheet("border : 2px solid black;")

        self.pixmap = QPixmap(im)
        scaled_pixmap = self.pixmap.scaled(200, 200, 1, 0)

        # adding image to label
        self.cover.setPixmap(scaled_pixmap)
 
        # Optional, resize label to image size
        self.cover.resize(self.pixmap.width(), self.pixmap.height())

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout() 

        self.vbox.addWidget(self.plotlbl)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        combobox = QComboBox()
        combobox.addItems(['RATE FILM', 'One Star', 'Two Stars', 'Three Stars', 'Four Stars', 'Five Stars', 'REMOVE RATING'])

        # Connect signals to the methods.
        rating = ''
        combobox.activated.connect(self.activated)

        combobox.setFont(QFont('Arial', 10))


        button_exit = QPushButton('Return')
        button_exit.clicked.connect(self.hide)
        layout.addWidget(button_exit, 0, 0)
        layout.addWidget(self.cover, 1, 0)
        layout.addWidget(self.info, 1, 1)
        layout.addWidget(self.scroll, 2, 0, 1, 1)
        layout.addWidget(combobox, 2, 1)
        
        

        self.setLayout(layout)


  
    
if __name__ == "__main__":
    #currentData = NULL
    app = QApplication([])
    app.setStyle('Oxygen')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())