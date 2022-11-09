from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout)
from PyQt5.QtGui import QPixmap


class movieWidget(QWidget):

    def __init__(self, name, image):
        super(movieWidget, self).__init__()

        self.name = name  # Name of widget used for searching.
        self.is_on = False # Current state (true=ON, false=OFF)

        self.lbl = QLabel(self.name)    #  The widget label
        self.btn_on = QPushButton("View")     # The ON button
        self.btn_off = QPushButton("Rate")   # The OFF button

        self.pixmap = QPixmap(image)

        # adding image to label
        self.lbl.setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        self.lbl.resize(self.pixmap.width(),
                          self.pixmap.height())
 

        self.hbox = QHBoxLayout()       # A horizontal layout to encapsulate the above
        self.hbox.addWidget(self.lbl)   # Add the label to the layout
        self.hbox.addWidget(self.btn_on)    # Add the ON button to the layout
        self.hbox.addWidget(self.btn_off)   # Add the OFF button to the layout
        self.setLayout(self.hbox)