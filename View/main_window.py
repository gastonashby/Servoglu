__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from View.pdf_dialog import ChildDlg
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

from View.ui_main_window import Ui_MainWindow
from View.ui_controls_widget import Ui_ControlsDockWidget
from View.ui_treat_widget import Ui_TreatDockWidget
from View.ui_properties_widget import Ui_PropertiesDockWidget
from View.ui_init_val_widget import Ui_InitialValuesDockWidget
from View.ui_menubar import Ui_Menubar
import os
import sys

import numpy
import types


class Window(QtGui.QMainWindow):
    def __init__(self, controller):
        super(Window, self).__init__()
        self.controller = controller
        self.setWindowTitle('SERVOGLU v1.0 - UdelaR - Núcleo de Ingeniería Biomédica')
        self.setWindowIcon(QtGui.QIcon('View/img/logo.png'))
        self.types = types
        self.numpy = numpy
        self.ui = Ui_MainWindow(self)
        self.languageHash = controller.languageSupport.languageHash
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
        self.round = 2  # General round

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
        
        self.multigraph = False

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.controller.handler_update_graph)
        self.timer.stop()

        self.ui.ui_menubar.create_toolbars()

    ## INIT

    def definite_graph(self):
        _i = 0
        self.dats = self.controller.np.multiply(self.controller.model.getPoint(), self.controller.eq_convert_factors)
        self.old_dats = self.dats

        sliderVals = self.ui.dck_treat_controls.get_sliders_vals()
        for aux in self.controller.model._u:
            if aux.isSlider:
                self.simulated_tr.append(True)
                self.treatment.append([sliderVals[_i]])
                self.all_treat_curves.append(self.create_treat_curve(_i, aux.name))

                if self.multigraph:
                    self.ui.setLabelSim(_i, self.controller.model._timeUnit)
                    self.ui.setLabelTr(_i, self.controller.model._timeUnit)
                    self.ui.setTitleSim(_i, self.controller.model._modelName[0:50])
                _i += 1

        for aux in self.controller.model._u:
            if aux.graphAsTreatment and not aux.isSlider:
                self.simulated_tr.append(True)
                self.treatment.append([sliderVals[_i]])
                self.all_treat_curves.append(self.create_treat_curve(_i, aux.name))

                if self.multigraph:
                    self.ui.setLabelSim(_i, self.controller.model._timeUnit)
                    self.ui.setLabelTr(_i, self.controller.model._timeUnit)
                    self.ui.setTitleSim(_i, self.controller.model._modelName[0:50])
                _i += 1

        if not self.multigraph:
            self.ui.setLabelSim(None, self.controller.model._timeUnit)
            self.ui.setLabelTr(None, self.controller.model._timeUnit)
            self.ui.setTitleSim(None, self.controller.model._modelName[0:50])


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
                                    '<span style="color: black"><strong>' + eq.name + ': ' + str(
                                        round(self.all_data[_i][self.indexGr], self.round)) + ' ' + eq.unit + '</strong></span>')
            if eq.alMinVal is not None:
                lin1 = pyqtgraph.InfiniteLine(movable=False, angle=0, pos=eq.alMinVal,
                                              pen=pyqtgraph.mkPen(
                                                  self.ui.dck_model_param_properties.colors[_i],
                                                  style=QtCore.Qt.DashLine,
                                                  width=2))
                self.minLines.append(lin1)
                if eq.simulate:
                    if self.multigraph:
                        self.ui.addItem(_i, lin1)
                    else:
                        self.ui.addItem(None, lin1)
            else:
                self.minLines.append(None)
                self.all_curves[_i].clear()

            if eq.alMaxVal != None:
                lin1 = pyqtgraph.InfiniteLine(movable=False, angle=0, pos=eq.alMaxVal,
                                              pen=pyqtgraph.mkPen(
                                                  self.ui.dck_model_param_properties.colors[_i],
                                                  style=QtCore.Qt.DashLine,
                                                  width=2))
                self.maxLines.append(lin1)
                if eq.simulate:
                    if self.multigraph:
                        self.ui.addItem(_i, lin1)
                    else:
                        self.ui.addItem(None, lin1)

            else:
                self.maxLines.append(None)
                self.all_curves[_i].clear()

            self.ui.dck_model_param_controls.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))

            self.alarms.append(False)
            self.alarmMin.append(eq.alMinVal)
            self.alarmMax.append(eq.alMaxVal)
            self.alarmMsg.append(eq.alDescription)

            _i += 1
        if self.multigraph:
            pass
        else:
            self.leyend.setParentItem(self.ui.ui_sinc_plot.graphicsItem())

        self.leyend.updateSize()
        self.modelTimeUnit = self.controller.model._timeUnit

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

        self.definite_controls()
        self.ui.ui_menubar.toggleActivationButtons(True)
        self.definite_graph()

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

    def create_curve(self, i, name):
        if self.multigraph:
            return self.ui.ui_sinc_plot[i].plot([self.xDataGraf[0]], [self.dats[i]], symbol='o',
                                         symbolPen='k', symbolBrush=1, name=name,
                                         symbolSize=3, antialias=True,
                                         pen=pyqtgraph.mkPen(self.ui.dck_model_param_properties.colors[i],
                                                             width=3))
        else:
            return self.ui.ui_sinc_plot.plot([self.xDataGraf[0]], [self.dats[i]], symbol='o',
                                             symbolPen='k', symbolBrush=1, name=name,
                                             symbolSize=3, antialias=True,
                                             pen=pyqtgraph.mkPen(self.ui.dck_model_param_properties.colors[i],
                                                                 width=3))

    def create_treat_curve(self, i, name):
        if self.multigraph:
            return self.ui.ui_treat_plot[i].plot([self.xDataGraf[0]], [self.ui.dck_treat_controls.get_sliders_vals()[i]],
                                          symbol='o',
                                          symbolPen='k', symbolBrush=1, name=name,
                                          symbolSize=3, antialias=True,
                                          pen=pyqtgraph.mkPen(self.ui.dck_treat_controls.colors[i],
                                                              width=3))
        else:
            return self.ui.ui_treat_plot.plot([self.xDataGraf[0]], [self.ui.dck_treat_controls.get_sliders_vals()[i]],
                                              symbol='o',
                                              symbolPen='k', symbolBrush=1, name=name,
                                              symbolSize=3, antialias=True,
                                              pen=pyqtgraph.mkPen(self.ui.dck_treat_controls.colors[i],
                                                                  width=3))

    ## UPDATE
    def update_time_index(self):
        # Update counters
        self.indexGr += self.step

        if self.controller.model._timeUnit == 's':
            self.timeCount += self.step * 1000
        elif self.controller.model._timeUnit == 'min':
            self.timeCount += self.step * 1000 * 60
        elif self.controller.model._timeUnit == 'hs':
            self.timeCount += self.step * 1000 * 60 * 60
        elif self.controller.model._timeUnit == 'ms':
            self.timeCount += self.step

        self.ui.ui_menubar.timeLbl.setText(self.controller.convertMs(self.timeCount))

    def update_graph(self, new_dats):
        old_dats = self.dats
        dats_aux = self.controller.np.multiply(new_dats, self.controller.eq_convert_factors)
        self.dats = dats_aux[len(dats_aux) - 1]

        treat = self.ui.dck_treat_controls.get_sliders_vals()

        _i = 0
        for aux in self.controller.model._u:
            if aux.graphAsTreatment:
                self.treatment[_i].extend([treat[_i]] * self.step)
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
            self.leyend.removeItem('<span style="color: black"><strong>' + eq.name + ': ' + str(round(old_dats[_i], self.round)) + ' ' + eq.unit + '</strong></span>')

            # Set the equations actual values in the SpinBoxs
            self.ui.dck_model_param_controls.eqCtrlList[_i].setValue(round(self.dats[_i], self.round))

            # Append the new values
            self.all_data[_i].extend(dats_aux[:,_i].tolist())

            # If simulated equation, add the value to the curve and the legend
            # Else clear the curve
            if self.simulated_eq[_i]:
                self.all_curves[_i].setData(self.xDataGraf[:self.indexGr +1], self.all_data[_i])
                self.leyend.addItem(self.all_curves[_i],
                                    '<span style="color: black"><strong>' + eq.name + ': ' + str(round(self.dats[_i], self.round)) + ' ' + eq.unit + '</strong></span>')

            else:
                self.all_curves[_i].clear()

            _i += 1

        self.check_alarms()

        # Refresh the X axis range
        if self.multigraph:
            for i in range(0, 4):
                self.ui.ui_sinc_plot[i].setXRange(self.xDataGraf[self.indexGr] - 20,
                                                  self.xDataGraf[self.indexGr] + 10)
                self.ui.ui_treat_plot[i].setXRange(self.xDataGraf[self.indexGr] - 20,
                                                   self.xDataGraf[self.indexGr] + 10)
        else:
            self.ui.ui_sinc_plot.setXRange(self.xDataGraf[self.indexGr] - 20,
                                           self.xDataGraf[self.indexGr] + 10)
            self.ui.ui_treat_plot.setXRange(self.xDataGraf[self.indexGr] - 20,
                                            self.xDataGraf[self.indexGr] + 10)

    def is_index_end_axis(self):
        return len(self.xDataGraf) - 2 <= self.indexGr

    def append_new_axis_points(self):
        linX = self.controller.model.np.arange(self.xDataGraf[len(self.xDataGraf) -1] + 1,
                                               self.xDataGraf[len(self.xDataGraf) -1] + self.simulated_cicle_steps,
                                               1)
        self.xDataGraf = self.controller.model.np.append(self.xDataGraf[:self.indexGr], linX)

    def activate_alarm(self, i, val):
        self.alarms[i] = val
        # self.ui.ui_menubar.alarmPic.setPixmap(QtGui.QPixmap(os.getcwd() + r"\View\img\alarm.png"))
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
            self.ui.ui_menubar.alarmPic.setToolTip(alarmToolTip)
            self.ui.ui_menubar.alarmPic.setText("\t\t" + str(cantAlarms) + " alarms.")
            self.ui.ui_menubar.alarmPic.setPixmap(QtGui.QPixmap(os.getcwd() + r"\View\img\alarm.png"))
            self.ui.ui_menubar.alarmPic.show()
        else:
            self.ui.ui_menubar.alarmPic.clear()

    def remove_graph_labels(self):
        _i = 0
        if self.dats != []:
            for eq in self.controller.model._e:
                # print(self.dats[_i])
                self.leyend.removeItem('<span style="color: black"><strong>' + eq.name + ': ' +
                                       str(round(self.dats[_i], self.round)) + ' ' + eq.unit + '</strong></span>')
                _i += 1


    ## ACTIONS
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
                self.ui.ui_menubar.alarmPic.clear()
                self.ui.ui_menubar.eventToolBar.clear()
                self.ui.ui_menubar.alarmToolBar.clear()
                self.removeDockWidget(self.ui.dck_model_param_properties.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_model_param_controls.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_treat_controls.ui_controls_box_widget)
                self.removeDockWidget(self.ui.dck_init_val_controls.ui_controls_box_widget)

                for a in self.minLines:
                    if self.multigraph:
                        for i in range(0,4):
                            self.ui.ui_sinc_plot[i].removeItem(a)
                    else:
                        self.ui.ui_sinc_plot.removeItem(a)

                for a in self.maxLines:
                    if self.multigraph:
                        for i in range(0,4):
                            self.ui.ui_sinc_plot.removeItem(a)
                    else:
                        self.ui.ui_sinc_plot.removeItem(a)

                self.minLines = []
                self.maxLines = []

                for gr in self.all_curves:
                    gr.clear()
                self.all_curves = []

                for gr in self.all_treat_curves:
                    gr.clear()
                self.all_treat_curves = []
                
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def close_app(self):
        choice = QtGui.QMessageBox.question(self, 'Exit?', 'Close application?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()

    def timerChange(self):
        interv = int(self.ui.ui_menubar.spBoxTimmer.value() * 1000)
        print(interv)
        self.timer.setInterval(interv)

    def play_stop(self):
        if not self.timer.isActive():
            self.timer.start()
            self.ui.ui_menubar.playAction.setIcon(QtGui.QIcon('View/img/pause.png'))
        else:
            self.timer.stop()
            self.ui.ui_menubar.playAction.setIcon(QtGui.QIcon('View/img/play.png'))

    def stop(self):
        self.timer.stop()
        self.ui.ui_menubar.playAction.setIcon(QtGui.QIcon('View/img/play.png'))

    def next_frame(self):
        self.controller.handler_update_graph()

    def restart_graph(self):
        self.ui.ui_menubar.playAction.setIcon(QtGui.QIcon('View/img/play.png'))
        self.controller.handler_restart_graph()
        self.ui.ui_menubar.init_time_controlls(self.modelTimeUnit)

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
                    self.ui.ui_menubar.init_time_controlls(self.modelTimeUnit)
                    self.openModel = name
                except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()
