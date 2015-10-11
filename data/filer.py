#!/usr/bin/env python3

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import(
    QApplication, QVBoxLayout, QScrollArea, QWidget)
from dragwidget import DragWidget
import sys
import os
import configparser
import argparse
from globalmenu import GlobalMenu


class Window(QWidget):

    child_windows = []
    pattern = None
    menu = None
    modifier = False

    def __init__(self, path, parent=None):
        super(Window, self).__init__()
        self.config = configparser.ConfigParser()
        self.config.read('prefs.cfg')
        if Window.menu is None:
            Window.menu = GlobalMenu()
        Window.menu.new_window_signal.connect(self.on_parent_window)
        Window.menu.clean_up_signal.connect(self.on_clean_up)
        self.setWindowTitle(path)
        Window.pattern = self.config.get("background", "file")
        self.path = path
        self.widget = QWidget()
        self.palette = QPalette()
        self.palette.setBrush(
            QPalette.Background, QBrush(QPixmap(self.pattern)))
        self.widget.setPalette(self.palette)
        layout = QVBoxLayout(self)
        self._drag_widget = DragWidget(path, parent=self)
        self._drag_widget.new_window_signal.connect(self.on_new_window)
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
        Window.child_windows.append(self)
        self.show()

    def closeEvent(self, event):
        for item in Window.child_windows:
            if item.windowTitle() == self.windowTitle():
                Window.child_windows.remove(item)
                item.deleteLater()

    def window_exists(self, path=None):
        for item in Window.child_windows:
            if item.path == path:
                print("exist=", path)
                item.raise_()
                return True
        return False

    def on_new_window(self, path):
        if self.window_exists(path):
            return
        else:
            Window(os.path.realpath(path))

    def on_parent_window(self):
        if self.isActiveWindow():
            if self.window_exists(self.path.rsplit('/', 1)[0]):
                    return
            else:
                self.on_new_window(self.path.rsplit('/', 1)[0])

    def on_clean_up(self):
        if self.isActiveWindow():
            self._drag_widget.clean_up()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            Window.modifier = True

    def keyReleaseEvent(self, event):
        if Window.modifier:
            Window.modifier = False

    def on_query(self):
        # get info when doubleclicking on nothing in a window
        print("got query=", self.windowTitle(),
              "obj=", self, "type=", type(self),
              "len child_windows=", len(Window.child_windows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="filesystem path")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    window = Window(args.path)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
