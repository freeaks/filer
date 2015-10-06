
from PyQt5.QtWidgets import QWidget, QMenuBar, QAction


class GlobalMenu(QWidget):

    def __init__(self, parent=None):
        super(GlobalMenu, self).__init__(parent)
        self.menubar = QMenuBar()
        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        open_file_action = QAction('Open file', self)
        open_drawer_action = QAction('Open drawer', self)
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

        file_menu.addAction(open_file_action)
        file_menu.addAction(open_drawer_action)
        file_menu.addAction(open_parent_action)
        file_menu.addAction(info_action)
        file_menu.addAction(about_action)
        file_menu.addAction(quit_action)
        edit_menu.addAction(preferences_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(delete_action)
        pass
