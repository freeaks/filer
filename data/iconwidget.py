
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import (Qt, QByteArray, QMimeData, 
                          QPoint, pyqtSignal, QProcess)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QMenu, QSizePolicy)
import os
import configparser
# import shutil


class IconWidget(QWidget):
    new_window = pyqtSignal(str)
    clipboard = pyqtSignal(object)

    def __init__(self, parent=None, name="None", path="None"):
        super().__init__(parent)
        self.path = path
        self.name = name
        self.drag_started = False 
        self.mimetext = "application/x-icon"
        self.mpixmap = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.kind = self.what_kind(path, name)
        self.text = ClickableLabel(path=path, name=name)
        self.icon = ClickableIcon(path=path, name=name, parent=self)
        self.icon.clicked.connect(self._on_drag_started)
        self.icon.double_clicked.connect(self.open_window)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)

    def what_kind(self, path, name):
        if os.path.isdir(os.path.join(path, name)):
            return "directory"
        return "file"

    def reset_selection(self):
        self.icon.selected = False
        self.icon.setAutoFillBackground(False)

    def getIconWidget(self):
        return self

    def getIcon(self):
        return self.icon

    def getText(self):
        return self.text

    def mouseMoveEvent(self, event):
        # if the left mouse button is used
        if self.drag_started:
            data = QByteArray()
            mime_data = QMimeData()
            mime_data.setData(self.mimetext, data)
            drag = QDrag(self) 
            drag.setMimeData(mime_data)
            drag.setPixmap(self.icon.get_icon())
            drag.setHotSpot(self.rect().topLeft())  # where do we drag from
            if drag.exec_(Qt.MoveAction):
                self.parent().icons.remove(self)
                self.deleteLater()

    def _on_drag_started(self):
        self.drag_started = True

    def open_window(self):
        self.reset_selection()
        self.new_window.emit(os.path.join(self.path, self.name))


class ClickableIcon(QLabel):
 
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()
 
    def __init__(self, path=None, name=None, parent=None):
        super(ClickableIcon, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 
        self.config = configparser.ConfigParser()
        self.config.read('prefs.cfg')
        self.selected = False
        self.name = name
        self.path = path
        self.icon = None
        self.kind = self.parent().kind
        self.select_icon(name)

    def select_icon(self, name):
        if self.kind == "directory":
            self.set_icon(QPixmap("./images/folder.png"))
        else:
            if self.config.has_option('icons', name.rsplit('.', 1)[1]):
                OPTION = self.config.get('icons', name.rsplit('.', 1)[1])
                self.set_icon(QPixmap("./images/"+OPTION))
            else:
                self.set_icon(QPixmap("./images/file.png"))

    def set_icon(self, icon):
        self.setPixmap(icon)
        self.icon = icon

    def mousePressEvent(self, event):
        # event.accept()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)

        if event.buttons() == Qt.LeftButton: 
            self.clicked.emit()
            print("clickedicon=", self.name)
            
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
            self.double_clicked.emit()
        else:
            print("execute =", os.path.join(self.path, self.name))
            file = "\"" + os.path.join(self.path, self.name) + "\""
            QProcess.execute("/usr/bin/open " + file)
            # event.accept()

    def copy_icon(self):
        print("copy_icon method")
        self.clipboard.emit(self)
        pass

    def delete_icon(self):
        print("delete_icon method")
        pass

    def get_icon(self):
        return self.icon 


class ClickableLabel(QLabel):

    def __init__(self, path=None, name=None, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.string_width = None
        self.selected = False
        self.name = name
        self.path = path
        self.set_name(name)
        # self.property
        config = configparser.ConfigParser()
        config.read('prefs.cfg')
        self.color = config.get("colors", "label")
        self.setStyleSheet("""QLabel{color:""" +
                           self.color +
                           """;}""")

    def set_name(self, name):
        temp_name = None
        label_length = len(name)
        if label_length > 11:
            if label_length < 22:
                temp_name = name[:10] + "\n" + name[10:]
            elif label_length > 22:
                temp_name = name[:10] + "\n" + name[10:17] + "..." + name[-3:]
            self.setText(temp_name)
        else:
            self.setText(name)
