
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QWidget, QMenuBar, QAction
import sys


class GlobalMenu(QWidget):

    def __init__(self, parent=None):
        super(GlobalMenu, self).__init__(parent)
        self.menubar = QMenuBar()
        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        requester_action = QAction('Requester', self)
        # open_drawer_action = QAction('Open drawer', self)
        open_parent_action = QAction('Open parent', self)
        info_action = QAction('Get info', self)
        about_action = QAction('About', self)
        quit_action = QAction('Quit', self)
        preferences_action = QAction('Preferences', self)
        copy_action = QAction('Copy', self)
        paste_action = QAction('Paste', self)
        create_file_action = QAction('Create file', self)
        create_drawer_action = QAction('Create drawer', self)
        delete_action = QAction('Delete', self)

        requester_action.triggered.connect(self.requester_action)
        quit_action.triggered.connect(self.quit_action)
        preferences_action.triggered.connect(self.preferences_action)

        file_menu.addAction(requester_action)
        # file_menu.addAction(open_drawer_action)
        file_menu.addAction(open_parent_action)
        file_menu.addAction(info_action)
        file_menu.addAction(about_action)
        file_menu.addAction(quit_action)
        edit_menu.addAction(preferences_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(delete_action)

    def requester_action(self):
        print("calling requester")
        QProcess.startDetached("./requester.py")

    def quit_action(self):
        print("quiting")
        sys.exit(0)

    def preferences_action(self):
        print("calling prefs")
        # subprocess.Popen("./prefs.py")
        QProcess.startDetached("./prefs.py")
