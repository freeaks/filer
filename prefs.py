#!/usr/bin/env python3

import sys
import os
import configparser
# from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import(
    QWidget, QListWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
    QListWidgetItem, QGroupBox, QButtonGroup, 
    QApplication, QLineEdit, QPushButton, QRadioButton, QSizePolicy)


class QCustomQWidget (QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textQVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.textQVBoxLayout.setSpacing(0)

        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.allQHBoxLayout.setSpacing(3)
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''color: rgb(0, 0, 255);''')
        self.textDownQLabel.setStyleSheet('''color: rgb(0, 0, 0);''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))


class exampleQMainWindow (QWidget):

    def __init__(self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.myQListWidget = QListWidget(self)
        self.myQListWidget.setStyleSheet("""
            QListWidget:item:selected:active {
            background-color:#A6A4FF;}
            """)

        self.setMinimumSize(350, 500)
        config = configparser.ConfigParser()
        config.read('prefs.cfg')

        self.extention = QLineEdit()
        self.filename = QLineEdit()
        self.add_type = QPushButton("add type")
        self.del_type = QPushButton("del type")
        self.pattern_label = QLabel()
        self.pattern_icon = QLabel()
        self.radio_button_one = QRadioButton('Classic')
        self.radio_button_two = QRadioButton('Magellan')
        self.radio_group = QGroupBox('operation mode')
        self.radio_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.pattern_group = QGroupBox('window pattern')
        self.pattern_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_one)
        self.button_group.addButton(self.radio_button_two)
        self.button_group.setId(self.radio_button_one, 1)
        self.button_group.setId(self.radio_button_two, 2)

        self.mainlayout = QVBoxLayout()
        self.holdgroups_layout = QHBoxLayout()
        self.radio_button_layout = QVBoxLayout()
        self.pattern_label_layout = QVBoxLayout()
        self.add_filetype_layout = QFormLayout()
        self.add_del_button_layout = QHBoxLayout()

        # adding
        self.holdgroups_layout.addWidget(self.radio_group)
        self.holdgroups_layout.addWidget(self.pattern_group)

        self.pattern_label_layout.addWidget(self.pattern_icon)
        self.pattern_group.setLayout(self.pattern_label_layout)

        self.radio_button_layout.addWidget(self.radio_button_one)
        self.radio_button_layout.addWidget(self.radio_button_two)
        self.radio_group.setLayout(self.radio_button_layout)

        self.add_filetype_layout.addRow('extention', self.extention)
        self.add_filetype_layout.addRow('path to icon', self.filename)
        self.add_del_button_layout.addWidget(self.add_type)
        self.add_del_button_layout.addWidget(self.del_type)

        # layouts settings 
        # self.radio_button_layout.setGeometry(QRect(10, 10, 10, 10))
        self.add_filetype_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.pattern_icon.setPixmap(QPixmap("./images/pattern.png").scaledToWidth(80)) 
        self.mainlayout.setContentsMargins(5, 5, 5, 0)
        self.mainlayout.setSpacing(7)   

        # reading stored settings
        for key, value in config.items('icons'):
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp("filetype: " + key.upper())
            myQCustomQWidget.setTextDown(value)
            myQCustomQWidget.setIcon(os.path.dirname(os.path.realpath(__file__)) + value)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget) 
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint()) 
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget) 

        # adding elements to layout
        self.mainlayout.addLayout(self.holdgroups_layout)
        self.mainlayout.insertSpacing(10, 10)
        self.mainlayout.addWidget(self.myQListWidget)
        self.mainlayout.addLayout(self.add_filetype_layout)    
        self.mainlayout.addLayout(self.add_del_button_layout)
        self.setLayout(self.mainlayout) 

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())
