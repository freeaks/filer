#!/usr/bin/env python3

import sys
import os
import configparser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import(
    QWidget, QListWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame,
    QListWidgetItem, QGroupBox, QButtonGroup, QColorDialog, QFileDialog,
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
        self.config = configparser.ConfigParser()
        self.config.read('prefs.cfg')

        self.extention = QLineEdit()
        self.filename = QLineEdit()
        self.add_type = QPushButton("add type")
        self.del_type = QPushButton("del type")
        self.color_button = color_picker(parent=self)
        self.pattern_icon = Pattern_button(parent=self)
        self.radio_button_one = QRadioButton('Classic')
        self.radio_button_two = QRadioButton('Magellan')
        self.radio_group = QGroupBox('operation mode')
        self.radio_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.pattern_group = QGroupBox('window pattern and text color')
        self.pattern_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_one)
        self.button_group.addButton(self.radio_button_two)
        self.button_group.setId(self.radio_button_one, 1)
        self.button_group.setId(self.radio_button_two, 2)

        self.mainlayout = QVBoxLayout()
        self.holdgroups_layout = QHBoxLayout()
        self.radio_button_layout = QVBoxLayout()
        self.pattern_label_layout = QHBoxLayout()
        self.add_filetype_layout = QFormLayout()
        self.add_del_button_layout = QHBoxLayout()

        # adding
        self.holdgroups_layout.addWidget(self.radio_group)
        self.holdgroups_layout.addWidget(self.pattern_group)

        self.pattern_label_layout.addWidget(self.pattern_icon)
        self.pattern_label_layout.addStretch(1)
        self.pattern_label_layout.addWidget(self.color_button)
        self.pattern_label_layout.addStretch(1)
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
        # self.pattern_icon.setPixmap(QPixmap("./images/pattern.png").scaledToWidth(80)) 
        self.mainlayout.setContentsMargins(5, 5, 5, 0)
        self.mainlayout.setSpacing(7)   

        # reading stored settings
        for key, value in self.config.items('icons'):
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


class Pattern_button(QLabel):

    def __init__(self, parent=None):
        super(Pattern_button, self).__init__()
        # self.set_image("./images/pattern.png")
        self.parent = parent
        self.image = self.set_image(parent.config.get("background", "file"))
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)
        # self.setPixmap(QPixmap("./images/pattern.png").scaledToWidth(80))
        pass

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton: 
            fileName = QFileDialog.getOpenFileName(self, 'Title', './', filter='*.png')
            self.set_image(fileName[0])

    def set_image(self, image):
        self.setPixmap(QPixmap(image).scaledToWidth(80))
        self.parent.config.set('background', 'file', image)
        pref_file = open('prefs.cfg', 'w')
        self.parent.config.write(pref_file)
        pref_file.close()


class color_picker(QPushButton):

    def __init__(self, parent=None):
        super(color_picker, self).__init__()
        self.parent = parent
        self.color = self.set_color(parent.config.get("colors", "label"))
        self.setMaximumSize(40, 30)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.onColorPicker()
    
    def set_color(self, color):
        self.color = color
        self.setStyleSheet("background-color: %s;" % self.color)
        self.parent.config.set('colors', 'label', self.color)
        pref_file = open('prefs.cfg', 'w')
        self.parent.config.write(pref_file)
        pref_file.close()

    def onColorPicker(self):
        color = QColorDialog.getColor().name() 
        self.set_color(color)

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())
