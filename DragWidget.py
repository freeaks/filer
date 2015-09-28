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
        self.icon = IconWidget(self, name="name", path=self.path)
        # for name in os.listdir(path):
        #     self.icon = IconWidget(self, name=name, path=path)
        #     self.icon.move(DragWidget.spacerX, DragWidget.spacerY)
        #     self.icon.setAttribute(Qt.WA_DeleteOnClose)
            # initial icon placement
        #     DragWidget.spacerX += 64
        #     if DragWidget.spacerX + 64 > self.minimumWidth():
        #         DragWidget.spacerY += 64
        #         DragWidget.spacerX = 16
        # # reset placement values
        # DragWidget.spacerX = 16
        # DragWidget.spacerY = 16

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
                # self.icon.move(event.pos().x(), event.pos().y())
                self.icon = IconWidget(self, name="name", path=self.path)
                self.updateScrollArea()

    def mousePressEvent(self, event):
        self.mchild = self.childAt(event.pos())
        # click on nothing cancels selection
        if self.childAt(event.pos()) == None:
            self.icon.IconSelect("notselected")

        # click on icon to select it
        for item in self.children():
            if item.getIcon() == self.mchild:
                self.icon.IconSelect("notselected")
                self.icon = item
                self.icon.IconSelect("selected")

    def mouseDoubleClickEvent(self, event):
        print("Double Click")
