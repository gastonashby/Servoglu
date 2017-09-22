__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtGui


class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), 'E&xit', self)
        self.export_action = QtGui.QAction(QtGui.QIcon('save.png'), '&Export to EDF', self)
        self.open_action = QtGui.QAction(QtGui.QIcon('open.png'), '&Open model...', self)

    def setupUi(self, Ui_Menubar):
        self.ui_menubar = QtGui.QMenuBar()
        #
        # file menu actions:
        # add file menu and file menu actions
        self.file_menu = self.ui_menubar.addMenu('&File')

        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addAction(self.exit_action)
