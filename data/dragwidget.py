from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt5.QtWidgets import QWidget, QRubberBand, QMessageBox
# from PyQt5.QtGui import QRubberBand
from iconwidget import IconWidget
import os
import shutil

# debug color
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
        self.icon_offsetx = 0
        self.icon_offsety = 0
        # self.clipicon = None
        # self.moving_icons = []
        self.read_drawer()
        self.clean_up()
        # print(type(IconWidget.icon))
        # print(self.findChildren(ClickableIcon))

    def read_drawer(self):
        # self.icons.clear()
        for item in os.scandir(self.path):
            if item.is_dir():
                icon_widget = IconWidget(parent=self, name=item.name, path=self.path, dir=True)
            else:
                icon_widget = IconWidget(parent=self, name=item.name, path=self.path, dir=False)
            icon_widget.new_window.connect(self.new_window_signal.emit)
            icon_widget.clipboard.connect(self.on_clipboard)
            self.icons.append(icon_widget)
            self.icons[-1].setAttribute(Qt.WA_DeleteOnClose)
        # self.update()

    def updateScrollArea(self):
        """ set the dimension of the widget """
        iconx = []
        icony = []
        if len(self.icons) > 0:
            for item in self.icons:
                iconx.append(item.x())
                icony.append(item.y())
            self.setMinimumWidth(max(iconx)+75)
            self.setMinimumHeight(max(icony)+75)
        
    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def get_dnd_list(self, event):
        icon_list = []
        icon_offsetx = None
        icon_offsety = None
        if len(DragWidget.src_selected) > 0:
            for item in DragWidget.src_selected:
                icon_list.append(item)
        else:
            icon_list.append(event.source())
        return icon_list

    def create_icon(self, name, drawer):
        if drawer:
            icon_widget = IconWidget(self, name=name, path=self.path, dir=True)
        else: 
            icon_widget = IconWidget(self, name=name, path=self.path, dir=False)
        icon_widget.new_window.connect(self.new_window_signal.emit)
        self.icons.append(icon_widget)

    def place_icon(self, x, y):
        self.icons[-1].move(x, y)
        self.icons[-1].show()

    def dropEvent(self, event):
        event.accept()
        icon_list = self.get_dnd_list(event)
        icon_offsetx = event.pos().x()
        icon_offsety = event.pos().y()
        for item in icon_list:
            name = item.name
            drawer = item.drawer
            src_path = item.path + "/" + name
            dst_path = self.path + "/"
            if event.mimeData().hasFormat("application/x-icon"):
                self.create_icon(name, drawer)
                self.move_data(src_path, dst_path)
                self.place_icon(icon_offsetx, icon_offsety)
                icon_offsetx += 100 
                if icon_offsetx > self.window().width():
                    icon_offsetx = event.pos().x()
                    icon_offsety += 75

        icon_offsetx = None
        icon_offsety = None
        self.updateScrollArea()

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
        self.clear_dnd()
        if self.rubberband.isVisible():
            self.rubberband.hide()
            rect = self.rubberband.geometry()
            for child in self.findChildren(IconWidget):
                if rect.intersects(child.geometry()):
                    child.icon.select_icon()
                    DragWidget.src_selected.append(child)
                    if DragWidget.src_dragwidget is not self:
                        DragWidget.src_dragwidget = self

    def mouseDoubleClickEvent(self, event):
        print(BLU, "Double Click", END) 
        self.query.emit()

    def create_file(self):
        new_file = self.path + "/" + "newfile.txt"
        open(new_file, 'w').close()
        icon_widget = IconWidget(self, name="newfile.txt", path=self.path, dir=False)
        icon_widget.new_window.connect(self.new_window_signal.emit)
        icon_widget.show()
        self.icons.append(icon_widget)

    def create_drawer(self):
        print("creating new drawer")
        new_drawer = self.path + "/" + "NewDrawer"
        os.makedirs(new_drawer)
        icon_widget = IconWidget(self, name="NewDrawer", path=self.path, dir=True)
        icon_widget.new_window.connect(self.new_window_signal.emit)
        icon_widget.show()
        self.icons.append(icon_widget)

    def rename_file(self):
        print("renaming file")

    def clean_up(self):
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

    def move_data(self, source, dest):
        srce_path = source.rsplit('/', 1)[0]
        dest_path = dest.rsplit('/', 1)[0]
        if srce_path != dest_path:
            try:
                shutil.move(source, dest)
            except Exception as err:
                print(err)

    def copy_icon(self, source, dest):
        pass

    def delete_icon(self):
        dest = os.path.expanduser("~") + "/.Trash/"
        error_string = ""
        for item in self.icons:
            if item.icon.selected:
                source = item.path + "/" + item.name
                if source is not "":
                    try:
                        shutil.move(source, dest)
                    except Exception as err:
                        error_string += str(err) + "\n" + "\n"
                    else:
                        self.icons.remove(item)
                        item.deleteLater()
        if error_string is not "":
            QMessageBox.information(self, 'Info', error_string, QMessageBox.Ok)

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
