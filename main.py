__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules
import sys

# import 3rd party libraries
from PyQt5.QtWidgets import QApplication

# import local python
from main_window import Window


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('SERVOGLU')
    window = Window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()