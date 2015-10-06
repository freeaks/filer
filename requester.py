#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import(
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFormLayout, QListWidget, QListWidgetItem,
    QLineEdit)


class requester(QWidget):

    def __init__(self):
        super(requester, self).__init__()
        self.path = "/"
        self.QVBoxLayout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.QVBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.QVBoxLayout.setSpacing(5)
        self.myQListWidget = QListWidget(self)
        self.create_list()

        self.ok_button = ok_button(parent=self)
        self.volumes_button = volumes_button()
        self.parent_button = parent_button()
        self.cancel_button = cancel_button()

        self.drawer_field = drawer_field()
        self.file_field = file_field()
        
        self.form_layout.addRow("Drawer", self.drawer_field)
        self.form_layout.addRow("File", self.file_field)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.volumes_button)
        self.button_layout.addWidget(self.parent_button)
        self.button_layout.addWidget(self.cancel_button)

        self.QVBoxLayout.addWidget(self.myQListWidget)
        self.QVBoxLayout.addLayout(self.form_layout)
        self.QVBoxLayout.addLayout(self.button_layout)
        self.setLayout(self.QVBoxLayout) 

    def create_list(self):
        for item in os.listdir(self.path):
            # print(item)
            if os.path.isdir(os.path.join(self.path, item)):
                self.myQCustomQWidget = QCustomQWidget(name=item, kind="directory")
            else:
                self.myQCustomQWidget = QCustomQWidget(name=item, kind="file")
            # myQListWidget = QListWidget(self)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, self.myQCustomQWidget)


class QCustomQWidget (QLabel):

    def __init__(self, name=None, kind=None, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.kind = kind
        self.text = name
        self.set_text(name)

    def set_text(self, text):
        if self.kind == "directory":
            self.setStyleSheet('''color: rgb(0, 0, 255);''')
        else:
            self.setStyleSheet('''color: rgb(0, 0, 0);''')        
        self.setText(text)


class drawer_field(QLineEdit):

    def __init__(self, name=None, kind=None, parent=None):
        super(drawer_field, self).__init__(parent)
        pass


class file_field(QLineEdit):

    def __init__(self, name=None, kind=None, parent=None):
        super(file_field, self).__init__(parent)
        pass


class ok_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(ok_button, self).__init__(parent)
        self.setText("Ok")
        self.show()


class volumes_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(volumes_button, self).__init__(parent)
        self.setText("Volumes")


class parent_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(parent_button, self).__init__(parent)
        self.setText("Parent")


class cancel_button(QPushButton):

    def __init__(self, name=None, kind=None, parent=None):
        super(cancel_button, self).__init__(parent)
        self.setText("Cancel")


if __name__ == '__main__':
    app = QApplication([])
    window = requester()
    window.show()
    sys.exit(app.exec_())
