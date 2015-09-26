from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class IconWidget(QWidget):

    def __init__(self, parent=None, name="None", path="None", dire=False):
        super().__init__(parent)
        self.mimetext = "application/x-icon"
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.icon = QLabel()
        self.text = QLabel(name)
        self.name = name
        self.path = path
        self.dire = dire
        self.selected = False
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)
        if dire:
            self.setIcon(QPixmap("./images/folder.png"))
        else:
            self.setIcon(QPixmap("./images/file.png"))

    def updateIcon(self, status):
        if status == "selected":
            self.selected = True 
            self.setColor()
        else:
            self.selected = False
            self.resetColor()

    def setText(self, text):
        self.text.setText(text)

    def setIcon(self, icon):
        self.icon.setPixmap(icon)

    def getIconWidget(self):
        return self

    def getIcon(self):
        return self.icon

    def setColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.red)
        self.text.setPalette(palette)

    def resetColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.black)
        self.text.setPalette(palette)
