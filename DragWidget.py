from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget
from IconWidget import IconWidget
import os


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16
    new_window = pyqtSignal(str)
    query = pyqtSignal()

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)
        self.setMinimumSize(200, 200)
        self.setAcceptDrops(True)
        self.path = path
        self.icons = []
        self.temp_drop = ""
        for name in os.listdir(path):
            icon_widget = IconWidget(self, name=name, path=self.path)
            icon_widget.new_window.connect(self.new_window.emit)
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
        event.accept()
        if event.mimeData().hasFormat("application/x-icon"):
            name = event.source().name
            icon_widget = IconWidget(self, name=name, path=self.path)
            icon_widget.new_window.connect(self.new_window.emit)
            self.icons.append(icon_widget)
            self.icons[-1].move(event.pos().x(), event.pos().y())
            self.icons[-1].show()
            self.updateScrollArea()

    def mousePressEvent(self, event):
        for item in self.icons:
            item.IconSelect(False)

    def mouseDoubleClickEvent(self, event):
        print("Double Click") 
        self.query.emit()
