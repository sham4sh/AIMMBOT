from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout, QScrollArea, QVBoxLayout, QFormLayout, QComboBox)
from PyQt5.QtGui import (QPixmap, QImage, QFont)
from PyQt5 import Qt
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
import pandas as pd
from PIL import Image
import requests
import sys
from UserDataFirebase import FirestoreDataAccess
from google.cloud import firestore
from firebase_admin import credentials


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

        


    def activated(self, index):
        #self.db.collection(u'users').document(cur.getUser()).set({
        #    self.id : index       
        #})
        print("Activated index:", index)
    
    def fillWindow(self, imdbId):
        title = ''
        url = ''
        plot = ''
        year = ''

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





#app = QApplication([])
#win = movieWindow()
#win.fillWindow(1231587)
#win.show()
#sys.exit(app.exec())
