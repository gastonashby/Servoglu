__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules


# import 3rd party libraries
from PyQt5 import QtGui, QtCore
import numpy

# import local python
from ui_main_window import Ui_MainWindow
from ui_dock_widget import Ui_ControlsBoxDockWidget
from PyQt5.QtWidgets import QFileDialog
import Plot2 as plt2
import EdfWriter as edf

import types

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('SERVOGLU')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)

        # EXIT ACTION
        self.ui.ui_menubar.exit_action.triggered.connect(self.close)

        # EXPORT TO EDF
        self.ui.ui_menubar.export_action.triggered.connect(self.exportToEDF)

        self.dck_widget = Ui_ControlsBoxDockWidget()
        self.dck_widget.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dck_widget.ui_controls_box_widget)

        # DATA
        self.all_data = []
        self.all_curves = []
        self.indexGr = 1

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

        i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:
                # sliderF = """def sliderValueChanged""" + str(i) + """(self, value):\n\tprint(value/100)\n\n"""
                sliderF = "def sliderValueChanged" + str(i) + "(self, int_value):\n\t#print(int_value / 100)\n\t" \
                    "plt2." + userDef.name + " = int_value / 100\n\tself.dck_widget.label[" + str(i - 1) + "]" \
                    ".setText('" + userDef.description + " ' + str(eval('plt2." + userDef.name + "')) + ' " + userDef.unit + "')\n\t" \
                    "plt2.recalculate(self.indexGr)\n"

                _s_f_aux = "sliderValueChanged" + str(i)
                # print(sliderF)
                exec(sliderF)
                exec("self." + _s_f_aux + " = types.MethodType(" + _s_f_aux + ", self)")

                _s_f_aux = "self.sliderValueChanged" + str(i)

                # print(sliderF)
                # print(_s_f_aux)
                # exec(sliderF)

                self.dck_widget.slider[i-1].valueChanged.connect(eval(_s_f_aux))
                i += 1



    def definite_graph(self):
        _i = 0
        _dats = plt2.obtener(0)
        self.mayor = _dats[0]
        self.menor = _dats[0]
        for eq in plt2._e:
            # print(eq.simulate)
            if eq.simulate:
                self.all_data.append([plt2.obtener(0)[_i]])
                self.all_curves.append(self.ui.ui_sinc_plot.plot(plt2._xdata, pen=(255, 255, 255)))

                if _dats[_i] > self.mayor:
                    self.mayor = _dats[_i]

                if _dats[_i] < self.menor:
                    self.menor = _dats[_i]

            _i += 1

        self.ui.ui_sinc_plot.setYRange(self.menor - 10 , self.mayor + 10)

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
        #plt2.recalculate(0)

        _dats = plt2.obtener(0)
        _i = 0
        _j = 0
        for eq in plt2._e:
            if eq.simulate:
                #print(_dats)
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

                if _dats[_j] > self.mayor:
                    self.mayor = _dats[_j]

                if _dats[_j] < self.menor:
                    self.menor = _dats[_j]

                _i += 1
            _j += 1
        self.indexGr += 1

        #if self.indexGr % 5 == 0:
        self.ui.ui_sinc_plot.setXRange(self.indexGr - 80, self.indexGr + 20)
        self.ui.ui_sinc_plot.setYRange(self.menor - 10, self.mayor + 10)

    def exportToEDF(self):

        # file_dialog = QFileDialog(self)
        #
        # # the name filters must be a list
        # file_dialog.setNameFilters(["EDF file (*.edf)"])
        # file_dialog.selectNameFilter("EDF file (*.edf)")
        #
        # file_dialog.setAcceptMode(1)
        # # # show the dialog
        # file_dialog.exec_()
        myFilter = ["EDF file (*.edf)"]
        name, _ = QFileDialog.getSaveFileName(self, 'Save EDF as',"","EDF file (*.edf)", options=QFileDialog.DontUseNativeDialog)
        if name != "":
            if not name.endswith(".edf"):
                name = name + ".edf"
            edf.WriteEDF(plt2._y[:self.indexGr,:],plt2._e,1/60,name)


        #file = open(name, 'w')
        #text = self.textEdit.toPlainText()
        #file.write(text)
        #file.close()



