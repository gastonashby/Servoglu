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
        #
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #
        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)
        self.ui.ui_menubar.exit_action.triggered.connect(self.close)
        #
        self.dck_widget = Ui_ControlsBoxDockWidget()
        self.dck_widget.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dck_widget.ui_controls_box_widget)
        #
        # DATA
        # initialize the time axis (this will not change)
        self.t = numpy.linspace(0, 1000, 10000)
        # a will change the coda of the sinc function
        #self.a = 1

        self.all_data = []
        self.all_curves = []
        self.indexGr = 1

        #
        # CONTROLS
        # first set the default value to a
        # TODO: self.dck_widget.slider.setValue(self.a)
        # when the slider is changed, it emits a signal and sends an integer value
        # we send that value to a method called slider value changed that updates the value a
        self.dck_widget.slider[0].valueChanged.connect(self.sliderValueChanged1)
        self.dck_widget.slider[1].valueChanged.connect(self.sliderValueChanged2)
        self.dck_widget.slider[2].valueChanged.connect(self.sliderValueChanged3)
        self.dck_widget.slider[3].valueChanged.connect(self.sliderValueChanged4)
        self.dck_widget.btnPlayStop.clicked.connect(self.play_stop)
        self.dck_widget.btnNext.clicked.connect(self.next_frame)
        self.dck_widget.btnReset.clicked.connect(self.restart_graph)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update1)

        # finally draw the curve
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

    def sliderValueChanged1(self, int_value):
        print(int_value/100)
        plt2.z = int_value / 100
        self.dck_widget.label[0].setText("Intravenous Glucose: " + str(float(plt2.z)) + " mmol/kg/min")
        plt2.recalculate(self.indexGr)

    def sliderValueChanged2(self, int_value):
        print(int_value/100)
        plt2.Ex = int_value / 100
        self.dck_widget.label[1].setText("Exogenous insulin appearance rate: " + str(float(plt2.Ex)) + " mU/min")
        plt2.recalculate(self.indexGr)

    def sliderValueChanged3(self, int_value):
        print(int_value/100)
        plt2.ecf = int_value / 100
        self.dck_widget.label[2].setText("Enteral carbohydrate feedrate: " + str(float(plt2.ecf)) + " mmol/kg min")
        plt2.recalculate(self.indexGr)

    def sliderValueChanged4(self, int_value):
        print(int_value / 100)
        plt2.s = int_value / 100
        self.dck_widget.label[3].setText("Insulin sensitiviy: " + str(float(plt2.s)) + " {1 normal}")
        plt2.recalculate(self.indexGr)


    def play_stop(self):
        if self.dck_widget.btnPlayStop.text() == "Play":
            self.timer.start(20)
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
