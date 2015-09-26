from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from IconWidget import *
import os


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setAcceptDrops(True)
        self.path = path
        # self.name = name
        for name in os.listdir(path):
            self.icon = IconWidget(self, name=name, path=path, dire=os.path.isfile(name))
            self.icon.move(DragWidget.spacerX, DragWidget.spacerY)
            self.icon.setAttribute(Qt.WA_DeleteOnClose)
            # initial icon placement
            DragWidget.spacerX += 64
            if DragWidget.spacerX + 64 > self.minimumWidth():
                DragWidget.spacerY += 64
                DragWidget.spacerX = 16
        # reset placement values
        DragWidget.spacerX = 16
        DragWidget.spacerY = 16

    def updateScrollArea(self):
        """ set the dimension of the widget """
        iconx = []
        icony = []
        for item in self.children():
            if type(item) == IconWidget:
                iconx.append(item.x())
                icony.append(item.y())
        self.setMinimumWidth(max(iconx)+64)
        self.setMinimumHeight(max(icony)+64)
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if self.icon.selected:
            event.accept()
            if event.mimeData().hasFormat("application/x-icon"):
                self.icon.move(event.pos().x(), event.pos().y())
                self.updateScrollArea()

    def mouseMoveEvent(self, event):
        # if the left mouse button is used
        if event.buttons() == Qt.LeftButton:
            if self.icon.selected:
                self.mimetext = self.icon.mimetext
                data = QByteArray()
                mime_data = QMimeData()
                mime_data.setData(self.mimetext, data)
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                drag.setHotSpot(self.rect().topLeft())  # where do we drag from
                drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, event):
        self.mchild = self.childAt(event.pos())
        # click on nothing cancels selection
        if self.childAt(event.pos()) == None:
            self.icon.updateIcon("notselected")

        # click on icon to select it
        for item in self.children():
            if item.getIcon() == self.mchild:
                self.icon.updateIcon("notselected")
                self.icon = item
                self.icon.updateIcon("selected")

    def mouseDoubleClickEvent(self, event):
        print("Double Click")
