from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout)
from PyQt5.QtGui import (QPixmap, QImage)
import pandas as pd
from PIL import Image
import requests


class movieWidget(QWidget):

    def __init__(self, name):
        super(movieWidget, self).__init__()

        self.is_on = False # Current state (true=ON, false=OFF)
        title = "Default"
        im = 'aimmbotlogo.png'

        df = pd.read_csv('data/movies_detailed.csv')

        for ind in df.index:
            if (str(name) == str(df['imdbId'][ind])):
                title = df['title'][ind]
                im = QImage()
                im.loadFromData(requests.get(df['coverURL'][ind]).content)

        self.lbl = QLabel(title)    #  The widget label
        self.btn = QPushButton(title)     

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