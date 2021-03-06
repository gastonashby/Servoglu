import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import collections
import numpy
from Controller import PdfWriter as pdf
import locale
import datetime
#python -m PyQt5.uic.pyuic -x prueba.ui -o prueba.py

class ChildDlg(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.parent = parent

        self.setObjectName("PDFdialog")
        self.resize(553, 579)
        self.setToolTipDuration(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 450, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 471, 251))
        self.groupBox.setObjectName("groupBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 40, 141, 16))
        self.label_7.setObjectName("label_7")
        self.patientName = QtWidgets.QLineEdit(self.groupBox)
        self.patientName.setGeometry(QtCore.QRect(238, 40, 211, 20))
        self.patientName.setObjectName("patientName")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 241, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 221, 16))
        self.label_4.setObjectName("label_4")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 100, 241, 16))
        self.label_12.setObjectName("label_12")
        self.technicianName = QtWidgets.QLineEdit(self.groupBox)
        self.technicianName.setGeometry(QtCore.QRect(238, 100, 211, 20))
        self.technicianName.setObjectName("technicianName")
        self.simulationAdditionalInfo = QtWidgets.QTextEdit(self.groupBox)
        self.simulationAdditionalInfo.setGeometry(QtCore.QRect(238, 160, 211, 71))
        self.simulationAdditionalInfo.setObjectName("simulationAdditionalInfo")
        self.patientIdentifier = QtWidgets.QLineEdit(self.groupBox)
        self.patientIdentifier.setGeometry(QtCore.QRect(238, 70, 211, 20))
        self.patientIdentifier.setObjectName("patientIdentifier")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(10, 130, 241, 16))
        self.label_13.setObjectName("label_13")
        self.technicianIdentifier = QtWidgets.QLineEdit(self.groupBox)
        self.technicianIdentifier.setGeometry(QtCore.QRect(238, 130, 211, 20))
        self.technicianIdentifier.setObjectName("technicianIdentifier")
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 280, 471, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setEnabled(False)
        self.label_5.setGeometry(QtCore.QRect(200, 110, 141, 16))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setObjectName("label_5")
        self.plotWidth = QtWidgets.QSpinBox(self.groupBox_2)
        self.plotWidth.setEnabled(False)
        self.plotWidth.setGeometry(QtCore.QRect(350, 100, 42, 31))
        self.plotWidth.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.plotWidth.setMinimum(1)
        self.plotWidth.setMaximum(10)
        self.plotWidth.setProperty("value", 2)
        self.plotWidth.setObjectName("plotWidth")
        self.plotByPeriods = QtWidgets.QCheckBox(self.groupBox_2)
        self.plotByPeriods.setGeometry(QtCore.QRect(160, 110, 20, 20))
        self.plotByPeriods.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.plotByPeriods.setText("")
        self.plotByPeriods.setChecked(False)
        self.plotByPeriods.setObjectName("plotByPeriods")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(20, 110, 141, 16))
        self.label_11.setObjectName("label_11")
        self.displayAlarm = QtWidgets.QCheckBox(self.groupBox_2)
        self.displayAlarm.setGeometry(QtCore.QRect(160, 70, 20, 20))
        self.displayAlarm.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.displayAlarm.setText("")
        self.displayAlarm.setChecked(True)
        self.displayAlarm.setObjectName("displayAlarm")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 70, 141, 16))
        self.label_10.setObjectName("label_10")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setGeometry(QtCore.QRect(168, 30, 81, 16))
        self.label_15.setObjectName("label_15")
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(220, 510, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.groupBox.raise_()
        self.buttonBox.raise_()
        self.groupBox_2.raise_()
        self.progressBar.raise_()

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.plotByPeriods.stateChanged.connect(self.plotByPeriodsEvent)
        QtCore.QMetaObject.connectSlotsByName(self)


        self.progressBar.setVisible(False)

        self.setTabOrder(self.patientName, self.patientIdentifier)
        self.setTabOrder(self.patientIdentifier, self.technicianName)
        self.setTabOrder(self.technicianName, self.technicianIdentifier)

    def retranslateUi(self, PDFdialog):
        try:
            _translate = QtCore.QCoreApplication.translate
            languageHash = self.parent.controller.languageSupport.languageHash
            self.setWindowTitle(_translate("PDFdialog", languageHash.__getitem__("lbl.PDFproperties")))
            locale.setlocale(locale.LC_TIME, '')
            format = '%Y/%m/%d %H:%M:%S'
            date = datetime.datetime.now().strftime(format)
            self.groupBox.setTitle(_translate("PDFdialog",languageHash.__getitem__("lbl.ExportInformation") + " - " + date))
            self.label_7.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.PatientName")))
            self.label_3.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.PatientIdentifier")))
            self.label_4.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.SimultationAdditionalInfo")))
            self.label_12.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.TechnicianName")))
            self.label_13.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.TechnicianIdentifier")))
            self.groupBox_2.setTitle(_translate("PDFdialog", languageHash.__getitem__("lbl.PlotConfig")))
            self.label_5.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.NumberOfPeriods")))
            self.label_10.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.DisplayAlarms")))
            self.label_11.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.PlotByPeriods")))
            self.label_14.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.SimulatedTime")))
            self.label_15.setText(_translate("PDFdialog", str(self.parent.indexGr) + " " + self.parent.controller.model._timeUnit))
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def plotByPeriodsEvent(self):
        if self.plotByPeriods.isChecked():
            self.label_5.setEnabled(True)
            self.plotWidth.setEnabled(True)
        else:
            self.label_5.setEnabled(False)
            self.plotWidth.setEnabled(False)


    def closeEvent(self, event):
        print("X is clicked")

    def accept(self):
        try:
                myFilter = ["PDF file (*.pdf)"]
                name, _ = QFileDialog.getSaveFileName(self, 'Save PDF as',"","PDF file (*.pdf)", options=QFileDialog.DontUseNativeDialog)
                if name != "":
                    self.groupBox.setEnabled(False)
                    self.groupBox_2.setEnabled(False)
                    self.buttonBox.setEnabled(False)


                    self.progressBar.setVisible(True)
                    self.progressBar.setValue(50)
                    if not name.endswith(".pdf"):
                        name = name + ".pdf"
                    Pdf = collections.namedtuple('Pdf',['patientName', 'patientIdentifier', 'technicianName',
                                                   'technicianIdentifier','simulationAdditionalInfo','plotByPeriods',
                                                    'periods','plotsPerPage','displayAlarm','modelInfo','timeUnit',
                                                     'simulatedTime','templateFile','fileName'])
                    pdfTuple = Pdf(self.patientName.text(),
                          self.patientIdentifier.text(),
                          self.technicianName.text(),
                          self.technicianIdentifier.text(),
                          self.simulationAdditionalInfo.toPlainText(),
                          self.plotByPeriods.isChecked(),
                          int(self.plotWidth.text()),
                          4,
                          self.displayAlarm.isChecked(),
                          self.parent.controller.model._modelName,
                          self.parent.controller.model._timeUnit,
                          str(self.parent.indexGr),
                          self.parent.controller.model._template,
                          name)


                    size = self.parent.indexGr + 1
                    results = numpy.asarray(numpy.transpose(self.parent.all_data))[:size, :]
                    self.simulated_eq = self.parent.simulated_eq  # Array of bool to indicate the simulated graph
                    self.simulated_tr = self.parent.simulated_tr

                    userDefinedParameters = self.parent.controller.model._u
                    userDefinedTreatment = self.parent.controller.model._t
                    equations = self.parent.controller.model._e
                    constants = self.parent.controller.model._c
                    xAxe = self.parent.xDataGraf[:size]

                    if (len(self.parent.treatment) > 0):
                        treatment = numpy.asarray(numpy.transpose(self.parent.treatment))[:size, :]
                    else:
                        treatment = []


                    pdf.createPdf(self.simulated_eq,self.simulated_tr, results, treatment,
                                  xAxe,equations,userDefinedTreatment, userDefinedParameters,
                                  constants, pdfTuple, self.parent.controller.languageSupport.languageHash)

                    self.progressBar.setValue(100)

                    languageHash = self.parent.controller.languageSupport.languageHash
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(languageHash.__getitem__("lbl.ExportSuccess"))
                    #msg.setInformativeText("Simulation exported succesfully")
                    msg.setWindowTitle(languageHash.__getitem__("lbl.ExportResult"))
                    msg.exec_()
                    self.close()


        except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    self.close()

    def getSimulatedTreatment(self, treatments,simulatedTreatment):
        d = collections.deque()
        i = 0
        for t in treatments:
            if simulatedTreatment[i]:
                d.append(t)
            i += 1
        return d

    def getSimulatedEquations(self, equations, simulatedEquations):
        d = collections.deque()
        i = 0
        for e in equations:
            if simulatedEquations[i]:
                d.append(e)
            i+=1
        return d