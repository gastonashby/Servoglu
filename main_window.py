__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtGui, QtCore
import pyqtgraph
from ui_main_window import Ui_MainWindow
from ui_dock_widget import Ui_ControlsBoxDockWidget
from ui_controls_widget import Ui_GeneralControlsWidget
from PyQt5.QtWidgets import QFileDialog
import Plot2 as plt2
import EdfWriter as edf

import types
import sys

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('SERVOGLU')
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        #TODO estilo QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)

        # EXIT ACTION
        self.ui.ui_menubar.exit_action.triggered.connect(self.close)

        # EXPORT TO EDF
        self.ui.ui_menubar.export_action.triggered.connect(self.exportToEDF)

        self.dck_widget = Ui_ControlsBoxDockWidget()
        self.dck_widget.setupUi(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dck_widget.ui_controls_box_widget)

        self.statusBar = QtGui.QStatusBar()
        self.setStatusBar(self.statusBar)

        # DATA
        self.all_data = []
        self.all_curves = []
        self.indexGr = 1
        self.step = 1
        self.leyend = []
        # CONTROLS
        self.dck_widget.parTr.sigTreeStateChanged.connect(self.changeModel)

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update1)

        # GRAPH
        self.definite_graph()
        self.restart_graph()
        self.create_toolbars()

        _i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:
                # sliderF = """def sliderValueChanged""" + str(_i) + """(self, value):\n\tprint(value/100)\n\n"""
                sliderF = "def sliderValueChanged" + str(_i) + "(self, int_value):\n\tprint(int_value / 100)\n\t" \
                    "plt2." + userDef.name + " = int_value / 100\n\tself.dck_widget.label[" + str(_i - 1) + "]" \
                    ".setText('" + userDef.description + " ' + str(eval('plt2." + userDef.name + "')) + ' " + userDef.unit + "')\n\t" \
                    "plt2.recalculate(self.indexGr)\n"

                _s_f_aux = "sliderValueChanged" + str(_i)
                # print(sliderF)
                exec(sliderF)
                exec("self." + _s_f_aux + " = types.MethodType(" + _s_f_aux + ", self)")

                _s_f_aux = "self.sliderValueChanged" + str(_i)

                # print(sliderF)
                # print(_s_f_aux)
                # exec(sliderF)

                #TODO que entre cuando se suelta el slider
                self.dck_widget.slider[_i-1].valueChanged.connect(eval(_s_f_aux))
                _i += 1

    def create_toolbars(self):
        prevAction = QtGui.QAction(QtGui.QIcon('prev.png'), 'Previous step', self)
        self.playAction = QtGui.QAction(QtGui.QIcon('play.png'), 'Play/Pause simulation', self)
        nextAction = QtGui.QAction(QtGui.QIcon('next.png'), 'Next step', self)
        resetAction = QtGui.QAction(QtGui.QIcon('reset.png'), 'Reset simulation', self)

        prevAction.triggered.connect(self.prev_frame)
        self.playAction.triggered.connect(self.play_stop)
        nextAction.triggered.connect(self.next_frame)
        resetAction.triggered.connect(self.restart_graph)

        self.ctrlToolBar = self.addToolBar('Tool Bar')

        self.ctrlToolBar.addAction(prevAction)
        self.ctrlToolBar.addAction(self.playAction)
        self.ctrlToolBar.addAction(nextAction)
        self.ctrlToolBar.addAction(resetAction)


        ##############################

        self.eventToolBar = self.addToolBar('Tool Bar 2')

        label1 = QtGui.QLabel("Step ")
        self.spboxStep = QtGui.QSpinBox()
        self.spboxStep.setValue(1)
        # TODO sacar unidad de xml
        label2 = QtGui.QLabel(" min every ")
        self.spBoxTimmer = QtGui.QSpinBox()
        self.spBoxTimmer.setRange(1, 60000)
        self.spBoxTimmer.setValue(500)
        label3 = QtGui.QLabel(" ms")

        self.eventToolBar.addWidget(label1)
        self.eventToolBar.addWidget(self.spboxStep)
        self.eventToolBar.addWidget(label2)
        self.eventToolBar.addWidget(self.spBoxTimmer)
        self.eventToolBar.addWidget(label3)

        self.spBoxTimmer.valueChanged.connect(self.timerChange)
        self.spboxStep.valueChanged.connect(self.stepChange)

    def stepChange(self):
        self.step = int(self.spboxStep.value())
        print(self.step)

    def close_app(self):
        choice = QtGui.QMessageBox.question(self, 'Exit?', 'Close application?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def timerChange(self):
        self.timer.setInterval(int(self.spBoxTimmer.value()))


    def changeModel(self, param, changes):
        print("tree changes MODEL:")
        _dats = plt2.obtener(self.indexGr)
        for param, change, data in changes:
            _i = -1
            j = 0
            var = 1
            while (var):
                if plt2._e[j].simulate:
                    _i += 1
                    if plt2._e[j].description == param._parent.name():
                        var = 0
                j += 1
            self.all_curves[_i] = self.ui.ui_sinc_plot.plot([plt2._xdata[0]], [_dats[j]],  symbol='o',
                        symbolPen='k', symbolBrush=1, name=plt2._e[j].name,
                        symbolSize=3, pen=pyqtgraph.mkPen(str(data.name()), width=self.dck_widget.pen_size[_i]))
            self.all_curves[_i].setData(plt2._xdata[:self.indexGr + 1], self.all_data[_i])



    def definite_graph(self):
        _i = 0
        _dats = plt2.obtener(0)
        self.mayor = _dats[0]
        self.menor = _dats[0]

        self.leyend = pyqtgraph.LegendItem((100, 60), offset=(70, 30))

        _j = 0

        for eq in plt2._e:
            # print(eq.simulate)
            if eq.simulate:
                self.all_data.append([plt2.obtener(0)[_i]])
                #print(plt2._xdata)
                self.all_curves.append(self.ui.ui_sinc_plot.plot([plt2._xdata[0]], [_dats[_i]],  symbol='o',
                        symbolPen='k', symbolBrush=1, name=eq.name,
                        symbolSize=3, pen=pyqtgraph.mkPen(self.dck_widget.colors[_i], width=self.dck_widget.pen_size[_i])))

                if _dats[_i] > self.mayor:
                    self.mayor = _dats[_i]

                if _dats[_i] < self.menor:
                    self.menor = _dats[_i]

                _j += 1

            _i += 1

        self.leyend.setParentItem(self.ui.ui_sinc_plot.graphicsItem())
        #self.ui.ui_sinc_plot.setYRange(self.menor - 10 , self.mayor + 10)

    def play_stop(self):
        if not self.timer.isActive():
            self.timer.start(500)
            self.playAction.setIcon(QtGui.QIcon('pause.png'))
        else:
            self.timer.stop()
            self.playAction.setIcon(QtGui.QIcon('play.png'))

    def next_frame(self):
        self.update1()

    def prev_frame(self):
        pass

    def restart_graph(self):
        self.indexGr = 0

        # TODO: falta restaurar los valores iniciales del XML
        #plt2.recalculate(0)

        _dats = plt2.obtener(0)
        _i = 0
        _j = 0
        for eq in plt2._e:
            if eq.simulate:
                self.leyend.removeItem(eq.name + ': ' + str(round(self.all_data[_i][self.indexGr -1], 2)))

                self.all_data[_i] = [_dats[_j]]
                self.all_curves[_i].setData(self.all_data[_i])

                self.leyend.addItem(self.all_curves[_i],
                                    eq.name + ': ' + str(round(self.all_data[_i][self.indexGr], 2)))
                _i += 1
            _j += 1
        self.timer.stop()

        plt2.recalculate(0)

    def update1(self):
        self.indexGr += 1
        self.ui.indexGr = self.indexGr
        _dats = plt2.obtener(self.indexGr)

        #print(_dats)
        _i = 0
        _j = 0
        for eq in plt2._e:
            if eq.simulate:
                #print(dats[_j])
                self.all_data[_i].append(_dats[_j])
                self.all_curves[_i].setData(plt2._xdata[:self.indexGr+1], self.all_data[_i])

                if _dats[_j] > self.mayor:
                    self.mayor = _dats[_j]

                if _dats[_j] < self.menor:
                    self.menor = _dats[_j]

                self.leyend.removeItem(eq.name + ': ' + str(round(self.all_data[_i][-2], 2)))
                self.leyend.addItem(self.all_curves[_i], eq.name + ': ' + str(round(self.all_data[_i][self.indexGr], 2)))

                _i += 1
            _j += 1

        #if self.indexGr % 5 == 0:
        self.ui.ui_sinc_plot.setXRange(plt2._xdata[self.indexGr+1] - 80, plt2._xdata[self.indexGr+1] + 20)
        #self.ui.ui_sinc_plot.setYRange(self.menor - 10, self.mayor + 10)

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



