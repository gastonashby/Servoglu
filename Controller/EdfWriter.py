from __future__ import division, print_function, absolute_import
import sys
import os
import os.path
from libsbml import *
import xml.etree.ElementTree as ET
import numpy as np
import pyedflib
import os
import numpy as np

from scipy import signal
from scipy import interpolate
from datetime import datetime, date
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def Interpolate(DataSet,Frecuency):
    interpolateCoef = 1/Frecuency ##in case its 1/minute then interpolateCoef = 60
    X = np.linspace(0, DataSet.shape[1], DataSet.shape[1])
    Y = np.linspace(0, DataSet.shape[0], DataSet.shape[0])

    x, y = np.meshgrid(X, Y, sparse=True)

    f = interpolate.interp2d(x, y, DataSet, kind='linear')
    # use linspace so your new range also goes from 0 to 3, with 8 intervals
    Xnew = np.linspace(0, DataSet.shape[1], DataSet.shape[1])
    Ynew = np.linspace(0, DataSet.shape[0] , DataSet.shape[0]*interpolateCoef)
    interpolatedDataSet = f(Xnew, Ynew)
    return interpolatedDataSet

def WriteEDF(DataSet,Equations,Frecuency,FileName,edf):
    test_data_file = os.path.join('.', FileName)
    numberOfColumns = DataSet.shape[1]
    numberOfRows = DataSet.shape[0]

    if Frecuency < 1:
        sampleRate = 1
        try:
            DataSet = Interpolate(DataSet,Frecuency)
        except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()
    else:
        sampleRate = Frecuency

    f = pyedflib.EdfWriter(test_data_file,numberOfColumns, file_type=pyedflib.FILETYPE_EDFPLUS)
    channel_info = []
    data_list = []
    _i = 0
    for ec in Equations:
        if ec.simulate:
            ch_dict = {'label': ec.name, 'dimension': ec.unit, 'sample_rate': sampleRate, 'physical_max': np.amax(DataSet[:,_i]),
                       'physical_min': np.amin(DataSet[:,_i]),
                       'digital_max': np.amax(DataSet[:,_i]), 'digital_min': np.amin(DataSet[:,_i]), 'transducer': '', 'prefilter': ''}
            channel_info.append(ch_dict)
            data_list.append(DataSet[:,_i])
            _i = _i + 1
    # Edf = collections.namedtuple('Edf', ['subjectCode', 'subjectName', 'sex', 'birthdate',
    #                                      'patientAdditionalInfo', 'adminCode', 'technician',
    #                                      'device', 'adminAdditionalInfo', 'start', 'duration'])
    f.setSignalHeaders(channel_info)
    f.setPatientCode(edf.subjectCode)
    f.setPatientName(edf.subjectName)
    f.setGender(edf.sex)
    y,m,d = edf.birthdate.split(".")
    #f.setBirthdate(date(int(y),int(m),int(d)))
    f.setPatientAdditional(edf.patientAdditionalInfo)
    f.setAdmincode(edf.adminCode)
    f.setTechnician(edf.technician)
    f.setEquipment(edf.device)
    f.setRecordingAdditional(edf.adminAdditionalInfo)

    #f.setStartdatetime(date.today())
    #f.setSamplefrequency()
    #f.setDatarecordDuration(10.0)
    f.writeSamples(data_list)
    f.writeAnnotation(0, -1, "Simulation Starts")
    f.writeAnnotation(DataSet.shape[0], -1, "Simulation Ends")
    f.close()
    del f

