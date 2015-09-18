#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from os import listdir
from os.path import isfile,isdir, join
from PyQt5.QtWidgets import QTabBar


class DragWidget(QFrame):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        #self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        boatIcon = QLabel(self)
        boatIcon.setPixmap(QPixmap('./images/closeicon.png'))
        boatIcon.move(20, 20)
        boatIcon.show()
        boatIcon.setAttribute(Qt.WA_DeleteOnClose)

        carIcon = QLabel(self)
        carIcon.setPixmap(QPixmap('./images/openicon.png'))
        carIcon.move(120, 20)
        carIcon.show()
        carIcon.setAttribute(Qt.WA_DeleteOnClose)



    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            itemData = event.mimeData().data('application/x-dnditemdata')
            dataStream = QDataStream(itemData, QIODevice.ReadOnly)

            pixmap = QPixmap()
            offset = QPoint()
            dataStream >> pixmap >> offset

            newIcon = QLabel(self)
            newIcon.setPixmap(pixmap)
            newIcon.move(event.pos() - offset)
            newIcon.show()
            newIcon.setAttribute(Qt.WA_DeleteOnClose)

            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
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

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)


#class Window(QWidget):
#    def __init__(self,val):
        # super(Window, self).__init__()
        # hbox = QHBoxLayout(self)
        # self.list_widget = QListWidget()
        # self.list_widget.addItem(QListWidgetItem(QIcon(QPixmap('./images/closeicon.png')),'your text here'))
        # self.list_widget.setIconSize(QSize(400,300)) #Set your image size
        # hbox.addWidget(self.list_widget)
        # self.setLayout(hbox)
        # self.show()
        # ------
        # QWidget.__init__(self)
        # mygroupbox = QGroupBox('this is my groupbox')
        # myform = QFormLayout()
        # labellist = []
        # combolist = []
        # for i in range(val):
        #     labellist.append(QLabel('mylabel'))
        #     combolist.append(QComboBox())
        #     myform.addRow(labellist[i],combolist[i])
        # mygroupbox.setLayout(myform)
        # scroll = QScrollArea()
        # scroll.setWidget(mygroupbox)
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        # layout = QVBoxLayout(self)
        # layout.addWidget(scroll)
        # self.show()

class Window(QWidget):
    def __init__(self, path):
        QWidget.__init__(self)
        self.path = path
        mainWidget = QWidget()
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("images/pattern.png")))
        mainWidget.setPalette(palette)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(mainWidget)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(100)
        self.setStyleSheet("""
            QScrollBar:vertical { border:none; width:6px }
            QScrollBar::handle:vertical { background: lightgray; }
            QScrollBar::add-line:vertical { background: none; }
            QScrollBar::sub-line:vertical { background: none; }
            """)

        # working:
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        myform = QHBoxLayout()
        myform.addWidget(DragWidget())
        mainWidget.setLayout(myform)
        # -------

        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                print("file = ",name)
                #DragImage('file.png',layout, path, name)
            if os.path.isdir(os.path.join(path, name)):
                print ("dire =", name)
                #DragImage('directory.png',layout, path, name)

        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    #window = Window(25)
    window = Window('./')
    window2 = Window('./')

    sys.exit(app.exec_())
