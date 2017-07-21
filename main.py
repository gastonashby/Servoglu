__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules
import sys



from PyQt5.QtWidgets import QApplication, QStyleFactory

from main_window import Window


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('SERVOGLU')
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = Window()
    window.show()
    window.showMaximized()
    app.exec_()


if __name__ == '__main__':
    main()