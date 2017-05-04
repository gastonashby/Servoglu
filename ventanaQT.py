# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtCore, QtGui
#from PyQt5.QtWidgets import QSlider

import pyqtgraph as pg

from pyqtgraph.parametertree import Parameter, ParameterTree

import Plot2 as plt2

####### Variables #######

#_slider = QSlider()
#_slider.setOrientation(QtCore.Vertical)

_app = QtGui.QApplication([])
_w = QtGui.QWidget()

# Layout
_layout = QtGui.QGridLayout()
_w.setLayout(_layout)

# Components
_btnPlayStop = QtGui.QPushButton('Play')
_btnNext = QtGui.QPushButton('Next')
_btnReset = QtGui.QPushButton('Reset')

_listw = QtGui.QListWidget()
_plot = pg.PlotWidget()

_init_timmer = 200

_params = []
_listChildAuxConst = []

_chunkSize = 50

_plot.setLabel('bottom', 'Time', 's')
_plot.showGrid(x=True, y=True)
# plot.setXRange(0, chunkSize)
#plot.setYRange(0, 30)

_all_data = []
_all_curves = []

def definite_graph():
    global _all_data, _all_curves
    _i = 0
    for eq in plt2._e:
        # print(eq.simulate)
        if eq.simulate:
            _all_data.append([plt2.obtener(0)[_i]])
            _all_curves.append(_plot.plot(plt2._xdata, pen=(255,0,0)))
        _i += 1

definite_graph()

_indexGr = 1

# Tree params
_listChildUsrDef = []
for userDef in plt2._u:
    #nomC = const.value1 + ' ' + const.operator
    _childAuxUsrDef = {'name': userDef.name, 'type': userDef.type, 'value': userDef.defaultValue, 'readonly': False, 'title': userDef.description,  'suffix': userDef.unit,  'siPrefix': True}
    _listChildUsrDef.append(_childAuxUsrDef)
_paramAuxUsrDef = {'name': 'User Defined', 'type': 'group', 'children': _listChildUsrDef}
_params.append(_paramAuxUsrDef)

for const in plt2._c:
    nomC = const.value1
    #nomC = const.value1 + ' ' + const.operator
    _childAuxConst = {'name': nomC, 'type': 'str', 'value': const.value2, 'readonly': True}
    _listChildAuxConst.append(_childAuxConst)
_paramAuxConst = {'name': 'Constantes', 'type': 'group', 'children': _listChildAuxConst}
_params.append(_paramAuxConst)

_listChildAuxEq = []
for const in plt2._e:
    _childAuxEq = {'name': const.name, 'type': 'str', 'value': const.equation, 'readonly': True}
    _listChildAuxEq.append(_childAuxEq)
    #print(const)
_paramAux = {'name': 'Ecuaciones', 'type': 'group', 'children': _listChildAuxEq}
_params.append(_paramAux)

_listChildAuxFunc = []
for const in plt2._f:
    _childAuxFunc = {'name': const.name, 'type': 'str', 'value': const.function, 'siPrefix': False, 'readonly': True}
    _listChildAuxFunc.append(_childAuxFunc)
    #print(const)
_paramAux = {'name': 'Funciones', 'type': 'group', 'children': _listChildAuxFunc}
_params.append(_paramAux)

_listCommAuxFunc = []
_childAuxComm = {'name': "Timmer", 'type': 'int', 'value': _init_timmer, 'suffix': 'ms', 'readonly': False, 'limits': (100, 1000), 'step': 100}
_listCommAuxFunc.append(_childAuxComm)
_paramAux = {'name': 'Controles', 'type': 'group', 'children': _listCommAuxFunc}
_params.append(_paramAux)

## Create tree of Parameter objects
_pp = Parameter.create(name='params', type='group', children=_params)


## If anything changes in the tree, print a message
def change(param, changes):
    print("tree changes:")
    global _init_timmer, _indexGr
    for param, change, data in changes:
        path = _pp.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s' % childName)
        print('  change:    %s' % change)
        print('  data:      %s' % str(data))
        print('  ----------')
        par1, par2 = childName.split('.')
        if 'Constantes' in par1:
            print('recalculando ' + par2 + '...')
            exec("plt2." + par2 + ' = float(eval(data))')
            # plt2.r = float(data)
            plt2.recalculate(_indexGr)
            _indexGr = 1
            print('ok!')
        elif 'User Defined' in childName:
            print('recalculando con ' + par2 + ' = ' + str(data) + '...')
            exec("plt2." + par2 + ' = data')
            # plt2.r = float(data)
            plt2.recalculate(_indexGr)
            _indexGr = 1
            print('ok!')
        elif 'Timmer' in childName:
            print('Cambiando timmer...')
            _init_timmer = data
            _timer.stop()
            _timer.start(_init_timmer)
            print('ok!')


_pp.sigTreeStateChanged.connect(change)

# update all plots

def update1():
    global _indexGr, _all_curves, _all_data

    _dats = plt2.obtener(_indexGr)
    _i = 0
    _j = 0
    for eq in plt2._e:
        if eq.simulate:
            #print(dats[_j])
            _all_data[_i].append(_dats[_j])
            _all_curves[_i].setData(_all_data[_i])
            _i += 1
        _j += 1
    _indexGr += 1

    # if indexGr == 60:
    #     plt2.Ex = 80
    #     plt2.recalculate()
    # elif indexGr == 120:
    #     plt2.Ex = 55
    #     plt2.recalculate()
    #plot.setXRange(indexGr - 50, indexGr)
    #plot.setXRange(0, indexGr)


def play_stop():
    global _timer, _btnPlayStop, _btnNext, _childAuxComm
    if _btnPlayStop.text() == "Play":
        _timer.start(10)
        _btnPlayStop.setText("Stop")
        _btnNext.setEnabled(False)
        _childAuxComm["readonly"] = True
    else:
        _timer.stop()
        _btnPlayStop.setText("Play")
        _btnNext.setEnabled(True)
        _childAuxComm["readonly"] = False


def next_frame():
    update1()


def restart_graph():
    global _indexGr, _all_data, _all_curves, _timer, _btnPlayStop, _btnNext
    _indexGr = 0
    _dats = plt2.obtener(_indexGr)
    _i = 0
    _j = 0
    for eq in plt2._e:
        if eq.simulate:
            # print(dats[_j])
            _all_data[_i] = [_dats[_j]]
            _all_curves[_i].setData(_all_data[_i])
            _i += 1
        _j += 1
    _timer.stop()
    _btnPlayStop.setText("Play")
    _btnNext.setEnabled(True)



## Create two ParameterTree widgets, both accessing the same data
_t = ParameterTree()
_t.setParameters(_pp, showTop=False)

_timer = pg.QtCore.QTimer()
_timer.timeout.connect(update1)


_btnPlayStop.clicked.connect(play_stop)
_btnNext.clicked.connect(next_frame)
_btnReset.clicked.connect(restart_graph)

## Add widgets to the layout in their proper positions
_layout.addWidget(_btnPlayStop, 1, 0)   # text edit goes in middle-left
_layout.addWidget(_btnNext, 2, 0)   # text edit goes in middle-left
_layout.addWidget(_btnReset, 3, 0)   # text edit goes in middle-left
_layout.addWidget(_plot, 0, 1, 4, 1)  # plot goes on right side, spanning 3 rows
_layout.addWidget(_t, 0, 0)

## Display the widget as a new window
_w.show()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
