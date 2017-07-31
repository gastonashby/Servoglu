__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Controller.main_controller import *
from View.ui_main_window import Ui_MainWindow
from View.ui_controls_widget import Ui_ControlsDockWidget
from View.ui_properties_widget import Ui_PropertiesDockWidget


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.controller = Controller(self)
        self.setWindowTitle('SERVOGLU')
        self.setWindowIcon(QtGui.QIcon('View/img/logo.png'))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mbar = self.setMenuBar(self.ui.ui_menubar.ui_menubar)

        # MENU ACTION
        self.ui.ui_menubar.open_action.triggered.connect(self.open_model)
        self.ui.ui_menubar.exit_action.triggered.connect(self.close_app)
        self.ui.ui_menubar.export_action.triggered.connect(self.exportToEDF)

        self.ui.dck_model_param_properties = []
        self.ui.dck_model_param_controls = []

        self.statusBar = QtGui.QStatusBar()
        self.setStatusBar(self.statusBar)


        # INITIAL SETTINGS
        self.round = 4          # General round
        self.simulated_cicle_number = 1     # Internal variable
        self.simulated_cicle_steps = 1000   # Cicle
        self.modelUbic = ""
        self.simulated_eq = []  # Array of bool to indicate the simulated graph

        # X Axis, default 1000 elements from 0 to 999
        self.xDataGraf = self.controller.create_X_axis(0, self.simulated_cicle_number * self.simulated_cicle_steps -1
                                          , self.simulated_cicle_number * self.simulated_cicle_steps)

        self.timeCount = 0
        self.all_data = []
        self.all_curves = []
        self.indexGr = 0
        self.step = 1
        self.dats = []
        self.leyend = pyqtgraph.LegendItem((100, 60), offset=(70, 30))

        # TIMMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.controller.handler_update_graph)
        self.timer.stop()

        self.create_toolbars()

    def definite_controls(self):
        self.ui.dck_model_param_properties = Ui_PropertiesDockWidget()
        self.ui.dck_model_param_properties.setupUi(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.ui.dck_model_param_properties.ui_controls_box_widget)

        self.ui.dck_model_param_controls = Ui_ControlsDockWidget()
        self.ui.dck_model_param_controls.setupUi(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ui.dck_model_param_controls.ui_controls_box_widget)
        self.ui.dck_model_param_properties.parTr.sigTreeStateChanged.connect(self.controller.handler_change_model_propertie)

        self.controller.handler_definite_controls()


    def create_toolbars(self):
        self.prevAction = QtGui.QAction(QtGui.QIcon('View/img/prev.png'), 'Previous step', self)
        self.playAction = QtGui.QAction(QtGui.QIcon('View/img/play.png'), 'Play/Pause simulation', self)
        self.nextAction = QtGui.QAction(QtGui.QIcon('View/img/next.png'), 'Next step', self)
        self.resetAction = QtGui.QAction(QtGui.QIcon('View/img/reset.png'), 'Reset simulation', self)

        self.prevAction.triggered.connect(self.prev_frame)
        self.playAction.triggered.connect(self.play_stop)
        self.nextAction.triggered.connect(self.next_frame)
        self.resetAction.triggered.connect(self.restart_graph)

        self.ctrlToolBar = self.addToolBar('Simulation controls')

        self.ctrlToolBar.addAction(self.prevAction)
        self.ctrlToolBar.addAction(self.playAction)
        self.ctrlToolBar.addAction(self.nextAction)
        self.ctrlToolBar.addAction(self.resetAction)

        self.prevAction.setVisible(False)

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
        self.spboxStep.valueChanged.connect(self.controller.handler_step_change)
        self.toggleActivationButtons(False)

    def toggleActivationButtons(self, enabled):
        self.nextAction.setEnabled(enabled)
        self.resetAction.setEnabled(enabled)
        self.prevAction.setEnabled(enabled)
        self.playAction.setEnabled(enabled)
        self.spboxStep.setEnabled(enabled)
        self.spBoxTimmer.setEnabled(enabled)


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
                                         symbolSize=3,
                                         pen=pyqtgraph.mkPen(self.ui.dck_model_param_properties.colors[i],
                                         width=self.ui.dck_model_param_properties.pen_size[i]))

    def play_stop(self):
        if not self.timer.isActive():
            self.timer.start(int(self.spBoxTimmer.value()))
            self.playAction.setIcon(QtGui.QIcon('View/img/pause.png'))
        else:
            self.timer.stop()
            self.playAction.setIcon(QtGui.QIcon('View/img/play.png'))

    def next_frame(self):
        self.controller.handler_update_graph()

    def restart_graph(self):
        self.playAction.setIcon(QtGui.QIcon('View/img/play.png'))
        self.controller.handler_restart_graph()

    def prev_frame(self):
        #TODO: todo
        pass


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
            self.controller.handler_edf(name)


        #file = open(name, 'w')
        #text = self.textEdit.toPlainText()
        #file.write(text)
        #file.close()

    def open_model(self):
        myFilter = ["XML file (*.xml)"]
        name, _ = QFileDialog.getOpenFileName(self, 'Open XML SERVOGLU model...',"","XML file (*.xml)", options=QFileDialog.DontUseNativeDialog)
        if name != "":
            if name.endswith(".xml"):
                try:
                    self.controller.handler_open_model(name)
                except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()
