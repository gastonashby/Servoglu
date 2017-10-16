__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtGui,QtCore,QtWidgets
from Controller.main_controller import *
import sys, os, subprocess

class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.controller = Controller(self)
        self.exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), 'E&xit', self)
        self.export_action = QtGui.QAction(QtGui.QIcon('save.png'), '&Export results to PDF', self)
        self.open_action = QtGui.QAction(QtGui.QIcon('open.png'), '&Open model...', self)

    def setupUi(self, Ui_Menubar):
        self.ui_menubar = QtWidgets.QMenuBar()
        #
        # file menu actions:
        # add file menu and file menu actions

        self.file_menu = self.ui_menubar.addMenu(self.controller.languageSupport.languageHash.__getitem__("lbl.File"))
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

        self.systemLanguageActions = {}

        d = self.controller.languageSupport.obtainPossibleLanguages()
        self.systemPossibleLanguages = d
        x=0
        for lang in d:
            # a sub-menu
            action = QtGui.QAction(QtGui.QIcon('changeSystemLanguage.png'), lang, self)
            # some dummy actions
            self.changeLanguageSystem.addAction(action)
            # keep reference
            #action.triggered.connect(self.changeSystemLanguage)
            action.triggered.connect(lambda checked, lang=lang: self.changeSystemLanguage(lang))
            #self.systemLanguageActions[(x)] = (action,lang)
            x += 1

    def changeSystemLanguage(self,lang):
        FILEPATH = 'C:\\Users\\GameGear\\PycharmProjects\\Servoglu\\main.py'#os.path.abspath(__file__)
        self.controller.languageSupport.changeLanguage("ES")
        try:
            self.__init__(self)
            self.update()
            self.repaint()
            #QtGui.qApp.quit(123)
            #QtCore.QCoreApplication.instance().quit()
            #sys.exit(123)
        except Exception as e:
            print('ERROR: could not restart aplication:')
            print('  %s' % str(e))
        # try:
        #     subprocess.Popen([sys.executable, FILEPATH])
        # except Exception as e:
        #     print('ERROR: could not restart aplication:')
        #     print('  %s' % str(e))
        # else:
        #     QtGui.qApp.quit()

