__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox
from PyQt5.QtGui import QFont

from Controller.main_controller import *

def main():

    try:
        app = QApplication(sys.argv)
        app.setApplicationName('SERVOGLU')
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        myFont = QFont()
        myFont.setBold(False)
        myFont.setPointSize(10)
        QApplication.setFont(myFont)
        controller = Controller()
        controller.window.resize(1000, 500)
        controller.window.showMaximized()
        currentExitCode = app.exec_()
    except Exception as e:
        print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == '__main__':
    main()

