__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

import pyqtgraph
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
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
        #myFilter = ["EDF file (*.edf)"]
        #name, _ = QFileDialog.getSaveFileName(self, 'Save EDF as',"","EDF file (*.edf)", options=QFileDialog.DontUseNativeDialog)
        #if name != "":
        #    if not name.endswith(".edf"):
        #        name = name + ".edf"
        #    self.controller.handler_edf(name)
        #pyuic5 prueba.ui -o dialog.py
        EDFdialog = QtWidgets.QDialog()
        EDFdialog.setObjectName("EDFdialog")
        EDFdialog.resize(481, 555)
        EDFdialog.setToolTipDuration(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(EDFdialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 490, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.subjectCodeInput = QtWidgets.QLineEdit(EDFdialog)
        self.subjectCodeInput.setGeometry(QtCore.QRect(110, 70, 113, 20))
        self.subjectCodeInput.setObjectName("subjectCodeInput")
        self.label = QtWidgets.QLabel(EDFdialog)
        self.label.setGeometry(QtCore.QRect(30, 70, 91, 16))
        self.label.setObjectName("label")
        self.SexInput = QtWidgets.QLineEdit(EDFdialog)
        self.SexInput.setGeometry(QtCore.QRect(110, 110, 113, 20))
        self.SexInput.setObjectName("SexInput")
        self.label_2 = QtWidgets.QLabel(EDFdialog)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 91, 16))
        self.label_2.setObjectName("label_2")
        self.patientAdditionalInfoInput = QtWidgets.QLineEdit(EDFdialog)
        self.patientAdditionalInfoInput.setGeometry(QtCore.QRect(110, 150, 341, 20))
        self.patientAdditionalInfoInput.setObjectName("patientAdditionalInfoInput")
        self.label_3 = QtWidgets.QLabel(EDFdialog)
        self.label_3.setGeometry(QtCore.QRect(30, 150, 91, 16))
        self.label_3.setObjectName("label_3")
        self.subjectNameInput = QtWidgets.QLineEdit(EDFdialog)
        self.subjectNameInput.setGeometry(QtCore.QRect(340, 70, 113, 20))
        self.subjectNameInput.setObjectName("subjectNameInput")
        self.label_7 = QtWidgets.QLabel(EDFdialog)
        self.label_7.setGeometry(QtCore.QRect(260, 70, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(EDFdialog)
        self.label_8.setGeometry(QtCore.QRect(260, 110, 91, 16))
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(EDFdialog)
        self.label_4.setGeometry(QtCore.QRect(30, 330, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(EDFdialog)
        self.label_5.setGeometry(QtCore.QRect(30, 290, 91, 16))
        self.label_5.setObjectName("label_5")
        self.technicianInput = QtWidgets.QLineEdit(EDFdialog)
        self.technicianInput.setGeometry(QtCore.QRect(340, 250, 113, 20))
        self.technicianInput.setObjectName("technicianInput")
        self.adminCodeInput = QtWidgets.QLineEdit(EDFdialog)
        self.adminCodeInput.setGeometry(QtCore.QRect(110, 250, 113, 20))
        self.adminCodeInput.setObjectName("adminCodeInput")
        self.label_6 = QtWidgets.QLabel(EDFdialog)
        self.label_6.setGeometry(QtCore.QRect(30, 250, 91, 16))
        self.label_6.setObjectName("label_6")
        self.recordingAdditionalInfoInput = QtWidgets.QLineEdit(EDFdialog)
        self.recordingAdditionalInfoInput.setGeometry(QtCore.QRect(110, 330, 341, 20))
        self.recordingAdditionalInfoInput.setObjectName("recordingAdditionalInfoInput")
        self.label_12 = QtWidgets.QLabel(EDFdialog)
        self.label_12.setGeometry(QtCore.QRect(260, 250, 91, 16))
        self.label_12.setObjectName("label_12")
        self.deviceInput = QtWidgets.QLineEdit(EDFdialog)
        self.deviceInput.setGeometry(QtCore.QRect(110, 290, 113, 20))
        self.deviceInput.setObjectName("deviceInput")
        self.birthdateInput = QtWidgets.QDateEdit(EDFdialog)
        self.birthdateInput.setGeometry(QtCore.QRect(340, 110, 110, 22))
        self.birthdateInput.setObjectName("birthdateInput")
        self.groupBox = QtWidgets.QGroupBox(EDFdialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 40, 441, 151))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(EDFdialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 220, 441, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(EDFdialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 400, 441, 81))
        self.groupBox_3.setObjectName("groupBox_3")
        self.durationInput = QtWidgets.QLineEdit(self.groupBox_3)
        self.durationInput.setGeometry(QtCore.QRect(320, 30, 113, 20))
        self.durationInput.setObjectName("durationInput")
        self.simulationStartInput = QtWidgets.QDateTimeEdit(self.groupBox_3)
        self.simulationStartInput.setGeometry(QtCore.QRect(90, 30, 121, 22))
        self.simulationStartInput.setObjectName("simulationStartInput")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.label_14.setObjectName("label_14")
        self.label_16 = QtWidgets.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(240, 30, 91, 16))
        self.label_16.setObjectName("label_16")
        self.groupBox_3.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.buttonBox.raise_()
        self.subjectCodeInput.raise_()
        self.label.raise_()
        self.SexInput.raise_()
        self.label_2.raise_()
        self.patientAdditionalInfoInput.raise_()
        self.label_3.raise_()
        self.subjectNameInput.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.technicianInput.raise_()
        self.adminCodeInput.raise_()
        self.label_6.raise_()
        self.recordingAdditionalInfoInput.raise_()
        self.label_12.raise_()
        self.deviceInput.raise_()
        self.birthdateInput.raise_()

        self.retranslateUi(EDFdialog)
        self.buttonBox.accepted.connect(EDFdialog.accept)
        self.buttonBox.rejected.connect(EDFdialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EDFdialog)

        EDFdialog.show()
        sys.exit(EDFdialog.exec_())

    def retranslateUi(self, EDFdialog):
        _translate = QtCore.QCoreApplication.translate
        EDFdialog.setWindowTitle(_translate("EDFdialog", "EDF - Properties"))
        self.label.setText(_translate("EDFdialog", "Subject code:"))
        self.label_2.setText(_translate("EDFdialog", "Sex:"))
        self.label_3.setText(_translate("EDFdialog", "Additional info:"))
        self.label_7.setText(_translate("EDFdialog", "Subject name:"))
        self.label_8.setText(_translate("EDFdialog", "Birthdate:"))
        self.label_4.setText(_translate("EDFdialog", "Additional info:"))
        self.label_5.setText(_translate("EDFdialog", "Device:"))
        self.label_6.setText(_translate("EDFdialog", "Admin code:"))
        self.label_12.setText(_translate("EDFdialog", "Technician:"))
        self.label_14.setText(_translate("EDFdialog", "Start:"))
        self.label_16.setText(_translate("EDFdialog", "Duration:"))
        self.groupBox.setTitle(_translate("EDFdialog", "Local patient identification"))
        self.groupBox_2.setTitle(_translate("EDFdialog", "Local recording identification"))
        self.groupBox_3.setTitle(_translate("EDFdialog", "Simulation info"))



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
