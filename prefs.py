#!/usr/bin/env python3

import sys
import configparser
# from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import(
    QWidget, QListWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
    QListWidgetItem,
    QApplication, QLineEdit, QPushButton)


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

        # lineEdits
        self.pattern = QLineEdit()
        self.extention = QLineEdit()
        self.filename = QLineEdit()
        
        # buttons
        self.add_type = QPushButton("add type")
        self.del_type = QPushButton("del type")

        # layouts
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(5, 5, 5, 0)
        self.mainlayout.setSpacing(7)
        self.change_pattern_layout = QFormLayout()
        self.add_filetype_layout = QFormLayout()
        self.add_del_button_layout = QHBoxLayout()
        self.change_pattern_layout.addRow('pattern', self.pattern)
        self.add_filetype_layout.addRow('extention', self.extention)
        self.add_filetype_layout.addRow('path to icon', self.filename)
        self.add_del_button_layout.addWidget(self.add_type)
        self.add_del_button_layout.addWidget(self.del_type)

        # layouts settings
        self.change_pattern_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.add_filetype_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # reading stored settings
        for key, value in config.items('icons'):
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp("filetype: " + key.upper())
            myQCustomQWidget.setTextDown(value)
            myQCustomQWidget.setIcon(value)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget) 

        self.mainlayout.addLayout(self.change_pattern_layout)
        self.mainlayout.addWidget(self.myQListWidget)
        self.mainlayout.addLayout(self.add_filetype_layout)    
        self.mainlayout.addLayout(self.add_del_button_layout)
        self.setLayout(self.mainlayout) 

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())
