from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt5.QtWidgets import QWidget, QRubberBand
# from PyQt5.QtGui import QRubberBand
from iconwidget import IconWidget, ClickableIcon, ClickableLabel
import os
import shutil


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16
    clipicon = None
    new_window_signal = pyqtSignal(str)
    query = pyqtSignal()

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)
        self.setMinimumSize(400, 200)
        self.setAcceptDrops(True)
        self.parent = parent
        # self.parent.modifier_signal.connect(self.get_modifier)
        self.modifier = False
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.path = path
        self.icons = []
        # self.clipicon = None
        for item in os.scandir(path):
            if item.is_dir():
                icon_widget = IconWidget(parent=self, name=item.name, path=self.path, dir=True)
            else:
                icon_widget = IconWidget(parent=self, name=item.name, path=self.path, dir=False)
            icon_widget.new_window.connect(self.new_window_signal.emit)
            icon_widget.clipboard.connect(self.on_clipboard)
            self.icons.append(icon_widget)
            self.icons[-1].setAttribute(Qt.WA_DeleteOnClose)
        self.clean_up()

    def updateScrollArea(self):
        """ set the dimension of the widget """
        iconx = []
        icony = []
        for item in self.icons:
            iconx.append(item.x())
            icony.append(item.y())
        self.setMinimumWidth(max(iconx)+75)
        self.setMinimumHeight(max(icony)+75)
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasFormat("application/x-icon"):
            name = event.source().name
            drawer = event.source().drawer
            # print("d=", drawer)
            if drawer:
                icon_widget = IconWidget(self, name=name, path=self.path, dir=True)
            else: 
                icon_widget = IconWidget(self, name=name, path=self.path, dir=False)
            icon_widget.new_window.connect(self.new_window_signal.emit)
            self.icons.append(icon_widget)
            self.icons[-1].move(event.pos().x(), event.pos().y())
            self.icons[-1].show()
            self.updateScrollArea()

    def get_modifier(self):
        return self.parent.modifier

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            for item in self.icons:
                item.icon.deselect_icon()
            
            self.origin = event.pos()
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QRect(self.origin, event.pos()).normalized())
        # QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        selected = []
        if self.rubberband.isVisible():
            self.rubberband.hide()
            
            rect = self.rubberband.geometry()
            for child in self.findChildren(IconWidget):
                
                if rect.intersects(child.geometry()):
                    selected.append(child)
                    child.icon.select_icon()
        print("selected len=", len(selected))

    def mouseDoubleClickEvent(self, event):
        print("Double Click") 
        self.query.emit()

    def focusInEvent(self, event):
        print("got focus=", self.path)

    def clean_up(self):
        print("clean_up method")
        # print("sw=", self.window().width())
        for item in self.icons:
            item.move(DragWidget.spacerX, DragWidget.spacerY)
            # initial icon placement
            DragWidget.spacerX += 100
            if DragWidget.spacerX + 100 > self.window().width():
                DragWidget.spacerY += 75
                DragWidget.spacerX = 16
        # reset placement values
        DragWidget.spacerX = 16
        DragWidget.spacerY = 16
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
