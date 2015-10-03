from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMenu
from IconWidget import IconWidget
import os
import shutil


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16
    clipicon = None
    windowclass_signal = pyqtSignal(str)
    query = pyqtSignal()

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)
        self.setMinimumSize(400, 200)
        self.setAcceptDrops(True)
        self.path = path
        self.icons = []
        # self.clipicon = None
        for name in os.listdir(path):
            icon_widget = IconWidget(self, name=name, path=self.path)
            icon_widget.new_window.connect(self.windowclass_signal.emit)
            icon_widget.clipboard.connect(self.on_clipboard)
            self.icons.append(icon_widget)
            # self.icons[-1].move(DragWidget.spacerX, DragWidget.spacerY)
            self.icons[-1].setAttribute(Qt.WA_DeleteOnClose)
        self.clean_up()
        self.updateScrollArea()

    def updateScrollArea(self):
        """ set the dimension of the widget """
        iconx = []
        icony = []
        for item in self.icons:
            iconx.append(item.x())
            icony.append(item.y())
        self.setMinimumWidth(max(iconx)+100)
        self.setMinimumHeight(max(icony)+75)
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasFormat("application/x-icon"):
            name = event.source().name
            icon_widget = IconWidget(self, name=name, path=self.path)
            icon_widget.new_window.connect(self.windowclass_signal.emit)
            self.icons.append(icon_widget)
            self.icons[-1].move(event.pos().x(), event.pos().y())
            self.icons[-1].show()
            self.updateScrollArea()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            for item in self.icons:
                item.reset_selection()

        if event.buttons() == Qt.RightButton:
            menu = QMenu("Window Menu")
            clean = menu.addAction("Clean Up")
            clean.triggered.connect(self.clean_up)
            if DragWidget.clipicon is not None:
                paste = menu.addAction("Paste")
                paste.triggered.connect(self.paste_icon)
            eventpos = event.screenPos()
            qpoint = QPoint(eventpos.x(), eventpos.y())
            menu.exec_(qpoint)

    def mouseDoubleClickEvent(self, event):
        print("Double Click") 
        self.query.emit()

    def clean_up(self):
        print("clean_up method")
        DragWidget.spacerX = 16
        DragWidget.spacerY = 16
        print("sw=", self.window().width())
        for item in self.icons:
            item.move(DragWidget.spacerX, DragWidget.spacerY)
            # initial icon placement
            DragWidget.spacerX += 100
            if DragWidget.spacerX + 100 > self.window().width():
                DragWidget.spacerY += 75
                DragWidget.spacerX = 16
        # reset placement values

        self.updateScrollArea()

    def paste_icon(self):
        print("---")
        print("srce=", self.clipicon.path + "/" + self.clipicon.name)
        # print("res=", self.clipicon.path + "/" + self.clipicon.name)
        print("dest=", self.path + "/")

        # if os.path.isdir(os.path.join(self.clipicon.path, self.clipicon.name)):
        SRCE = self.clipicon.path + "/" + self.clipicon.name
        DEST = self.path+"/" + self.clipicon.name
        shutil.copytree(SRCE, DEST)

    def on_clipboard(self, icon):
        print("realpath", self.path)
        print("clip_icon_name=", icon.name)
        DragWidget.clipicon = icon
