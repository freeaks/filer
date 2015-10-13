#!/usr/bin/env python3

import sys
import os
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import(
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFormLayout, QListWidget, QListWidgetItem, 
    QLineEdit)


class requester(QWidget):

    def __init__(self):
        super(requester, self).__init__()
        self.setWindowTitle("/")
        self.current_path = "/"
        self.parent_path = "/"
        self.main_Layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.main_Layout.setContentsMargins(5, 5, 5, 5)
        self.main_Layout.setSpacing(5)
        self.myQListWidget = QListWidget(self)
        # self.myQListWidget.horizontalScrollBar().
        self.myQListWidget.setStyleSheet("""
            QListWidget:item:selected:active {
            background-color:#A6A4FF;}
            """)

        self.ok_button = ok_button(parent=self)
        self.volumes_button = volumes_button(parent=self)
        self.parent_button = parent_button(parent=self)
        self.cancel_button = cancel_button()

        self.drawer_field = drawer_field(parent=self)
        self.file_field = file_field()

        self.form_layout.addRow("Drawer", self.drawer_field)
        self.form_layout.addRow("File", self.file_field)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.volumes_button)
        self.button_layout.addWidget(self.parent_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_Layout.addWidget(self.myQListWidget)
        self.main_Layout.addLayout(self.form_layout)
        self.main_Layout.addLayout(self.button_layout)
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
        for item in files:
            if item.is_dir():
                list_item = ListItem(name=item.name, drawer=True, current_path=self.current_path,
                                     parent=self)
            else:
                list_item = ListItem(name=item.name, drawer=False, current_path=self.current_path,
                                     parent=self)

            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(list_item.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, list_item)


class ListItem (QWidget):

    def __init__(self, name=None, drawer=None, current_path=None, parent=None):
        super(ListItem, self).__init__(parent)
        self.current_path = current_path
        self.parent = parent
        self.file_layout = QHBoxLayout()
        self.file_layout.setContentsMargins(5, 5, 5, 0)
        self.name_label = QLabel("")
        self.size_label = QLabel("")
        self.size_label.setAlignment(Qt.AlignRight)
        self.file_layout.addWidget(self.name_label)
        self.file_layout.addWidget(self.size_label)
        self.file_layout.addSpacing(5)
        self.setLayout(self.file_layout)
        self.drawer = drawer
        self.name = name
        self.set_text(name)

    def set_text(self, text):
        if self.drawer:
            self.setStyleSheet('''color: rgb(0, 0, 255);''')
            self.size_label.setText("Drawer")
        else:
            self.setStyleSheet('''color: rgb(0, 0, 0);''')
        self.name_label.setText(self.name)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.drawer:
                self.parent.create_list(current_path=self.current_path + self.name)
            else:
                self.parent.file_field.set_text(name=self.name, path=self.current_path)
                

class drawer_field(QLineEdit):

    def __init__(self, name=None, kind=None, parent=None):
        super(drawer_field, self).__init__(parent)
        self.parent = parent

    def set_text(self, name=None):
        self.name = name
        self.setText(name)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            entry = self.text()
            try:
                if os.path.isdir(entry):
                    self.parent.create_list(entry)
            except Exception as reason:
                print("error:", reason.args)
        else:
            super(drawer_field, self).keyPressEvent(event)


class file_field(QLineEdit):

    def __init__(self, parent=None):
        super(file_field, self).__init__(parent)
        # self.name = name

    def set_text(self, name=None, path=None):
        self.path = path
        self.name = name
        self.setText(name)


class ok_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(ok_button, self).__init__(parent)
        self.parent = parent
        self.setText("Ok")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.parent.file_field.name:
                file = "\"" + self.parent.file_field.path
                file += "/" + self.parent.file_field.name + "\""
                print(file)
                QProcess.execute("/usr/bin/open " + file)
            else:
                path = self.parent.current_path
                print(path)
                QProcess.startDetached(
                    "/Users/freeaks/source/filer/data/filer.py -p " + path)
            sys.exit(0)


class volumes_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(volumes_button, self).__init__(parent)
        self.parent = parent
        self.setText("Volumes")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.create_list(path="/Volumes/")


class parent_button(QPushButton):

    def __init__(self, parent=None):
        super(parent_button, self).__init__(parent)
        self.parent = parent
        self.setText("Parent")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            print("parent_button=", self.parent.parent_path)
            self.parent.create_list(current_path=self.parent.parent_path)


class cancel_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(cancel_button, self).__init__(parent)
        self.setText("Cancel")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            sys.exit(0)


if __name__ == '__main__':
    app = QApplication([])
    window = requester()
    window.show()
    sys.exit(app.exec_())
