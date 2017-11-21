__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from View.pdf_dialog import ChildDlg
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from Controller.main_controller import *
from View.ui_main_window import Ui_MainWindow
from View.ui_controls_widget import Ui_ControlsDockWidget
from View.ui_treat_widget import Ui_TreatDockWidget
from View.ui_properties_widget import Ui_PropertiesDockWidget
from View.ui_init_val_widget import Ui_InitialValuesDockWidget
from View.ui_menubar import Ui_Menubar
import os

import numpy
import types


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.controller = Controller(self)
        self.setWindowTitle('SERVOGLU v1.0 - UdelaR - Núcleo de Ingeniería Biomédica')
        self.setWindowIcon(QtGui.QIcon('View/img/logo.png'))
        self.types = types
        self.ui = Ui_MainWindow(self)

        # self.ui.dck_model_param_properties = Ui_PropertiesDockWidget()
        # self.ui.dck_model_param_properties.setupUi(self)
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.ui.dck_model_param_properties.ui_controls_box_widget)

        # MENUBAR
        self.ui.ui_menubar = Ui_Menubar(self)
        self.ui.ui_menubar.setupUi()
        self.setMenuBar(self.ui.ui_menubar.ui_menubar)

        # MENU ACTION
        self.ui.ui_menubar.open_action.triggered.connect(self.open_model)
        self.ui.ui_menubar.exit_action.triggered.connect(self.close_app)
        self.ui.ui_menubar.export_action.triggered.connect(self.exportResultsToPdf)

        self.ui.dck_model_param_properties = []
        self.ui.dck_model_param_controls = []
        self.ui.dck_treat_controls = []

        self.statusBar = QtGui.QStatusBar()

        self.statusBar.addPermanentWidget(QtGui.QLabel(self.controller.version))
        self.setStatusBar(self.statusBar)

        # INITIAL SETTINGS
        self.round = 4  # General round

        self.simulated_cicle_number = 1  # Internal variable
        self.simulated_cicle_steps = 1000  # Cicle
        self.modelUbic = ""
        self.modelTimeUnit = ""

        self.simulated_eq = []  # Array of bool to indicate the simulated graph
        self.simulated_tr = []  # Array of bool to indicate the treat graph

        # X Axis, default 1000 elements from 0 to 999
        self.xDataGraf = self.controller.create_X_axis(0, self.simulated_cicle_number * self.simulated_cicle_steps - 1
                                                       , self.simulated_cicle_number * self.simulated_cicle_steps * 2)

        self.timeCount = 0
        self.all_data = []
        self.all_curves = []
        self.all_treat_curves = []
        self.indexGr = 0
        self.step = 1

        self.dats = []
        self.treatment = []
        self.leyend = pyqtgraph.LegendItem((100, 60), offset=(70, 30))
        self.alarmMin = []
        self.alarmMax = []
        self.alarmMsg = []
        self.alarms = []
        self.minLines = []
        self.maxLines = []
        self.alarmPic = None

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.controller.handler_update_graph)
        self.timer.stop()

        self.create_toolbars()

    def is_index_end_axis(self):
        return len(self.xDataGraf) - 2 == self.indexGr

    def append_new_axis_points(self):
        linX = self.controller.model.np.linspace(self.xDataGraf[self.indexGr]
                                                 , self.xDataGraf[self.indexGr] + (
                                                     self.step * (
                                                         (
                                                         self.simulated_cicle_number * self.simulated_cicle_steps) - 1))
                                                 , self.simulated_cicle_number * self.simulated_cicle_steps)
        self.xDataGraf = self.controller.model.np.append(self.xDataGraf[:self.indexGr], linX)

    def update_time_index(self):
        # Update counters
        self.indexGr += 1

        if self.controller.model._timeUnit == 's':
            self.timeCount += self.step * 1000
        elif self.controller.model._timeUnit == 'min':
            self.timeCount += self.step * 1000 * 60
        elif self.controller.model._timeUnit == 'hs':
            self.timeCount += self.step * 1000 * 60 * 60

        self.timeLbl.setText(self.controller.convertMs(self.timeCount))

    def activate_alarm(self, i, val):
        self.alarms[i] = val
        # self.alarmPic.setPixmap(QtGui.QPixmap(os.getcwd() + r"\View\img\alarm.png"))
        # self.alarmToolBar.show()

    def check_alarms(self):
        alarm = False
        alarmToolTip = ""
        _i = 0
        cantAlarms = 0
        for al in self.alarms:
            if al:
                alarmToolTip += self.alarmMsg[_i] + " ("+ str(self.alarmMin[_i]) + ", " + \
                                str(self.alarmMax[_i]) + ")" + ".\n"
                alarm = True
                cantAlarms += 1
                self.alarms[_i] = False
            _i += 1

        alarmToolTip = alarmToolTip[:len(alarmToolTip)-2]

        if alarm:
            self.alarmPic.setToolTip(alarmToolTip)
            self.alarmPic.setText("\t\t" + str(cantAlarms) + " alarms.")
            self.alarmPic.setPixmap(QtGui.QPixmap(os.getcwd() + r"\View\img\alarm.png"))
            self.alarmPic.show()
        else:
            self.alarmPic.clear()

    def update_graph(self, new_dats):
        old_dats = self.dats
        self.dats = self.controller.np.multiply(new_dats, self.controller.eq_convert_factors)
        treat = self.ui.dck_treat_controls.get_sliders_vals()

        _i = 0
        for aux in self.controller.model._u:
            if aux.graphAsTreatment:
                self.treatment[_i].append(treat[_i])
                if self.simulated_tr[_i]:
                    self.all_treat_curves[_i].setData(self.xDataGraf[:self.indexGr + 1],
                                                      self.treatment[_i])
                else:
                    self.all_treat_curves[_i].clear()
                _i += 1

        # Update graph
        _i = 0
        for eq in self.controller.model._e:

            if self.alarmMin[_i] != None and self.alarmMin[_i] > self.dats[_i]:
                self.activate_alarm(_i, True)

            if self.alarmMax[_i] != None and self.alarmMax[_i] < self.dats[_i]:
                self.activate_alarm(_i, True)

            # Delete legend old values
            self.leyend.removeItem(eq.name + ': ' + str(round(old_dats[_i], self.round)) + ' ' + eq.unit)

            # Set the equations actual values in the SpinBoxs
            self.ui.dck_model_param_controls.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))

            # Append the new values
            self.all_data[_i].append(self.dats[_i])

            # If simulated equation, add the value to the curve and the legend
            # Else clear the curve
            if self.simulated_eq[_i]:
                self.all_curves[_i].setData(self.xDataGraf[:self.indexGr + 1], self.all_data[_i])
                self.leyend.addItem(self.all_curves[_i],
                                    eq.name + ': ' + str(round(self.dats[_i], self.round)) + ' ' + eq.unit)

            else:
                self.all_curves[_i].clear()
            _i += 1

        self.check_alarms()

        # Refresh the X axis range
        self.ui.ui_sinc_plot.setXRange(self.xDataGraf[self.indexGr] - 20,
                                       self.xDataGraf[self.indexGr] + 10)
        self.ui.ui_treat_plot.setXRange(self.xDataGraf[self.indexGr] - 20,
                                        self.xDataGraf[self.indexGr] + 10)

    def remove_graph_labels(self):
        _i = 0
        if self.dats != []:
            for eq in self.controller.model._e:
                # print(self.dats[_i])
                self.leyend.removeItem(eq.name + ': ' + str(round(self.dats[_i], self.round)) + ' ' + eq.unit)
                _i += 1

    def restart_graphs(self):
        # if is open a previous model
        try:
            if self.ui.dck_model_param_properties != []:
                self.remove_graph_labels()
                self.indexGr = 0
                self.timeCount = 0
                self.simulated_eq = []
                self.simulated_tr = []
                self.alarmMin = []
                self.alarmMax = []
                self.alarmMsg = []
                self.alarms = []
                self.step = 1
                self.alarmPic.clear()
                self.removeDockWidget(self.ui.dck_model_param_properties.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_model_param_controls.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_treat_controls.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_init_val_controls.ui_controls_box_widget)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def definite_controls(self):

        self.ui.dck_init_val_controls = Ui_InitialValuesDockWidget()
        self.ui.dck_init_val_controls.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ui.dck_init_val_controls.ui_controls_box_widget)

        self.ui.dck_model_param_controls = Ui_ControlsDockWidget()
        self.ui.dck_model_param_controls.setupUi(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.ui.dck_model_param_controls.ui_controls_box_widget)

        self.ui.dck_model_param_properties = Ui_PropertiesDockWidget()
        self.ui.dck_model_param_properties.setupUi(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.ui.dck_model_param_properties.ui_controls_box_widget)
        self.ui.dck_model_param_properties.parTr.sigTreeStateChanged.connect(
            self.controller.handler_change_model_propertie)

        self.ui.dck_treat_controls = Ui_TreatDockWidget()
        self.ui.dck_treat_controls.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ui.dck_treat_controls.ui_controls_box_widget)
        self.controller.handler_definite_controls()

    def create_toolbars(self):
        self.playAction = QtGui.QAction(QtGui.QIcon('View/img/play.png'),
                                        self.controller.languageSupport.languageHash.__getitem__("lbl.PlayPause"), self)
        self.nextAction = QtGui.QAction(QtGui.QIcon('View/img/next.png'), 'Next step', self)
        self.resetAction = QtGui.QAction(QtGui.QIcon('View/img/reset.png'), 'Reset simulation', self)

        self.playAction.triggered.connect(self.play_stop)
        self.nextAction.triggered.connect(self.next_frame)
        self.resetAction.triggered.connect(self.restart_graph)

        self.ctrlToolBar = self.addToolBar('Simulation controls')

        self.ctrlToolBar.addAction(self.playAction)
        self.ctrlToolBar.addAction(self.nextAction)
        self.ctrlToolBar.addAction(self.resetAction)

        self.eventToolBar = self.addToolBar('Time controls')

        label1 = QtGui.QLabel("Step ")
        self.spboxStep = QtGui.QSpinBox()
        self.spboxStep.setValue(1)
        self.spboxStep.setMinimum(1)

        label2 = QtGui.QLabel(" every ")
        self.spBoxTimmer = QtGui.QSpinBox()
        self.spBoxTimmer.setRange(50, 60000)
        self.spBoxTimmer.setValue(500)
        self.spBoxTimmer.setSingleStep(50)
        self.spBoxTimmer.setSuffix(" ms")

        self.eventToolBar.addWidget(label1)
        self.eventToolBar.addWidget(self.spboxStep)
        self.eventToolBar.addWidget(label2)
        self.eventToolBar.addWidget(self.spBoxTimmer)

        self.spBoxTimmer.valueChanged.connect(self.timerChange)
        self.spboxStep.valueChanged.connect(self.controller.handler_step_change)
        self.toggleActivationButtons(False)

        self.alarmToolBar = self.addToolBar('Alarm Toolbar')

        self.alarmPic = QtGui.QLabel(self)
        self.alarmToolBar.addWidget(self.alarmPic)

        self.init_time_label()

    def init_time_label(self):
        label = QtGui.QLabel("Simulation time (D:HH:MM:SS): ")
        self.timeLbl = QtGui.QLabel("0:00:00:00")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        myFont.setPointSize(11)
        self.timeLbl.setFont(myFont)

        self.eventToolBar.addWidget(QtGui.QLabel("   "))
        self.eventToolBar.addWidget(label)
        self.eventToolBar.addWidget(self.timeLbl)

    def initialize_graphs(self, name):
        self.modelUbic = name
        self.xDataGraf = self.controller.model.np.arange(0,
                                                         self.simulated_cicle_number * self.simulated_cicle_steps - 1,
                                                         1)

        for gr in self.all_curves:
            gr.clear()
        for gr in self.all_treat_curves:
            gr.clear()

        self.all_data = []
        self.treatment = []
        self.all_treat_curves = []
        self.simulated_eq = []
        self.simulated_tr = []
        self.timeLbl.setText(self.controller.convertMs(0))
        self.definite_controls()
        self.toggleActivationButtons(True)
        self.definite_graph()

    def definite_graph(self):
        _i = 0
        self.dats = self.controller.np.multiply(self.controller.model.getPoint(), self.controller.eq_convert_factors)
        self.old_dats = self.dats

        sliderVals = self.ui.dck_treat_controls.get_sliders_vals()
        for aux in self.controller.model._u:
            if aux.graphAsTreatment:
                self.simulated_tr.append(True)
                self.treatment.append([sliderVals[_i]])
                self.all_treat_curves.append(self.create_treat_curve(_i, aux.name))
                _i += 1

        self.ui.ui_sinc_plot.setLabel('bottom', 'Time', units=self.controller.model._timeUnit)
        self.ui.ui_sinc_plot.setTitle(self.controller.model._modelName[0:50])
        self.ui.ui_treat_plot.setLabel('bottom', 'Time', units=self.controller.model._timeUnit)

        _i = 0
        for eq in self.controller.model._e:
            if eq.simulate:
                self.simulated_eq.append(True)
            else:
                self.simulated_eq.append(False)

            self.all_data.append([self.dats[_i]])
            self.all_curves.append(self.create_curve(_i, eq.name))

            if eq.simulate:
                self.leyend.addItem(self.all_curves[_i],
                                    eq.name + ': ' + str(
                                        round(self.all_data[_i][self.indexGr], self.round)) + ' ' + eq.unit)
            if eq.alMinVal != None:
                lin1 = pyqtgraph.InfiniteLine(movable=False, angle=0, pos=eq.alMinVal,
                                                              pen=pyqtgraph.mkPen(
                                                              self.ui.dck_model_param_properties.colors[_i],
                                                              style=QtCore.Qt.DashLine,
                                                              width=2))
                self.minLines.append(lin1)
                if eq.simulate:
                    self.ui.ui_sinc_plot.addItem(lin1)

            if eq.alMaxVal != None:
                lin1 = pyqtgraph.InfiniteLine(movable=False, angle=0, pos=eq.alMaxVal,
                                                              pen=pyqtgraph.mkPen(
                                                              self.ui.dck_model_param_properties.colors[_i],
                                                              style=QtCore.Qt.DashLine,
                                                              width=2))
                self.maxLines.append(lin1)
                if eq.simulate:
                    self.ui.ui_sinc_plot.addItem(lin1)

            else:
                self.all_curves[_i].clear()

            self.ui.dck_model_param_controls.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))

            self.alarms.append(False)
            self.alarmMin.append(eq.alMinVal)
            self.alarmMax.append(eq.alMaxVal)
            self.alarmMsg.append(eq.alDescription)

            _i += 1
        self.leyend.setParentItem(self.ui.ui_sinc_plot.graphicsItem())
        self.leyend.updateSize()
        self.modelTimeUnit = self.controller.model._timeUnit
        self.spboxStep.setSuffix(" " + self.modelTimeUnit)
        self.spboxStep.setValue(1)

    def create_line(self, minmax, _i):
        if minmax == "MIN":
            return pyqtgraph.InfiniteLine(movable=False, angle=0, pos=self.alarmMin[_i],
                                          pen=pyqtgraph.mkPen(
                                              self.ui.dck_model_param_properties.colors[_i],
                                              style=QtCore.Qt.DashLine,
                                              width=2))
        elif minmax == "MAX":
            return pyqtgraph.InfiniteLine(movable=False, angle=0, pos=self.alarmMax[_i],
                                          pen=pyqtgraph.mkPen(
                                              self.ui.dck_model_param_properties.colors[_i],
                                              style=QtCore.Qt.DashLine,
                                              width=2))

    def toggleActivationButtons(self, enabled):
        self.nextAction.setEnabled(enabled)
        self.resetAction.setEnabled(enabled)
        self.playAction.setEnabled(enabled)
        self.spboxStep.setEnabled(enabled)
        self.spBoxTimmer.setEnabled(enabled)
        self.ui.ui_menubar.export_action.setEnabled(enabled)

    def close_app(self):
        choice = QtGui.QMessageBox.question(self, 'Exit?', 'Close application?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()

    def timerChange(self):
        self.timer.setInterval(int(self.spBoxTimmer.value()))

    def create_curve(self, i, name):
        return self.ui.ui_sinc_plot.plot([self.xDataGraf[0]], [self.dats[i]], symbol='o',
                                         symbolPen='k', symbolBrush=1, name=name,
                                         symbolSize=3, antialias=True,
                                         pen=pyqtgraph.mkPen(self.ui.dck_model_param_properties.colors[i],
                                                             width=self.ui.dck_model_param_properties.pen_size[i]))

    def create_treat_curve(self, i, name):
        return self.ui.ui_treat_plot.plot([self.xDataGraf[0]], [self.ui.dck_treat_controls.get_sliders_vals()[i]],
                                          symbol='o',
                                          symbolPen='k', symbolBrush=1, name=name,
                                          symbolSize=3, antialias=True,
                                          pen=pyqtgraph.mkPen(self.ui.dck_treat_controls.colors[i],
                                                              width=self.ui.dck_treat_controls.pen_size[i]))

    def play_stop(self):
        if not self.timer.isActive():
            self.timer.start(int(self.spBoxTimmer.value()))
            self.playAction.setIcon(QtGui.QIcon('View/img/pause.png'))
        else:
            self.timer.stop()
            self.playAction.setIcon(QtGui.QIcon('View/img/play.png'))

    def stop(self):
        self.timer.stop()
        self.playAction.setIcon(QtGui.QIcon('View/img/play.png'))

    def next_frame(self):
        self.controller.handler_update_graph()

    def restart_graph(self):
        self.playAction.setIcon(QtGui.QIcon('View/img/play.png'))
        self.controller.handler_restart_graph()

    def exportResultsToPdf(self):
        self.stop()
        PDFdialog = ChildDlg(self)
        PDFdialog.show()

    def open_model(self):
        myFilter = ["XML file (*.xml)"]
        name, _ = QFileDialog.getOpenFileName(self, 'Open XML SERVOGLU model...', "", "XML file (*.xml)",
                                              options=QFileDialog.DontUseNativeDialog)
        if name != "":
            if name.endswith(".xml"):
                try:
                    self.controller.handler_open_model(name)
                    self.ui.ui_menubar.setPossibleModelLanguages()
                    self.ui.ui_menubar.changeLanguageModel.setEnabled(True)
                    self.openModel = name
                except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()


