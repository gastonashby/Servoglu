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

        area = DockArea()
        ds = Dock("Simulation", closable=False)
        dt = Dock("Treatment", closable=False)
        area.addDock(ds, 'top')
        area.addDock(dt, 'bottom')

        self.ui_sinc_plot = []
        self.ui_treat_plot = []
        self.ui_menubar = []
        self.init_singlegraph(ds, dt)
        # self.init_multigraph(ds, dt)

        MainWindow.setCentralWidget(area)

    def addItem(self, i, item):
        if i is None:
            self.ui_sinc_plot.addItem(item)
        else:
            self.ui_sinc_plot[i].addItem(item)


    def removeItem(self, i, item):
        if i is None:
            self.ui_sinc_plot.removeItem(item)
        else:
            self.ui_sinc_plot[i].removeItem(item)

    def init_multigraph(self, ds, dt):
        for i in range(0, 4):
            self.ui_sinc_plot.append(self.ui_window.addPlot())
            self.ui_sinc_plot[i].showGrid(x=True, y=True, alpha=1)
            self.ui_sinc_plot[i].setLabel('bottom', 'Time', units="")
            self.ui_sinc_plot[i].setXRange(0, 8)

            self.ui_treat_plot.append(self.ui_window_treat.addPlot())
            self.ui_treat_plot[i].showGrid(x=True, y=True, alpha=1)
            self.ui_treat_plot[i].setLabel('bottom', 'Time', units="")
            self.ui_treat_plot[i].setXLink(self.ui_sinc_plot[i])

        ds.addWidget(self.ui_window)
        dt.addWidget(self.ui_window_treat)
        self.ui_treat_plot[i-1].setXLink(self.ui_sinc_plot[i])
        # TODO : Linkear los ejes X

    def init_singlegraph(self, ds, dt):
        self.ui_sinc_plot = self.ui_window.addPlot()
        self.ui_sinc_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_sinc_plot.setLabel('bottom', '<h3 style="color: black; width: 500px">Time<h3/>', units="")
        self.ui_sinc_plot.setXRange(0, 8)

        self.ui_treat_plot = self.ui_window_treat.addPlot()
        self.ui_treat_plot.showGrid(x=True, y=True, alpha=1)
        self.ui_treat_plot.setLabel('bottom', '<h3 style="color: black">Time<h3/>', units="")
        self.ui_treat_plot.setXLink(self.ui_sinc_plot)

        ds.addWidget(self.ui_window)
        dt.addWidget(self.ui_window_treat)

    def setTitleSim(self, i, title):
        if i is None:
            self.ui_sinc_plot.setTitle('<br/><h2 style="color: black">' + title +  '<h2/>')
        else:
            self.ui_sinc_plot[i].setTitle('<br/><h2 style="color: black">' + title +  '<h2/>')

    def setLabelSim(self, i, label):
        if i is None:
            self.ui_sinc_plot.setLabel('bottom', '<h3 style="color: blackk; width: 500px">Time (' + label + ')<h3/>', units="")
        else:
            self.ui_sinc_plot[i].setLabel('bottom', '<h3 style="color: black">Time (' + label + ')<h3/>', units="")

    def setLabelTr(self, i, label):
        if i is None:
            self.ui_treat_plot.setLabel('bottom', '<h3 style="color: black">Time (' + label + ')<h3/>', units="")
        else:
            self.ui_treat_plot[i].setLabel('bottom', '<h3 style="color: black">Time (' + label + ')<h3/>', units="")

    def setTitleTr(self, i, title):
        if i is None:
            self.ui_treat_plot.setTitle('<h2 style="color: black">' + title +  '<h2/>')
        else:
            self.ui_treat_plot[i].setTitle('<h2 style="color: black">' + title +  '<h2/>')
