from __future__ import division, print_function, absolute_import
import sys
import os
import os.path
from libsbml import *
import xml.etree.ElementTree as ET
import ParsingMathML as mp
import numpy as np
import pyedflib
from DefineFunction import *
import os
import numpy as np
from scipy import signal
from scipy import interpolate

def Interpolate(DataSet):
    X = np.linspace(0, 4, 4)
    Y = np.linspace(0, 10000, 10000)

    x, y = np.meshgrid(X, Y, sparse=True)

    f = interpolate.interp2d(x, y, DataSet, kind='linear')
    # use linspace so your new range also goes from 0 to 3, with 8 intervals
    Xnew = np.linspace(0, 4, 4)
    Ynew = np.linspace(0, 10000*60, 10000*60)
    test8x8 = f(Xnew, Ynew)

    print(DataSet.shape)
    print(test8x8.shape)

    return test8x8

def WriteEDF(DataSet,Equations):
    test_data_file = os.path.join('.', 'test_generator2.edf')
    numberOfColumns = DataSet.shape[1]

    DataSet = Interpolate(DataSet)
    numberOfRows = DataSet.shape[0]
    f = pyedflib.EdfWriter(test_data_file,numberOfColumns, file_type=pyedflib.FILETYPE_EDFPLUS)
    channel_info = []
    data_list = []
    _i = 0
    for ec in Equations:
        if ec.simulate:
            ch_dict = {'label': ec.name, 'dimension': ec.unit, 'sample_rate': 1, 'physical_max': np.amax(DataSet[:,_i]),
                       'physical_min': np.amin(DataSet[:,_i]),
                       'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter': ''}
            channel_info.append(ch_dict)
            #time = np.linspace(0, file_duration, file_duration * 200)
            #xtemp = np.sin(2 * np.pi * 0.1 * time)
            #x1 = xtemp.copy()
            #x1[np.where(xtemp > 0)[0]] = 100
            #x1[np.where(xtemp < 0)[0]] = -100
            data_list.append(DataSet[:,_i])
            _i = _i + 1

    f.setSignalHeaders(channel_info)
    f.writeSamples(data_list)
    f.writeAnnotation(0, -1, "Recording starts")
    #f.writeAnnotation(298, -1, "Test 1")
    #f.writeAnnotation(294.99, -1, "pulse 1")
    #f.writeAnnotation(295.9921875, -1, "pulse 2")
    #f.writeAnnotation(296.99078341013825, -1, "pulse 3")
    f.writeAnnotation(numberOfRows*60, -1, "Recording ends")
    f.close()
    del f

