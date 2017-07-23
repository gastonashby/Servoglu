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

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)
        self.round = 4
        # EXIT ACTION
        self.ui.ui_menubar.exit_action.triggered.connect(self.close)

        # EXPORT TO EDF
        self.ui.ui_menubar.export_action.triggered.connect(self.exportToEDF)

        self.dck_widget = Ui_ControlsBoxDockWidget()
        self.dck_widget.setupUi(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dck_widget.ui_controls_box_widget)

        self.dck_param = Ui_GeneralControlsWidget()
        self.dck_param.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dck_param.ui_controls_box_widget)

        self.statusBar = QtGui.QStatusBar()
        self.setStatusBar(self.statusBar)

        # DATA
        self.simulated_cicle_number = 1
        self.simulated_cicle_steps = 1000
        
        self.xDataGraf = plt2.np.linspace(0, self.simulated_cicle_number * self.simulated_cicle_steps -1
                                          , self.simulated_cicle_number * self.simulated_cicle_steps, dtype=plt2.np.int32)
        self.timeCount = 0
        self.all_data = []
        self.all_curves = []
        self.indexGr = 0
        self.step = 1
        self.leyend = []
        self.dats = plt2.getPoint()
        self.old_dats = self.dats
        # CONTROLS
        self.dck_widget.parTr.sigTreeStateChanged.connect(self.changeModelPropertie)

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update1)
        self.timer.stop()

        # GRAPH
        self.create_toolbars()
        self.definite_graph()
        #self.restart_graph()

        _i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:
                # sliderF = """def sliderValueChanged""" + str(_i) + """(self, value):\n\tprint(value/100)\n\n"""
                sliderF = "def sliderValueChanged" + str(_i) + "(self, int_value):\n\tprint(int_value / 100)\n\t" \
                    "plt2." + userDef.name + " = int_value / 100\n\tself.dck_param.label[" + str(_i - 1) + "]" \
                    ".setText('" + userDef.description + " ' + str(eval('plt2." + userDef.name + "')) + ' " + userDef.unit + "')\n\t" \
                    "plt2.recalculate()\n"

                _s_f_aux = "sliderValueChanged" + str(_i)
                # print(sliderF)
                exec(sliderF)
                exec("self." + _s_f_aux + " = types.MethodType(" + _s_f_aux + ", self)")

                _s_f_aux = "self.sliderValueChanged" + str(_i)

                # print(sliderF)
                # print(_s_f_aux)
                # exec(sliderF)

                #TODO que entre cuando se suelta el slider
                self.dck_param.slider[_i-1].valueChanged.connect(eval(_s_f_aux))
                _i += 1


    def changeActualPoint(self, i, value):
        self.all_data[i][self.indexGr] = value
        self.all_curves[i].setData(self.xDataGraf[:self.indexGr + 1], self.all_data[i])

        _i = 0
        for eq in plt2._e:
            self.leyend.removeItem(eq.name + ': ' + str(round(self.dats[_i], self.round)))
            _i += 1

        self.dats[i] = value
        plt2.recalculate()

        _i = 0
        for eq in plt2._e:
            self.leyend.addItem(self.all_curves[_i], eq.name + ': ' + str(round(self.dats[_i], self.round)))

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

        self.ctrlToolBar = self.addToolBar('Simulation controls')

        self.ctrlToolBar.addAction(prevAction)
        self.ctrlToolBar.addAction(self.playAction)
        self.ctrlToolBar.addAction(nextAction)
        self.ctrlToolBar.addAction(resetAction)


        ##############################

        self.eventToolBar = self.addToolBar('Time controls')

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
        plt2.change_scale(self.step)
        plt2.recalculate()
        linX = plt2.np.linspace(self.xDataGraf[self.indexGr]
                        , self.xDataGraf[self.indexGr] + (self.step * ((self.simulated_cicle_number * self.simulated_cicle_steps) - 1))
                        , self.simulated_cicle_number * self.simulated_cicle_steps, dtype=plt2.np.int32)
        #plt2.np.concatenate((arr1, arr2), axis=0)
        self.xDataGraf = plt2.np.append(self.xDataGraf[:self.indexGr], linX)

        print("Main ", self.xDataGraf[:self.indexGr +10])

    def close_app(self):
        choice = QtGui.QMessageBox.question(self, 'Exit?', 'Close application?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def timerChange(self):
        self.timer.setInterval(int(self.spBoxTimmer.value()))

    def changeModelPropertie(self, param, changes):
        print("change color:")
        for param, change, data in changes:

            _i = -1
            # j = 0
            var = 1

            while (var):
                # if plt2._e[j].simulate:
                _i += 1
                if plt2._e[_i].description == param._parent.name():
                    var = 0
                # j += 1

            self.all_curves[_i].clear()
            self.all_curves[_i] = self.ui.ui_sinc_plot.plot([self.xDataGraf[0]], [self.dats[_i]],  symbol='o',
                        symbolPen='k', symbolBrush=1, name=plt2._e[_i].name,
                        symbolSize=3, pen=pyqtgraph.mkPen(str(data.name()), width=self.dck_widget.pen_size[_i]))
            self.all_curves[_i].setData(self.xDataGraf[:self.indexGr + 1], self.all_data[_i])

    def definite_graph(self):
        _i = 0
        # self.mayor = self.dats[0]
        # self.menor = self.dats[0]

        self.leyend = pyqtgraph.LegendItem((100, 60), offset=(70, 30))

        #_j = 0

        for eq in plt2._e:
            # print(eq.simulate)
            # if eq.simulate:
            self.all_data.append([self.dats[_i]])
            self.all_curves.append(self.ui.ui_sinc_plot.plot([self.xDataGraf[0]], [self.dats[_i]],  symbol='o',
                    symbolPen='k', symbolBrush=1, name=eq.name,
                    symbolSize=3, pen=pyqtgraph.mkPen(self.dck_widget.colors[_i], width=self.dck_widget.pen_size[_i])))

            self.leyend.addItem(self.all_curves[_i],
                                eq.name + ': ' + str(round(self.all_data[_i][self.indexGr], self.round)))
            self.dck_param.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))
            # if self.dats[_i] > self.mayor:
            #     self.mayor = self.dats[_i]
            #
            # if self.dats[_i] < self.menor:
            #     self.menor = self.dats[_i]

            # _j += 1

            _i += 1
        self.leyend.setParentItem(self.ui.ui_sinc_plot.graphicsItem())
        # self.ui.ui_sinc_plot.setYRange(0 , 20)

    def play_stop(self):
        if not self.timer.isActive():
            self.timer.start(int(self.spBoxTimmer.value()))
            self.playAction.setIcon(QtGui.QIcon('pause.png'))
        else:
            self.timer.stop()
            self.playAction.setIcon(QtGui.QIcon('play.png'))

    def next_frame(self):
        self.update1()

    def prev_frame(self):
        #TODO: todo
        pass

    def restart_graph(self):
        self.timer.stop()
        plt2.restart()
        self.indexGr = 0
        self.playAction.setIcon(QtGui.QIcon('play.png'))
        # TODO: falta restaurar los valores iniciales del XML?
        self.xDataGraf = plt2.np.linspace(0, self.simulated_cicle_number * self.simulated_cicle_steps -1
                                          , self.simulated_cicle_number * self.simulated_cicle_steps, dtype=plt2.np.int32)
        _i = 0
        # _j = 0
        for eq in plt2._e:
            #if eq.simulate:
            self.leyend.removeItem(eq.name + ': ' + str(round(self.dats[_i], self.round)))
            _i += 1
            #_j += 1

        self.dats = plt2.getPoint()
        _i = 0
        # _j = 0
        for eq in plt2._e:
            #if eq.simulate:
            self.all_data[_i] = [self.dats[_i]]
            self.all_curves[_i].setData(self.all_data[_i])

            self.leyend.addItem(self.all_curves[_i],
                                eq.name + ': ' + str(round(self.all_data[_i][self.indexGr], self.round)))
            _i += 1
            #_j += 1

    def convertMs(self, mili):
        # ms = mili % 1000
        s = (mili / 1000) % 60
        m = (mili / (1000 * 60)) % 60
        h = (mili / (1000 * 60 * 60)) % 24
        if h < 10:
            h = "0" + str(int(h))
        else:
            h = str(int(h))

        if m < 10:
            m = "0" + str(int(m))
        else:
            m = str(int(m))

        if s < 10:
            s = "0" + str(int(s))
        else:
            s = str(int(s))

        # if ms < 10:
        #     ms = "00" + str(int(ms))
        # elif ms < 100:
        #     ms = "0" + str(int(ms))
        # else:
        #     ms = str(int(ms))

        return h + ":" + m + ":" + s #+ ":" + ms

    def update1(self):
        self.indexGr += 1
        self.ui.indexGr = self.indexGr #TODO usar parent
        self.timeCount += self.step * 1000 * 60
        self.dck_param.timeLbl.setText(self.convertMs(self.timeCount))

        _i = 0
        if len(self.xDataGraf) - 2 == self.indexGr:
            linX = plt2.np.linspace(self.xDataGraf[self.indexGr]
                                    , self.xDataGraf[self.indexGr] + (
                                    self.step * ((self.simulated_cicle_number * self.simulated_cicle_steps) - 1))
                                    , self.simulated_cicle_number * self.simulated_cicle_steps, dtype=plt2.np.int32)
            # plt2.np.concatenate((arr1, arr2), axis=0)
            self.xDataGraf = plt2.np.append(self.xDataGraf[:self.indexGr], linX)


        for eq in plt2._e:
            self.leyend.removeItem(eq.name + ': ' + str(round(self.dats[_i], self.round)))
            _i += 1

        self.dats = plt2.getPoint()

        _i = 0
        # _j = 0
        for eq in plt2._e:

            self.dck_param.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))
            # if eq.simulate:
            #print(dats[_j])
            self.all_data[_i].append(self.dats[_i])
            self.all_curves[_i].setData(self.xDataGraf[:self.indexGr+1], self.all_data[_i])

            # if self.dats[_j] > self.mayor:
            #     self.mayor = self.dats[_j]
            #
            # if self.dats[_j] < self.menor:
            #     self.menor = self.dats[_j]

            self.leyend.addItem(self.all_curves[_i], eq.name + ': ' + str(round(self.dats[_i], self.round)))

            _i += 1
            # _j += 1
        # act_range = plt2.np.absolute(self.ui.ui_sinc_plot.getAxis('bottom').range[1]) + \
        #             plt2.np.absolute(self.ui.ui_sinc_plot.getAxis('bottom').range[0])
        self.ui.ui_sinc_plot.setXRange(self.xDataGraf[self.indexGr] - 20,
                                       self.xDataGraf[self.indexGr] + 10)
        # print('x axis range: {}'.format(self.ui.ui_sinc_plot.getAxis('bottom').range))

        # self.ui.ui_sinc_plot.setYRange(0, 20)

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



