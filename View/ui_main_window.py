__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from PyQt5 import QtGui, QtCore

from View.ui_menubar import Ui_Menubar


class Ui_MainWindow(QtCore.QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.ui_central_widget = QtGui.QWidget(MainWindow)
        #
        self.ui_window = pyqtgraph.GraphicsWindow()
        self.ui_window.setBackground('w')

        # PLOT
        # TODO: Sacar el titulo del XML y unidad
        self.ui_sinc_plot = self.ui_window.addPlot(title='Glucosa')
        self.ui_sinc_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_sinc_plot.setLabel('bottom', 'Time', units='min')
        self.ui_sinc_plot.setXRange(-20, 10)

        self.ui_treat_plot = self.ui_window.addPlot(title='Treatment')
        self.ui_treat_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_treat_plot.setLabel('bottom', 'Time', units='min')
        self.ui_treat_plot.setXRange(-20, 10)


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