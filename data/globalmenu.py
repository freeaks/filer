
from PyQt5.QtCore import QProcess, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMenuBar, QAction
import sys


class GlobalMenu(QWidget):

    new_window_signal = pyqtSignal()
    clean_up_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(GlobalMenu, self).__init__(parent)
        self.menubar = QMenuBar()
        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        
        about_action = QAction('About', self)
        preferences_action = QAction('Preferences', self)
        quit_action = QAction('Quit', self)

        create_file_action = QAction('Create file', self)
        create_drawer_action = QAction('Create drawer', self)
        requester_action = QAction('Requester', self)
        requester_action.setShortcut('Ctrl+O')
        parent_action = QAction('Open Parent', self)
        parent_action.setShortcut('Ctrl+P')
        info_action = QAction('Get info', self)
        info_action.setShortcut('Ctrl+I')

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        clean_action = QAction('Clean Up', self)
        clean_action.setShortcut('Ctrl+;')
        delete_action = QAction('Delete', self)

        preferences_action.triggered.connect(self.preferences_action)
        quit_action.triggered.connect(self.quit_action)
        requester_action.triggered.connect(self.requester_action)
        parent_action.triggered.connect(self.parent_action)
        clean_action.triggered.connect(self.clean_action)
        
        file_menu.addAction(requester_action)
        # file_menu.addAction(open_drawer_action)
        file_menu.addAction(parent_action)
        file_menu.addAction(info_action)
        file_menu.addAction(about_action)
        file_menu.addAction(quit_action)
        edit_menu.addAction(preferences_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(clean_action)
        edit_menu.addAction(delete_action)

    def quit_action(self):
        print("quiting")
        sys.exit(0)

    def preferences_action(self):
        print("calling prefs")
        # subprocess.Popen("./prefs.py")
        QProcess.startDetached("./prefs.py")

    def requester_action(self):
        print("calling requester")
        QProcess.startDetached("./requester.py")

    def parent_action(self):
        self.new_window_signal.emit()
        # print("wp=", Window.pa)
        
    def clean_action(self):
        print("clean up")
        self.clean_up_signal.emit()
