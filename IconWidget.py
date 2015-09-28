from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os


class IconWidget(QWidget):

    def __init__(self, parent=None, name="None", path="None"):
        super().__init__(parent)
        self.mimetext = "application/x-icon"
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.icon = QLabel()
        self.text = QLabel(name)
        self.name = name
        self.path = path
        self.iconRender(path, name)
        self.selected = False
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)  
        # print("icon=", self)          

    def mouseMoveEvent(self, event):
        # if the left mouse button is used
        if event.buttons() == Qt.LeftButton:
            # if self.selected:
            data = QByteArray()
            mime_data = QMimeData()
            mime_data.setData(self.mimetext, data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(self.rect().topLeft())  # where do we drag from
            # drag.exec_(Qt.MoveAction)

            if drag.exec_(Qt.MoveAction): 
                # print("mouseMoveEv=", len(self.parent().icons))
                # print("deleting icon=", self)
                self.parent().icons.remove(self)
                self.deleteLater()

    def iconRender(self, path, name):
        if os.path.isdir(name):
            self.setIcon(QPixmap("./images/folder.png"))
        else:
            self.setIcon(QPixmap("./images/file.png"))

    def IconSelect(self, status):
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
