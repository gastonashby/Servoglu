__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules


# import 3rd party libraries
from PyQt5 import QtGui, QtCore
import numpy

# import local python
from ui_main_window import Ui_MainWindow
from ui_dock_widget import Ui_ControlsBoxDockWidget
import Plot2 as plt2


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('SERVOGLU')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)
        self.ui.ui_menubar.exit_action.triggered.connect(self.close)

        self.dck_widget = Ui_ControlsBoxDockWidget()
        self.dck_widget.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dck_widget.ui_controls_box_widget)

        # DATA
        self.all_data = []
        self.all_curves = []
        #self.indexGr = 1

        # CONTROLS
        self.dck_widget.btnPlayStop.clicked.connect(self.play_stop)
        self.dck_widget.btnNext.clicked.connect(self.next_frame)
        self.dck_widget.btnReset.clicked.connect(self.restart_graph)

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update1)



        # GRAPH
        self.definite_graph()
        self.restart_graph()




    def definite_graph(self):
        _i = 0
        for eq in plt2._e:
            # print(eq.simulate)
            if eq.simulate:
                self.all_data.append([plt2.obtener(0)[_i]])
                self.all_curves.append(self.ui.ui_sinc_plot.plot(plt2._xdata, pen=(255, 255, 255)))
            _i += 1

    def play_stop(self):
        if self.dck_widget.btnPlayStop.text() == "Play":
            self.timer.start(50)
            self.dck_widget.btnPlayStop.setText("Stop")
            self.dck_widget.btnNext.setEnabled(False)
        else:
            self.timer.stop()
            self.dck_widget.btnPlayStop.setText("Play")
            self.dck_widget.btnNext.setEnabled(True)

    def next_frame(self):
        self.update1()

    def restart_graph(self):
        self.indexGr = 0

        # TODO: falta restaurar los valores iniciales del XML
        # plt2.restart()

        _dats = plt2.obtener(0)
        _i = 0
        _j = 0
        for eq in plt2._e:
            if eq.simulate:
                # print(dats[_j])
                self.all_data[_i] = [_dats[_j]]
                self.all_curves[_i].setData(self.all_data[_i])
                _i += 1
            _j += 1
        self.timer.stop()
        self.dck_widget.btnPlayStop.setText("Play")
        self.dck_widget.btnNext.setEnabled(True)

    def update1(self):
        _dats = plt2.obtener(self.indexGr)
        #print(_dats)
        _i = 0
        _j = 0
        for eq in plt2._e:
            if eq.simulate:
                #print(dats[_j])
                self.all_data[_i].append(_dats[_j])
                self.all_curves[_i].setData(self.all_data[_i])
                _i += 1
            _j += 1
        self.indexGr += 1
        self.ui.ui_sinc_plot.setXRange(self.indexGr - 80, self.indexGr + 20)
