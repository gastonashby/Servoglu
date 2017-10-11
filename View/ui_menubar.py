__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtGui,QtCore,QtWidgets
from Controller.main_controller import *


class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.controller = Controller(self)
        self.exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), 'E&xit', self)
        self.export_action = QtGui.QAction(QtGui.QIcon('save.png'), '&Export results to PDF', self)
        self.open_action = QtGui.QAction(QtGui.QIcon('open.png'), '&Open model...', self)



        #self.changeModelLanguage_action = QtGui.QAction(QtGui.QIcon('changeModelLanguage.png'), '&Change Model Language', self)
        #self.changeSystemLanguage_action = QtGui.QAction(QtGui.QIcon('changeSystemLanguage.png'), '&Change System Language', self)


    def setupUi(self, Ui_Menubar):
        self.ui_menubar = QtWidgets.QMenuBar()
        #
        # file menu actions:
        # add file menu and file menu actions
        self.file_menu = self.ui_menubar.addMenu('&File')
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addAction(self.exit_action)

        # language menu

        self.language_menu = self.ui_menubar.addMenu('&Languages')

        self.changeLanguageModel = QtWidgets.QMenu("Change Model Language", parent=self)
        self.changeLanguageSystem = QtWidgets.QMenu("Change System Language", parent=self)

        self.language_menu.addMenu(self.changeLanguageModel)
        self.language_menu.addMenu(self.changeLanguageSystem)

        self.changeLanguageModel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.changeLanguageSystem.setLayoutDirection(QtCore.Qt.LeftToRight)

        actions = {}

        d = self.controller.languageSupport.obtainPossibleLanguages()
        x=0
        for lang in d:
            # a sub-menu
            action = QtGui.QAction(QtGui.QIcon('changeSystemLanguage.png'), lang, self)
            # some dummy actions
            self.changeLanguageSystem.addAction(action)
            # keep reference
            actions[(x)] = action
            x += 1


