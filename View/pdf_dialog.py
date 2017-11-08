import sys
import Controller.EdfWriter as edf
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import collections
import numpy
from Controller import PdfWriter as pdf
#python -m PyQt5.uic.pyuic -x prueba.ui -o prueba.py

class ChildDlg(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.parent = parent

        self.setObjectName("PDFdialog")
        self.resize(679, 749)
        self.setToolTipDuration(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(100, 620, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 601, 381))
        self.groupBox.setObjectName("groupBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 40, 141, 16))
        self.label_7.setObjectName("label_7")
        self.subjectNameInput = QtWidgets.QLineEdit(self.groupBox)
        self.subjectNameInput.setGeometry(QtCore.QRect(260, 40, 211, 20))
        self.subjectNameInput.setObjectName("subjectNameInput")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 141, 16))
        self.label_2.setObjectName("label_2")
        self.SexInput = QtWidgets.QLineEdit(self.groupBox)
        self.SexInput.setGeometry(QtCore.QRect(260, 120, 211, 20))
        self.SexInput.setObjectName("SexInput")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(10, 80, 141, 16))
        self.label_8.setObjectName("label_8")
        self.birthdateInput = QtWidgets.QDateEdit(self.groupBox)
        self.birthdateInput.setGeometry(QtCore.QRect(260, 80, 211, 22))
        self.birthdateInput.setObjectName("birthdateInput")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 160, 241, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 300, 241, 16))
        self.label_4.setObjectName("label_4")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 250, 171, 16))
        self.label_12.setObjectName("label_12")
        self.technicianInput = QtWidgets.QLineEdit(self.groupBox)
        self.technicianInput.setGeometry(QtCore.QRect(260, 250, 211, 20))
        self.technicianInput.setObjectName("technicianInput")
        self.recordingAdditionalInfoInput = QtWidgets.QTextEdit(self.groupBox)
        self.recordingAdditionalInfoInput.setGeometry(QtCore.QRect(260, 290, 211, 71))
        self.recordingAdditionalInfoInput.setObjectName("recordingAdditionalInfoInput")
        self.patientAdditionalInfoInput = QtWidgets.QTextEdit(self.groupBox)
        self.patientAdditionalInfoInput.setGeometry(QtCore.QRect(260, 160, 211, 71))
        self.patientAdditionalInfoInput.setObjectName("patientAdditionalInfoInput")
        self.label_7.raise_()
        self.subjectNameInput.raise_()
        self.label_2.raise_()
        self.SexInput.raise_()
        self.label_8.raise_()
        self.birthdateInput.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_12.raise_()
        self.technicianInput.raise_()
        self.recordingAdditionalInfoInput.raise_()
        self.patientAdditionalInfoInput.raise_()
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(39, 419, 601, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(310, 30, 131, 16))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 131, 16))
        self.label_5.setObjectName("label_5")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox.setGeometry(QtCore.QRect(260, 20, 42, 41))
        self.spinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_2.setGeometry(QtCore.QRect(260, 70, 42, 41))
        self.spinBox_2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 80, 221, 16))
        self.label_10.setObjectName("label_10")
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(290, 700, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.groupBox.raise_()
        self.buttonBox.raise_()
        self.groupBox_2.raise_()
        self.progressBar.raise_()

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)


        self.progressBar.setVisible(False)

        # self.setTabOrder(self.textboxA, self.textboxB)
        # self.setTabOrder(self.textboxB, self.textboxC)
        # self.setTabOrder(self.textboxC, self.textboxD)

    def retranslateUi(self, EDFdialog):
        _translate = QtCore.QCoreApplication.translate
        languageHash = self.parent.controller.languageSupport.languageHash

        self.setWindowTitle(_translate("PDFdialog", languageHash.__getitem__("lbl.PDFproperties")))
        self.groupBox.setTitle(_translate("PDFdialog",languageHash.__getitem__("lbl.ExportInformation")))
        self.label_7.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.PatientName")))
        self.label_2.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.Sex")))
        self.label_8.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.BirthDate")))
        self.birthdateInput.setDisplayFormat(_translate("PDFdialog", "d/M/yyyy"))
        self.label_3.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.AddPatienceInfo")))
        self.label_4.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.AddSimInfo")))
        self.label_12.setText(_translate("PDFdialog",languageHash.__getitem__("lbl.TecName")))
        self.groupBox_2.setTitle(_translate("PDFdialog", languageHash.__getitem__("lbl.PlotConfiguration")))
        self.label_6.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.Sections")))
        self.label_5.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.DividePlotInto")))
        self.label_10.setText(_translate("PDFdialog", languageHash.__getitem__("lbl.NumberOfPlots")))


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
                    Pdf = collections.namedtuple('Pdf',['patientName', 'sex', 'birthdate',
                                                   'patientAdditionalInfo', 'technician',
                                                   'simulationInfo','modelInfo'])
                    pdfTuple = Pdf(self.subjectNameInput.text(),
                          self.SexInput.text(),
                          self.birthdateInput.text(),
                          self.patientAdditionalInfoInput.toPlainText(),
                          self.technicianInput.text(),
                          self.recordingAdditionalInfoInput.toPlainText(),
                          self.parent.controller.model._modelName)


                    size = self.parent.indexGr + 1
                    results = numpy.asarray(numpy.transpose(self.parent.all_data))[:size, :]
                    self.simulated_eq = self.parent.simulated_eq  # Array of bool to indicate the simulated graph
                    self.simulated_tr = self.parent.simulated_tr
                    userDefinedTreatment = self.getSimulatedTreatment(self.parent.controller.model._t,self.simulated_tr)
                    equations = self.getSimulatedEquations(self.parent.controller.model._e,self.simulated_eq)
                    timeUnit = self.parent.controller.model._timeUnit

                    constants = self.parent.controller.model._c
                    templateFile = self.parent.controller.model._template
                    xAxe = self.parent.xDataGraf[:size]

                    if (len(self.parent.treatment) > 0):
                        treatment = numpy.asarray(numpy.transpose(self.parent.treatment))[:size, :]
                    else:
                        treatment = []
                    sections = int(self.spinBox.text())
                    plotsPerPage =  int(self.spinBox_2.text())

                    pdf.createPdf(results, treatment, xAxe, size, equations,userDefinedTreatment,
                                  constants,name,pdfTuple,sections,plotsPerPage,timeUnit,templateFile)

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