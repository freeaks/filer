from PyQt5.QtGui import QPixmap, QPalette, QDrag
from PyQt5.QtCore import Qt, QByteArray, QMimeData, QPoint, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMenu, QSizePolicy 
import os
# import shutil


class ClickableIcon(QLabel):
 
    clicked = pyqtSignal()  
 
    def __init__(self, path=None, name=None, parent=None):
        super(ClickableIcon, self).__init__(parent)
        self.selected = False
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setAutoFillBackground(True)

    def mousePressEvent(self, event):

        self.clicked.emit()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)
        print("clickedicon")
        event.accept()


class ClickableLabel(QLabel):
 
    clicked = pyqtSignal()  
 
    def __init__(self, path=None, name=None, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.selected = False
        # self.setAutoFillBackground(True)
 
    def mousePressEvent(self, event):
        self.clicked.emit()
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)
        print("clickedlabel")
        event.accept()


class IconWidget(QWidget):
    new_window = pyqtSignal(str)
    clipboard = pyqtSignal(object)

    def __init__(self, parent=None, name="None", path="None"):
        super().__init__(parent)
        self.name = name
        self._drag_started = False
        string_width = self.fontMetrics().boundingRect(name).width() 
        self.mimetext = "application/x-icon"
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.text = ClickableLabel(path=path, name=name)
        self.text.clicked.connect(self._on_drag_started)
        self.icon = ClickableIcon(path=path, name=name)
        self.icon.clicked.connect(self._on_drag_started)
        
        self.iconRender(path, name)
        self.setText(name)
        self.path = path
        self.kind = "icon or directory"
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)

    def iconRender(self, path, name):
        if os.path.isdir(os.path.join(path, name)):
            self.setIcon(QPixmap("./images/folder.png"))
            self.kind = "directory"
        else:
            self.setIcon(QPixmap("./images/file.png"))
            self.kind = "file"

    def IconSelect(self, status):
        if status:
            self.text.selected = True 
            self.icon.selected = True
            self.setColor()
        else:
            self.text.selected = False
            self.icon.selected = False
            self.icon.setAutoFillBackground(False)

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
        self.icon.setPalette(palette)

    def resetColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.black)
        self.text.setPalette(palette)
        self.icon.setPalette(palette)

    def mouseMoveEvent(self, event):
        # if the left mouse button is used
        if self._drag_started:
            data = QByteArray()
            mime_data = QMimeData()
            mime_data.setData(self.mimetext, data)
            drag = QDrag(self) 
            drag.setMimeData(mime_data)
            drag.setHotSpot(self.rect().topLeft())  # where do we drag from
            if drag.exec_(Qt.MoveAction):
                self.parent().icons.remove(self)
                self.deleteLater()

    def _on_drag_started(self):
        self._drag_started = True

    def mousePressEvent(self, event):
        # if event.buttons() == Qt.LeftButton: 
        #     # for item in self.parent().icons:
        #     #    item.icon.mousePressedButton(event)
        #     #    item.text.mousePressedButton(event)
        #     # self.IconSelect(True)
        #     # self.icon.mousePressedButton(event)
        #     pass
        if event.buttons() == Qt.RightButton:
            menu = QMenu("Icon Menu")
            copy = menu.addAction("Copy")
            copy.triggered.connect(self.copy_icon)
            delete = menu.addAction("Delete")
            delete.triggered.connect(self.delete_icon)
            eventpos = event.screenPos()
            qpoint = QPoint(eventpos.x(), eventpos.y())
            menu.exec_(qpoint)

    def mouseDoubleClickEvent(self, event):
        if self.kind == "directory": 
            self.new_window.emit(os.path.join(self.path, self.name))

    def copy_icon(self):
        print("copy_icon method")
        self.clipboard.emit(self)
        pass

    def delete_icon(self):
        print("delete_icon method")
        pass
