from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt5.QtWidgets import QWidget, QRubberBand
# from PyQt5.QtGui import QRubberBand
from iconwidget import IconWidget
import os
import shutil

# color
# -----------
RED = '\033[91m'
GRE = '\033[92m'
BLU = '\033[94m'
END = '\033[0m'
# -----------


class DragWidget(QWidget):
    spacerX = 16
    spacerY = 16
    clipicon = None
    new_window_signal = pyqtSignal(str)
    query = pyqtSignal()
    src_dragwidget = None
    src_selected = []

    def __init__(self, path, parent=None):
        super(DragWidget, self).__init__(parent)
        self.setMinimumSize(400, 200)
        self.setAcceptDrops(True)
        self.parent = parent
        # self.parent.menu.connect(self.delete_icon)
        self.modifier = False
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.path = path
        self.icons = []
        # self.clipicon = None
        # self.moving_icons = []
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

        icon_list = []
        
        if len(DragWidget.src_selected) > 0:
            print("equality here too=", GRE, self is DragWidget.src_dragwidget, END)
            for item in DragWidget.src_selected:
                icon_list.append(item)
        else:
            icon_list.append(event.source())

        for item in icon_list:

            src_path = item.path
            dst_path = self.path

            if event.mimeData().hasFormat("application/x-icon"):
                # name = event.source().name
                # drawer = event.source().drawer
                name = item.name
                drawer = item.drawer
                
                print("loop item.name=[", RED, name, END, "]\n",
                      "drawer=[", RED, drawer, END, "]\n",
                      "src_path=[", RED, src_path + "/" + name, END, "]\n",
                      "dst_path=[", RED, dst_path + "/", END, "]\n",
                      "icon_list=[", RED, len(icon_list), END, "]\n",
                      "---------------")

                if src_path is not dst_path:
                    src_path += "/" + name
                    dst_path += "/"
                    # print("src=", src_path, "dst=", dst_path)
                    # self.move_icon(src_path, dst_path)
                if drawer:
                    icon_widget = IconWidget(self, name=name, path=self.path, dir=True)
                else: 
                    icon_widget = IconWidget(self, name=name, path=self.path, dir=False)
                icon_widget.new_window.connect(self.new_window_signal.emit)
                self.icons.append(icon_widget)
                self.icons[-1].move(event.pos().x(), event.pos().y())
                self.icons[-1].show()
        # self.remove_old()
        # self.updateScrollArea()
        # self.clean_up()

    def clear_dnd(self):
        DragWidget.src_dragwidget = None
        DragWidget.src_selected.clear()

    def get_modifier(self):
        return self.parent.modifier

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            for item in self.icons:
                item.icon.deselect_icon()
            self.clear_dnd() 
            
            self.origin = event.pos()
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QRect(self.origin, event.pos()).normalized())
        # QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        # print("len1=", len(self.icons))
        DragWidget.src_selected.clear()
        selected = []
        if self.rubberband.isVisible():
            self.rubberband.hide()
            
            rect = self.rubberband.geometry()
            for child in self.findChildren(IconWidget):
                if rect.intersects(child.geometry()):
                    # selected.append(child)
                    child.icon.select_icon()
                    DragWidget.src_selected.append(child)
                    if DragWidget.src_dragwidget is not self:
                        print("\n", GRE, "(dw: mouse release rubber) saving the wg", END, "\n")
                        DragWidget.src_dragwidget = self

    def mouseDoubleClickEvent(self, event):
        print(BLU, "Double Click", END) 
        self.query.emit()

    def clean_up(self):
        # print("clean_up method")
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

    def move_icon(self, source, dest):
        try:
            shutil.move(source, dest)
        except Exception as err:
            print(err)

    def copy_icon(self, source, dest):
        pass

    def delete_icon(self):
        dest = os.path.expanduser("~") + "/.Trash/"
        # print(dest)
        counter = 0
        for item in self.icons:
            if item.icon.selected:
                source = item.path + "/" + item.name
                # print("move=", source, "to=", dest)
                # counter += 1
                if source is not "":
                    try:
                        self.icons.remove(item)
                        item.deleteLater()
                        shutil.move(source, dest)
                    except Exception as err:
                        print(err)
        # print("icons selected=", counter)

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
