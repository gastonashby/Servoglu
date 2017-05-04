__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules


# import 3rd party libraries
from PyQt5 import QtGui, QtCore
import pyqtgraph

# import local python
from ui_menubar import Ui_Menubar


class Ui_MainWindow(QtCore.QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.ui_central_widget = QtGui.QWidget(MainWindow)
        #
        self.ui_window = pyqtgraph.GraphicsWindow()
        self.ui_window.setBackground('k')

        # PLOT
        # TODO: Sacar el titulo del XML
        self.ui_sinc_plot = self.ui_window.addPlot(title='Glucosa')
        self.ui_sinc_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_sinc_plot.setLabel('bottom', 'Time', 'min')
        self.ui_sinc_plot.setXRange(0, 100)

        # LAYOUT
        self.ui_central_layout = QtGui.QVBoxLayout()
        self.ui_central_layout.addWidget(self.ui_window)
        self.ui_central_widget.setLayout(self.ui_central_layout)
        #
        MainWindow.setCentralWidget(self.ui_central_widget)
        #
        # MENUBAR
        self.ui_menubar = Ui_Menubar()
        self.ui_menubar.setupUi(self)