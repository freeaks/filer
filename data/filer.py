#!/usr/bin/env python3

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import(
    QApplication, QVBoxLayout, QScrollArea, QWidget)
from dragwidget import DragWidget
import sys
import os
import configparser
from globalmenu import GlobalMenu


class Window(QWidget):

    child_windows = []
    pattern = None
    menu = None

    def __init__(self, path, parent=None):
        super(Window, self).__init__()
        self.config = configparser.ConfigParser()
        self.config.read('prefs.cfg')
        if Window.menu is None:
            Window.menu = GlobalMenu()
        self.setWindowTitle(path)
        Window.pattern = self.config.get("background", "file")
        self.path = path
        self.widget = QWidget()
        self.palette = QPalette()
        self.palette.setBrush(
            QPalette.Background, QBrush(QPixmap(self.pattern)))
        self.widget.setPalette(self.palette)
        layout = QVBoxLayout(self)
        self._drag_widget = DragWidget(path)
        self._drag_widget.windowclass_signal.connect(self.on_make_new_window)
        self._drag_widget.query.connect(self.on_query)
        layout.addWidget(self._drag_widget)
        self.widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)
        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(scroll)
        self.setLayout(vlayout)
        self.show()

    def closeEvent(self, event):
        for item in Window.child_windows:
            if item.windowTitle() == self.windowTitle():
                Window.child_windows.remove(item)
                item.deleteLater()

    def on_make_new_window(self, path):
        Window.child_windows.append(Window(os.path.realpath(path)))

    def on_query(self):
        # get info when doubleclicking on nothing in a window
        print("got query=", self.windowTitle(),
              "obj=", self, "type=", type(self),
              "len child_windows=", len(Window.child_windows))

        for item in Window.child_windows:
            print("loop child_window=", type(
                item), "title=", item.windowTitle())


def main():
    app = QApplication(sys.argv)
    window = Window(os.path.abspath(os.path.expanduser("~")))
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
