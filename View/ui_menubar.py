__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtGui,QtCore,QtWidgets
from Controller.main_controller import *
import sys, os, subprocess
import time



class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self,MainWindow, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.parent = MainWindow

    def setupUi(self):
        self.ui_menubar = QtWidgets.QMenuBar()
        #
        # file menu actions:
        # add file menu and file menu actions


        self.languageHash = self.parent.controller.languageSupport.languageHash
        self.exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), self.languageHash.__getitem__("lbl.Exit"), self)
        self.export_action = QtGui.QAction(QtGui.QIcon('save.png'),
                                           self.languageHash.__getitem__("lbl.ExportResultsToPDF"), self)
        self.open_action = QtGui.QAction(QtGui.QIcon('open.png'), self.languageHash.__getitem__("lbl.OpenModel"), self)

        self.file_menu = self.ui_menubar.addMenu(self.languageHash.__getitem__("lbl.File"))
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addAction(self.exit_action)

        # language menu

        self.language_menu = self.ui_menubar.addMenu(self.languageHash.__getitem__("lbl.Languages"))

        self.changeLanguageModel = QtWidgets.QMenu(self.languageHash.__getitem__("lbl.ChangeModelLanguage"), parent=self)
        self.changeLanguageSystem = QtWidgets.QMenu(self.languageHash.__getitem__("lbl.ChangeSystemLanguage"), parent=self)

        self.language_menu.addMenu(self.changeLanguageModel)
        self.changeLanguageModel.setEnabled(False)
        self.language_menu.addMenu(self.changeLanguageSystem)

        self.changeLanguageModel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.changeLanguageSystem.setLayoutDirection(QtCore.Qt.LeftToRight)

        # load system languages
        self.systemLanguageActions = {}
        d = self.parent.controller.languageSupport.obtainPossibleLanguages()
        self.systemPossibleLanguages = d
        x=0
        for lang in d:
            # a sub-menu
            action = QtGui.QAction(QtGui.QIcon('changeSystemLanguage.png'), lang, self)
            self.changeLanguageSystem.addAction(action)
            # keep reference
            action.triggered.connect(lambda checked, lang=lang: self.changeSystemLanguage(lang))
            x += 1

    def changeSystemLanguage(self,lang):
        box = QtGui.QMessageBox()
        box.setIcon(QtGui.QMessageBox.Question)
        box.setWindowTitle(self.languageHash.__getitem__("lbl.Restart?"))
        box.setText(self.languageHash.__getitem__("lbl.Restart"))
        box.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        buttonY = box.button(QtGui.QMessageBox.Yes)
        buttonY.setText(self.languageHash.__getitem__("lbl.Yes"))
        buttonN = box.button(QtGui.QMessageBox.No)
        buttonN.setText(self.languageHash.__getitem__("lbl.No"))
        choice = box.exec_()
        # choice = QtGui.QMessageBox.question(self,self.languageHash.__getitem__("lbl.Restart?"),self.languageHash.__getitem__("lbl.Restart"),
        #                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            FILEPATH = os.path.abspath("servoglu.py")
            try:
                # QtCore.QCoreApplication.instance().quit()
                #print(sys.executable)
                #exitSignal = os.spawnv(os.P_OVERLAY, sys.executable, [lang])
                #print(exitSignal)
                print(sys.executable, FILEPATH, lang)
                subprocess.Popen([sys.executable, FILEPATH, lang])

            except Exception as e:
                print('ERROR: could not restart aplication:')
                print('  %s' % str(e))
            finally:
                QtCore.QCoreApplication.instance().quit()
                sys.exit(99)


    def setPossibleModelLanguages(self):
        # load model languages
        self.changeLanguageModel.clear()
        self.modelLanguageActions = {}
        d = self.parent.controller.model.languages
        self.modelPossibleLanguages = d
        x = 0
        for lang in d:
            # a sub-menu
            action = QtGui.QAction(QtGui.QIcon('changeModelLanguage.png'), lang, self)
            # some dummy actions
            self.changeLanguageModel.addAction(action)
            # keep reference
            # action.triggered.connect(self.changeSystemLanguage)
            action.triggered.connect(lambda checked, lang=lang: self.changeModelLanguage(lang))
            # self.systemLanguageActions[(x)] = (action,lang)
            x += 1

    def changeModelLanguage(self, lang):
        box = QtGui.QMessageBox()
        box.setIcon(QtGui.QMessageBox.Question)
        box.setWindowTitle(self.languageHash.__getitem__("lbl.Restart?"))
        box.setText(self.languageHash.__getitem__("lbl.RestartSimulation"))
        box.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        buttonY = box.button(QtGui.QMessageBox.Yes)
        buttonY.setText(self.languageHash.__getitem__("lbl.Yes"))
        buttonN = box.button(QtGui.QMessageBox.No)
        buttonN.setText(self.languageHash.__getitem__("lbl.No"))
        choice = box.exec_()
        # choice = QtGui.QMessageBox.question(self, self.languageHash.__getitem__("lbl.Restart?"),
        #                                     self.languageHash.__getitem__("lbl.RestartSimulation"),
        #                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            try:
                #self.parent.controller = Controller(self.mainWindow)
                self.parent.controller.handler_change_language_model(lang)
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

