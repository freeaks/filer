#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
# from pprint import pprint


class DragWidget(QWidget):

    spacerX = 16
    spacerY = 16

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setAcceptDrops(True)
        self.path = path
        # for name in os.listdir(path):
        #     if os.path.isfile(os.path.join(path, name)):
        #         self.name = name
        #         foo = IconWidget(self)
        #         foo.setText(name)
        #         foo.setIcon(QPixmap('./images/file.png'))
        #         foo.move(DragWidget.spacerX, DragWidget.spacerY)
        #         foo.setAttribute(Qt.WA_DeleteOnClose)

        foo = IconWidget(self)
        foo.setText("name")
        foo.setIcon(QPixmap('./images/file.png'))
        foo.move(16, 16)
        foo.setAttribute(Qt.WA_DeleteOnClose)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                print("DragEnterEvent: event.source")
                event.acceptProposedAction()
        else:
            print("DragEnterEvent: event.mimeData")
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            itemData = event.mimeData().data('application/x-dnditemdata')
            dataStream = QDataStream(itemData, QIODevice.ReadOnly)

            pixmap = QPixmap()
            offset = QPoint()
            dataStream >> pixmap >> offset

            # newIcon = QLabel(self)
            # newIcon.setPixmap(pixmap)
            # newIcon.move(event.pos() - offset)
            # newIcon.show()
            # newIcon.setAttribute(Qt.WA_DeleteOnClose)

            newIcon = IconWidget(self)
            newIcon.setText("self.name")
            newIcon.setIcon(pixmap)
            newIcon.move(event.pos() - offset)
            newIcon.show()
            newIcon.setAttribute(Qt.WA_DeleteOnClose)

            print("dropEvent ..")

            if newIcon.y() + 32 > self.minimumHeight():
                self.setMinimumHeight(newIcon.y() + 32)

            if newIcon.x() + 32 > self.minimumWidth():
                self.setMinimumWidth(newIcon.x() + 32)

            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                print("dropEvent:  event.source")
                event.acceptProposedAction()
        else:
            print("dropEvent: event.mimeData")
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            prin("not child")
            return

        pixmap = QPixmap(child.pixmap())
        itemData = QByteArray()

        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        dataStream << pixmap << QPoint(event.pos() - child.pos())

        mimeData = QMimeData()
        mimeData.setData('application/x-dnditemdata', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - child.pos())

        tempPixmap = QPixmap(pixmap)
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        child.setPixmap(tempPixmap)
        if drag.exec_(Qt.CopyAction |
                      Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            # if drag.exec_(Qt.CopyAction | Qt.MoveAction) == Qt.MoveAction:
            child.close()
        else:
            print("mousePressEvent: drag.exec")
            child.show()
            child.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, event):
        print("Double Click")


class IconWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.icon = QLabel()
        self.text = QLabel()
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)

    def setText(self, text):
        self.text.setText(text)

    def setIcon(self, icon):
        self.icon.setPixmap(icon)

    # def move(self,)


class Window(QWidget):

    def __init__(self, path, parent=None):
        super(Window, self).__init__()
        self.pattern = "images/pattern.png"
        self.path = path
        self.widget = QWidget()
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap(self.pattern)))
        self.widget.setPalette(self.palette)
        layout = QVBoxLayout(self)
        layout.addWidget(DragWidget(path))
        self.widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)
        self.setStyleSheet("""
            QScrollBar:vertical { border:none; width:6px }
            QScrollBar::handle:vertical { background: lightgray; }
            QScrollBar::add-line:vertical { background: none; }
            QScrollBar::sub-line:vertical { background: none; }
            QScrollBar:horizontal { border:none; height:6px }
            QScrollBar::handle:horizontal { background: lightgray; }
            QScrollBar::add-line:horizontal { background: none; }
            QScrollBar::sub-line:horizontal { background: none; }
            """)
        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(scroll)
        self.setLayout(vlayout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # help(QIcon)
    window = Window('./')
    # window2 = Window('./')
    sys.exit(app.exec_())
