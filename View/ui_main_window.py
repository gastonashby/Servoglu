__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from PyQt5 import QtGui, QtCore
from pyqtgraph.dockarea import *

class Ui_MainWindow(QtCore.QObject):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # self.ui_central_widget = QtGui.QWidget(MainWindow)

        self.ui_window = pyqtgraph.GraphicsWindow()
        self.ui_window.setBackground('w')

        self.ui_window_treat = pyqtgraph.GraphicsWindow()
        self.ui_window_treat.setBackground('w')

        self.ui_sinc_plot = self.ui_window.addPlot()
        self.ui_sinc_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_sinc_plot.setLabel('bottom', 'Time', units="")
        self.ui_sinc_plot.setXRange(-20, 10)

        self.ui_treat_plot = self.ui_window_treat.addPlot(title='Treatment')
        self.ui_treat_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_treat_plot.setLabel('bottom', 'Time', units="")
        self.ui_treat_plot.setXRange(-20, 10)
        # LAYOUT
        # self.ui_central_layout = QtGui.QVBoxLayout()
        # self.ui_central_layout.addWidget(self.ui_window)
        # self.ui_central_layout.addWidget(self.ui_window_treat)
        # self.ui_central_widget.setLayout(self.ui_central_layout)

        self.ui_treat_plot.setXLink(self.ui_sinc_plot)

        area = DockArea()
        ds = Dock("Simulation", closable=True)
        dt = Dock("Treatment", closable=True)
        area.addDock(ds, 'top')
        area.addDock(dt, 'bottom')
        ds.addWidget(self.ui_window)
        dt.addWidget(self.ui_window_treat)

        MainWindow.setCentralWidget(area)