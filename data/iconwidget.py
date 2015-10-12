
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import (Qt, QByteArray, QMimeData, 
                          pyqtSignal, QProcess)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QSizePolicy)
import os
import configparser
# import shutil


class IconWidget(QWidget):
    new_window = pyqtSignal(str)
    clipboard = pyqtSignal(object)

    def __init__(self, parent=None, name=None, path=None, dir=None):
        super().__init__(parent)
        self.path = path
        self.name = name
        self.drawer = dir
        self.moving_icons = []
        self.delete_flag = False
        self.drag_started = False 
        self.mimetext = "application/x-icon"
        self.mpixmap = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.text = ClickableLabel(path=path, name=name)
        self.icon = ClickableIcon(path=path, name=name, drawer=dir, parent=self)
        # self.icon.clicked.connect(self._on_drag_started)
        self.icon.double_clicked.connect(self.open_window)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)

    def reset_selection(self):
        for item in self.parent().icons: 
            item.icon.selected = False
            item.icon.setAutoFillBackground(False)
        # print("reset selection", len(self.parent().icons))

    def getIconWidget(self):
        return self

    def getIcon(self):
        return self.icon

    def getText(self):
        return self.text

    def get_modifier(self):
        # print("modif", self.parent().get_modifier())
        return self.parent().get_modifier()

    def mouseMoveEvent(self, event):
        # print("(iw) parent=", self.parent())
        # for item in self.parent().icons:
        #     if item.icon.selected:
        #         item.delete_flag = True
        #         self.moving_icons.append(item)

        # print("(iw) moving number=", len(self.moving_icons))

        # if self.drag_started:
        data = QByteArray()
        mime_data = QMimeData()
        mime_data.setData(self.mimetext, data)
        drag = QDrag(self) 
        drag.setMimeData(mime_data)
        drag.setPixmap(self.icon.get_icon())
        drag.setHotSpot(self.rect().topLeft())

        if drag.exec_(Qt.MoveAction):
            if len(self.parent().src_selected) > 0:
                for item in self.parent().src_selected:
                    self.parent().icons.remove(item)
                    item.deleteLater()
            else:
                self.parent().icons.remove(self)
                self.deleteLater()

        self.parent().src_selected.clear()
        self.parent().src_dragwidget = None

        #     if self in self.parent().icons:
        #         self.parent().icons.remove(self)
        #         self.deleteLater()
        # drag.exec_(Qt.MoveAction)

    def _on_drag_started(self):
        self.drag_started = True

    def open_window(self):
        self.reset_selection()
        self.new_window.emit(os.path.join(self.path, self.name))


class ClickableIcon(QLabel):
 
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()
 
    def __init__(self, path=None, name=None, parent=None, drawer=None):
        super(ClickableIcon, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setFrameShape
        self.parent = parent
        self.config = configparser.ConfigParser()
        self.config.read('prefs.cfg')
        self.selected = False
        self.name = name
        self.path = path
        self.icon = None
        self.drawer = drawer
        self.apply_icon(name)

    def apply_icon(self, name):
        """ parse cfg file to assign icon or use fallback """
        if self.drawer:
            self.set_icon(QPixmap("./images/folder.png"))
        else:
            try:
                OPTION = self.config.get('icons', name.rsplit('.', 1)[1])
                self.set_icon(QPixmap(OPTION))
            except:
                self.set_icon(QPixmap("./images/file.png"))

    def set_icon(self, icon):
        self.setPixmap(icon)
        self.icon = icon

    def icon_selection_mode(self):
        """ choose between multi or single icon selection """
        # if self.parent.get_modifier():
        #     self.select_icon()
        # else:
        #     self.parent.reset_selection()
        #     self.select_icon()
        self.select_icon()

    def deselect_icon(self):
        self.selected = False
        self.setAutoFillBackground(False)

    def select_icon(self):
        self.setAutoFillBackground(True)
        self.selected = True
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)
        self.clicked.emit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton: 
                self.icon_selection_mode()

    def mouseDoubleClickEvent(self, event):
        if self.drawer:
            self.double_clicked.emit()
        else:
            file = "\"" + os.path.join(self.path, self.name) + "\""
            QProcess.execute("/usr/bin/open " + file)

    def copy_icon(self):
        print("copy_icon method")
        self.clipboard.emit(self)

    def delete_icon(self):
        print("delete_icon method")

    def get_icon(self):
        return self.icon 


class ClickableLabel(QLabel):

    """ icon filename class """

    def __init__(self, path=None, name=None, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # self.setGeometry(QRect(0, 40, 40, 40))
        self.selected = False
        self.name = name
        self.path = path
        self.set_name(name)
        config = configparser.ConfigParser()
        config.read('prefs.cfg')
        self.color = config.get("colors", "label")
        self.setStyleSheet("""QLabel{color:""" +
                           self.color +
                           """;}""")

    def set_name(self, name):
        """ set icon label """
        temp_name = None
        label_length = len(name)       
        if label_length > 11:
            if label_length < 22:
                temp_name = name[:10] + "\n" + name[10:]
            elif label_length >= 22:
                temp_name = name[:10] + "\n" + name[10:17] + "..." + name[-3:]
            self.setText(temp_name)
        else:
            self.setText(name)
