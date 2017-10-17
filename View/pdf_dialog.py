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
#python -m PyQt5.uic.pyuic -x prueba.ui -o prueba.py

class ChildDlg(QDialog):
    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.parent = parent
        self.setObjectName("PDFdialog")
        self.resize(523, 474)
        self.setToolTipDuration(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(140, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(40, 40, 441, 341))
        self.groupBox.setObjectName("groupBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.label_7.setObjectName("label_7")
        self.subjectNameInput = QtWidgets.QLineEdit(self.groupBox)
        self.subjectNameInput.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.subjectNameInput.setObjectName("subjectNameInput")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 91, 16))
        self.label_2.setObjectName("label_2")
        self.SexInput = QtWidgets.QLineEdit(self.groupBox)
        self.SexInput.setGeometry(QtCore.QRect(100, 60, 113, 20))
        self.SexInput.setObjectName("SexInput")
        self.patientAdditionalInfoInput = QtWidgets.QLineEdit(self.groupBox)
        self.patientAdditionalInfoInput.setGeometry(QtCore.QRect(170, 100, 231, 41))
        self.patientAdditionalInfoInput.setObjectName("patientAdditionalInfoInput")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(230, 30, 91, 16))
        self.label_8.setObjectName("label_8")
        self.birthdateInput = QtWidgets.QDateEdit(self.groupBox)
        self.birthdateInput.setGeometry(QtCore.QRect(290, 30, 110, 22))
        self.birthdateInput.setObjectName("birthdateInput")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 220, 161, 16))
        self.label_4.setObjectName("label_4")
        self.recordingAdditionalInfoInput = QtWidgets.QLineEdit(self.groupBox)
        self.recordingAdditionalInfoInput.setGeometry(QtCore.QRect(170, 210, 231, 41))
        self.recordingAdditionalInfoInput.setObjectName("recordingAdditionalInfoInput")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(50, 160, 111, 16))
        self.label_12.setObjectName("label_12")
        self.technicianInput = QtWidgets.QLineEdit(self.groupBox)
        self.technicianInput.setGeometry(QtCore.QRect(170, 160, 111, 20))
        self.technicianInput.setObjectName("technicianInput")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(70, 300, 131, 16))
        self.label_5.setObjectName("label_5")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(170, 300, 42, 22))
        self.spinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)
        self.spinBox.setObjectName("spinBox")
        self.groupBox.raise_()
        self.buttonBox.raise_()

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, EDFdialog):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PDFdialog", "PDF - Properties"))
        self.groupBox.setTitle(_translate("PDFdialog", "PDF export information"))
        self.label_7.setText(_translate("PDFdialog", "Patient name:"))
        self.label_2.setText(_translate("PDFdialog", "Sex:"))
        self.label_8.setText(_translate("PDFdialog", "Birthdate:"))
        self.label_3.setText(_translate("PDFdialog", "Additional patient info:"))
        self.label_4.setText(_translate("PDFdialog", "Additional simulation info:"))
        self.label_12.setText(_translate("PDFdialog", "Technician name:"))
        self.label_5.setText(_translate("PDFdialog", "Plots per page:"))

    def closeEvent(self, event):
        print("X is clicked")

    def accept(self):
        try:
                myFilter = ["PDF file (*.pdf)"]
                name, _ = QFileDialog.getSaveFileName(self, 'Save PDF as',"","PDF file (*.pdf)", options=QFileDialog.DontUseNativeDialog)
                if name != "":
                    if not name.endswith(".pdf"):
                        name = name + ".pdf"
                    Pdf = collections.namedtuple('Pdf',['patientName', 'sex', 'birthdate',
                                                   'patientAdditionalInfo', 'technician',
                                                   'simulationInfo','modelInfo'])
                    pdfTuple = Pdf(self.subjectNameInput.text(),
                          self.SexInput.text(),
                          self.birthdateInput.text(),
                          self.patientAdditionalInfoInput.text(),
                          self.technicianInput.text(),
                          self.recordingAdditionalInfoInput.text(),
                          self.parent.controller.model.simulatedModel.name)

                    size = self.parent.indexGr
                    results = numpy.asarray(numpy.transpose(self.parent.all_data))[:size, :]
                    xAxe = self.parent.xDataGraf[:size]
                    pdf.createPdf(results, xAxe, size, self.parent.controller.model._e,name,pdfTuple,int(self.spinBox.text()))

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