
from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMenuBar, QAction
import sys


class GlobalMenu(QWidget):

    new_window_signal = pyqtSignal()
    rename_signal = pyqtSignal()
    file_signal = pyqtSignal()
    drawer_signal = pyqtSignal()
    clean_up_signal = pyqtSignal()
    delete_signal = pyqtSignal()
    trash_action_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(GlobalMenu, self).__init__(parent)
        self.menubar = QMenuBar()
        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        
        about_action = QAction('About', self)
        preferences_action = QAction('Preferences', self)
        preferences_action.setShortcut('Ctrl+Shift+P')
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')

        file_action = QAction('Create file', self)
        file_action.setShortcut('Ctrl+Shift+N')
        drawer_action = QAction('Create drawer', self)
        drawer_action.setShortcut('Ctrl+N')
        requester_action = QAction('Requester', self)
        requester_action.setShortcut('Ctrl+O')
        parent_action = QAction('Open Parent', self)
        parent_action.setShortcut('Ctrl+P')
        info_action = QAction('Get info', self)
        info_action.setShortcut('Ctrl+I')

        rename_action = QAction('Rename', self)
        rename_action.setShortcut('Ctrl+R')
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        clean_action = QAction('Clean Up', self)
        clean_action.setShortcut('Ctrl+;')
        delete_action = QAction('Move to Trash', self)
        delete_action.setShortcut('Ctrl+Backspace')
        trash_action = QAction('Empty trash', self)
        trash_action.setShortcut('Ctrl+Shift+Backspace')

        preferences_action.triggered.connect(self.preferences_action)
        quit_action.triggered.connect(self.quit_action)
        requester_action.triggered.connect(self.requester_action)
        parent_action.triggered.connect(self.parent_action)
        file_action.triggered.connect(self.file_action)
        drawer_action.triggered.connect(self.drawer_action)
        rename_action.triggered.connect(self.rename_action)
        clean_action.triggered.connect(self.clean_action)
        delete_action.triggered.connect(self.delete_action)
        trash_action.triggered.connect(self.trash_action)
        
        file_menu.addAction(requester_action)
        file_menu.addAction(parent_action)
        file_menu.addAction(info_action)
        file_menu.addAction(about_action)
        file_menu.addAction(quit_action)
        edit_menu.addAction(preferences_action)
        edit_menu.addAction(file_action)
        edit_menu.addAction(drawer_action)
        edit_menu.addAction(rename_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(clean_action)
        edit_menu.addAction(delete_action)
        edit_menu.addAction(trash_action)

    def quit_action(self):
        print("quit action menu")
        sys.exit(0)

    def preferences_action(self):
        print("preference action menu")
        QProcess.startDetached("./prefs.py")

    def requester_action(self):
        print("requester action menu")
        QProcess.startDetached("./requester.py")

    def parent_action(self):
        print("parent action menu")
        self.new_window_signal.emit()

    def file_action(self):
        print("file action menu")
        self.file_signal.emit()        

    def drawer_action(self):
        print("drawer action menu")
        self.drawer_signal.emit()   

    def rename_action(self):
        print("rename action menu")
        self.rename_signal.emit()

    def clean_action(self):
        print("clean up menu")
        self.clean_up_signal.emit()

    def delete_action(self):
        print("delete action menu")
        self.delete_signal.emit()

    def trash_action(self):
        print("empty trash action menu")
        self.empty_trash_action.signal.emit()
