#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import(
    QApplication, QWidget, QLabel, QVBoxLayout, QAction, QToolBar, QMainWindow,
    QHBoxLayout, QFormLayout, QListWidget, QListWidgetItem, 
    QLineEdit, QAbstractItemView, QSizePolicy)


class requester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mywidget = central_widget()
        self.setCentralWidget(self.mywidget)
        
        Toolbar = QToolBar()
        Toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(Toolbar)

        parent_action = QAction(QIcon('images/toolbar/up.png'), 'Parent', self)
        home_action = QAction(QIcon('images/toolbar/home.png'), 'Home', self)
        copy_action = QAction(QIcon('images/toolbar/copy.png'), 'Copy', self)
        paste_action = QAction(QIcon('images/toolbar/paste.png'), 'Paste', self)
        cut_action = QAction(QIcon('images/toolbar/cut.png'), 'Cut', self)
        view_action = QAction(QIcon('images/toolbar/view.png'), 'View', self)
        info_action = QAction(QIcon('images/toolbar/info.png'), 'Info', self)
        setup_action = QAction(QIcon('images/toolbar/setup.png'), 'Setup', self)
        trash_action = QAction(QIcon('images/toolbar/trash.png'), 'Trash', self)
        # parent_action.setShortcut('Ctrl+Q')
        parent_action.triggered.connect(self.open_parent)
        home_action.triggered.connect(self.open_home)
        copy_action.triggered.connect(self.copy_file)
        info_action.triggered.connect(self.get_dir_size)

        Toolbar.addAction((parent_action))
        Toolbar.addAction((home_action))
        Toolbar.addAction((copy_action))
        Toolbar.addAction((paste_action))
        Toolbar.addAction((cut_action))
        Toolbar.addAction((view_action))
        Toolbar.addAction((info_action))
        Toolbar.addAction((setup_action))
        Toolbar.addAction((trash_action))

    def open_parent(self):
        self.mywidget.create_list(self.mywidget.parent_path)

    def open_home(self):
        self.mywidget.create_list("/home")

    def copy_file(self):
        print("copying:")

    def get_dir_size(self):
        self.mywidget.get_dir_size()


class central_widget(QWidget):
    def __init__(self):
        super(central_widget, self).__init__()
        self.setWindowTitle("/")
        self.current_path = "/"
        self.parent_path = "/"
        self.main_Layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.main_Layout.setContentsMargins(5, 5, 5, 5)
        self.main_Layout.setSpacing(5)
        self.myQListWidget = QListWidget(self)
        self.myQListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.myQListWidget.setSelectionMode(QAbstractItemView.MultiSelection)

        self.file_field = file_field(parent=self)

        self.form_layout.addRow(self.file_field)

        self.main_Layout.addWidget(self.myQListWidget)
        self.main_Layout.addLayout(self.form_layout)
        self.setLayout(self.main_Layout)
        self.create_list(self.current_path)

    def create_list(self, current_path):
        self.myQListWidget.clear()
        self.file_field.set_text(name=None, path=None)

        # file browsing logic
        # ----------------------
        self.parent_path = current_path.rsplit('/', 1)[0]
        if self.parent_path is "":
            self.parent_path = "/"
        if current_path is "/":
            self.current_path = current_path
            self.setWindowTitle(current_path)
        else:
            self.current_path = current_path + "/" 
            self.setWindowTitle(current_path.rsplit('/', 1)[-1])
        # -----------------------

        files = sorted(os.scandir(current_path), key=lambda e: e.is_file())
        self.items = []
        print("size of items=", len(self.items))
        for item in files:
            if item.is_dir():
                list_item = ListItem(name=item.name, drawer=True, current_path=self.current_path,
                                     parent=self)
            else:
                list_item = ListItem(name=item.name, drawer=False, current_path=self.current_path,
                                     parent=self)

            self.myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            self.myQListWidgetItem.setSizeHint(list_item.sizeHint())
            self.myQListWidget.setItemWidget(self.myQListWidgetItem, list_item)
            self.items.append(self.myQListWidgetItem)

    # def mousePressEvent(self, event):
    #     self.get_dir_size()
        # for element in self.items:
        #     if element.isSelected():
        #         print("selected element=", self.myQListWidget.itemWidget(element).xyz())
        # print("-------\n")

    def get_dir_size(self): 
        sitems = []
        for element in self.items:
            if element.isSelected():
                sitems = self.myQListWidget.itemWidget(element)
                dir_size = subprocess.check_output(["du", "-sh", self.current_path + sitems.xyz()])
                dir_str = dir_size.decode("utf-8")
                dir_str = dir_str.split('\t')[0]
                sitems.set_text(sitems.xyz(), dir_str)


class ListItem (QWidget):
    def __init__(self, name=None, drawer=None, current_path=None, parent=None):
        super(ListItem, self).__init__(parent)
        self.current_path = current_path
        self.parent = parent
        self.file_layout = QHBoxLayout()
        self.file_layout.setContentsMargins(5, 5, 5, 0)
        self.name_label = QLabel("")
        self.size_label = QLabel("")
        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.size_label.setAlignment(Qt.AlignRight)
        self.file_layout.addWidget(self.name_label)
        self.file_layout.addWidget(self.size_label)
        self.file_layout.addSpacing(5)
        self.setLayout(self.file_layout)
        self.drawer = drawer
        self.name = name
        self.set_text(name)

    def set_text(self, text, text2="Drawer"):
        if self.drawer:
            self.setStyleSheet('''color: rgb(0, 0, 255);''')
            self.size_label.setText(text2)
        else:
            self.setStyleSheet('''color: rgb(0, 0, 0);''')
            filesize = os.path.getsize(self.current_path + self.name)
            self.size_label.setText(self.GetHumanReadable(filesize))
        self.name_label.setText(self.name)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.drawer:
                self.parent.create_list(current_path=self.current_path + self.name)
            else:
                self.parent.file_field.set_text(name=self.name, path=self.current_path)
    
    def xyz(self):
        return self.name

    def GetHumanReadable(self, size, precision=2):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
            suffixIndex += 1  # increment the index of the suffix
            size = size/1024.0  # apply the division
        return "%.*f%s" % (precision, size, suffixes[suffixIndex])
                

class file_field(QLineEdit):

    def __init__(self, parent=None):
        super(file_field, self).__init__(parent)
        self.parent = parent
        # self.name = name
        self.setPlaceholderText("Path")

    def set_text(self, name=None, path=None):
        self.path = path
        self.name = name

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            entry = self.text()
            try:
                if os.path.isdir(entry):
                    self.parent.create_list(entry)
            except Exception as reason:
                print("error:", reason.args)
        else:
            super(file_field, self).keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication([])
    window = requester()
    window.show()
    sys.exit(app.exec_())
