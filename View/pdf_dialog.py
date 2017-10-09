import sys
import Controller.EdfWriter as edf
import Model.Plot2 as plt2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import collections
import numpy
from Controller import PdfWriter as pdf

class ChildDlg(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.parent = parent
        self.setObjectName("EDFdialog")
        self.resize(481, 555)
        self.setToolTipDuration(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(110, 490, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.subjectCodeInput = QtWidgets.QLineEdit(self)
        self.subjectCodeInput.setGeometry(QtCore.QRect(110, 70, 113, 20))
        self.subjectCodeInput.setObjectName("subjectCodeInput")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 70, 91, 16))
        self.label.setObjectName("label")
        self.SexInput = QtWidgets.QLineEdit(self)
        self.SexInput.setGeometry(QtCore.QRect(110, 110, 113, 20))
        self.SexInput.setObjectName("SexInput")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 91, 16))
        self.label_2.setObjectName("label_2")
        self.patientAdditionalInfoInput = QtWidgets.QLineEdit(self)
        self.patientAdditionalInfoInput.setGeometry(QtCore.QRect(110, 150, 341, 20))
        self.patientAdditionalInfoInput.setObjectName("patientAdditionalInfoInput")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(30, 150, 91, 16))
        self.label_3.setObjectName("label_3")
        self.subjectNameInput = QtWidgets.QLineEdit(self)
        self.subjectNameInput.setGeometry(QtCore.QRect(340, 70, 113, 20))
        self.subjectNameInput.setObjectName("subjectNameInput")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(260, 70, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(260, 110, 91, 16))
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(30, 330, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(30, 290, 91, 16))
        self.label_5.setObjectName("label_5")
        self.technicianInput = QtWidgets.QLineEdit(self)
        self.technicianInput.setGeometry(QtCore.QRect(340, 250, 113, 20))
        self.technicianInput.setObjectName("technicianInput")
        self.adminCodeInput = QtWidgets.QLineEdit(self)
        self.adminCodeInput.setGeometry(QtCore.QRect(110, 250, 113, 20))
        self.adminCodeInput.setObjectName("adminCodeInput")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(30, 250, 91, 16))
        self.label_6.setObjectName("label_6")
        self.recordingAdditionalInfoInput = QtWidgets.QLineEdit(self)
        self.recordingAdditionalInfoInput.setGeometry(QtCore.QRect(110, 330, 341, 20))
        self.recordingAdditionalInfoInput.setObjectName("recordingAdditionalInfoInput")
        self.label_12 = QtWidgets.QLabel(self)
        self.label_12.setGeometry(QtCore.QRect(260, 250, 91, 16))
        self.label_12.setObjectName("label_12")
        self.deviceInput = QtWidgets.QLineEdit(self)
        self.deviceInput.setGeometry(QtCore.QRect(110, 290, 113, 20))
        self.deviceInput.setObjectName("deviceInput")
        self.birthdateInput = QtWidgets.QDateEdit(self)
        self.birthdateInput.setDisplayFormat("dd.MM.yyyy")
        self.birthdateInput.setGeometry(QtCore.QRect(340, 110, 110, 22))
        self.birthdateInput.setObjectName("birthdateInput")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(20, 40, 441, 151))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 220, 441, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self)
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
        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

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

    def closeEvent(self, event):
        print("X is clicked")

    def accept(self):
        try:
                myFilter = ["PDF file (*.pdf)"]
                name, _ = QFileDialog.getSaveFileName(self, 'Save PDF as',"","PDF file (*.pdf)", options=QFileDialog.DontUseNativeDialog)
                if name != "":
                    if not name.endswith(".pdf"):
                        name = name + ".pdf"
                    Edf = collections.namedtuple('Pdf',['subjectCode', 'subjectName', 'sex', 'birthdate',
                                                   'patientAdditionalInfo', 'adminCode', 'technician',
                                                   'device', 'adminAdditionalInfo','start','duration'])
                    pdfTuple = Edf(self.subjectCodeInput.text(),self.subjectNameInput.text(),self.SexInput.text(),
                          self.birthdateInput.text(),
                          self.patientAdditionalInfoInput.text(),
                          self.adminCodeInput.text(),
                          self.technicianInput.text(),
                          self.deviceInput.text(),
                          self.recordingAdditionalInfoInput.text(),
                          self.simulationStartInput.text(),
                          self.durationInput.text())

                    size = self.parent.indexGr
                    results = numpy.asarray(numpy.transpose(self.parent.all_data))[:size, :]
                    xAxe = self.parent.xDataGraf[:size]
                    pdf.createPdf(results, xAxe, size, self.parent.controller.model._e,name,pdfTuple)

        except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()

    # def  accept(self):
    #     try:
    #         myFilter = ["EDF file (*.pdf)"]
    #         name, _ = QFileDialog.getSaveFileName(self, 'Save PDF as',"","PDF file (*.pdf)", options=QFileDialog.DontUseNativeDialog)
    #         if name != "":
    #             if not name.endswith(".pdf"):
    #                 name = name + ".pdf"
    #             Edf = collections.namedtuple('Pdf',['subjectCode', 'subjectName', 'sex', 'birthdate',
    #                                            'patientAdditionalInfo', 'adminCode', 'technician',
    #                                            'device', 'adminAdditionalInfo','start','duration'])
    #             edfTuple = Edf(self.subjectCodeInput.text(),self.subjectNameInput.text(),self.SexInput.text(),
    #                   self.birthdateInput.text(),
    #                   self.patientAdditionalInfoInput.text(),
    #                   self.adminCodeInput.text(),
    #                   self.technicianInput.text(),
    #                   self.deviceInput.text(),
    #                   self.recordingAdditionalInfoInput.text(),
    #                   self.simulationStartInput.text(),
    #                   self.durationInput.text())
    #
    #             edf.WriteEDF(numpy.asarray(numpy.transpose(self.parent.all_data))[:self.parent.indexGr,:],
    #                          self.parent.controller.model._e,
    #                          eval(self.parent.controller.model.simulatedModel.simulationFrequency), name, edfTuple)
    #     except Exception as e:
    #                 print(e)
    #                 msg = QMessageBox()
    #                 msg.setIcon(QMessageBox.Critical)
    #                 msg.setText("Error")
    #                 msg.setInformativeText(str(e))
    #                 msg.setWindowTitle("Error")
    #                 msg.exec_()