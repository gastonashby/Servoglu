__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt5 import QtGui


# import local python

class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        self.export_action = QtGui.QAction(QtGui.QIcon('save.png'), '&Export to EDF', self)

    def setupUi(self, Ui_Menubar):
        self.ui_menubar = QtGui.QMenuBar()
        #
        # file menu actions:
        # add file menu and file menu actions
        self.file_menu = self.ui_menubar.addMenu('&File')
        self.file_menu.addAction(self.exit_action)
        self.file_menu.addAction(self.export_action)