from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from IconWidget import *
import os


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16
    go_deeper = pyqtSignal(str)

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setAcceptDrops(True)
        self.path = path
        self.icons = []
        self.temp_drop = ""
        for name in os.listdir(path):
            # self.icons.append(IconWidget(self, name=name, path=self.path))
            icon_widget = IconWidget(self, name=name, path=self.path)
            icon_widget.go_deeper.connect(self.go_deeper.emit)
            self.icons.append(icon_widget)
            self.icons[-1].move(DragWidget.spacerX, DragWidget.spacerY)
            self.icons[-1].setAttribute(Qt.WA_DeleteOnClose)
            # initial icon placement
            DragWidget.spacerX += 64
            if DragWidget.spacerX + 64 > self.minimumWidth():
                DragWidget.spacerY += 64
                DragWidget.spacerX = 16
        # reset placement values
        DragWidget.spacerX = 16
        DragWidget.spacerY = 16
        self.updateScrollArea()

    def updateScrollArea(self):
        """ set the dimension of the widget """
        iconx = []
        icony = []
        for item in self.icons:
                iconx.append(item.x())
                icony.append(item.y())
        self.setMinimumWidth(max(iconx)+64)
        self.setMinimumHeight(max(icony)+64)
        pass
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        # if self.icon.selected:
        event.accept()
        if event.mimeData().hasFormat("application/x-icon"):
            # print("icon=", event.source().name)
            name = event.source().name
            self.icons.append(IconWidget(self, name=name, path=self.path))
            # print("dropEvent len=", len(self.icons))
            self.icons[-1].move(event.pos().x(), event.pos().y())
            self.icons[-1].show()
            self.updateScrollArea()

    def mousePressEvent(self, event):
        for item in self.icons:
            item.IconSelect(False)

    def mouseDoubleClickEvent(self, event):
        print("Double Click")
        # Window("./test-tree")
