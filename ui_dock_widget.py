__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt5 import QtCore, QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree

# TODO: No importar Plot2, pasar por parametro
import Plot2 as plt2
# import local python scripts

class Ui_ControlsBoxDockWidget(QtCore.QObject):
    def createParams(self):
        # Tree params
        _listChildUsrDef = []
        _params = []
        _init_timmer = 200
        for userDef in plt2._u:
            # nomC = const.value1 + ' ' + const.operator
            _childAuxUsrDef = {'name': userDef.name, 'value': userDef.defaultValue, #'type': userDef.type,
                               'readonly': True,
                               'title': userDef.description, 'suffix': userDef.unit, 'siPrefix': True}
            _listChildUsrDef.append(_childAuxUsrDef)
        _paramAuxUsrDef = {'name': 'User Defined', 'type': 'group', 'children': _listChildUsrDef, 'expanded': False}
        _params.append(_paramAuxUsrDef)

        _listChildAuxConst = []
        for const in plt2._c:
            nomC = const.value1
            # nomC = const.value1 + ' ' + const.operator
            _childAuxConst = {'name': nomC, 'type': 'str', 'value': const.value2, 'readonly': True}
            _listChildAuxConst.append(_childAuxConst)
        _paramAuxConst = {'name': 'Constantes', 'type': 'group', 'children': _listChildAuxConst, 'expanded': False}
        _params.append(_paramAuxConst)

        _listChildAuxEq = []
        for const in plt2._e:
            _childAuxEq = {'name': const.name, 'type': 'str', 'value': const.equation, 'readonly': True}
            _listChildAuxEq.append(_childAuxEq)
            # print(const)
        _paramAux = {'name': 'Ecuaciones', 'type': 'group', 'children': _listChildAuxEq, 'expanded': False}
        _params.append(_paramAux)

        _listChildAuxFunc = []
        for const in plt2._f:
            _childAuxFunc = {'name': const.name, 'type': 'str', 'value': const.function, 'siPrefix': False,
                             'readonly': True}
            _listChildAuxFunc.append(_childAuxFunc)
            # print(const)
        _paramAux = {'name': 'Funciones', 'type': 'group', 'children': _listChildAuxFunc, 'expanded': False}
        _params.append(_paramAux)

        # _listCommAuxFunc = []
        # _childAuxComm = {'name': "Timmer", 'type': 'int', 'value': _init_timmer, 'suffix': 'ms', 'readonly': False,
        #                  'limits': (100, 1000), 'step': 100}
        # _listCommAuxFunc.append(_childAuxComm)
        # _paramAux = {'name': 'Controles', 'type': 'group', 'children': _listCommAuxFunc, 'expanded': False}
        # _params.append(_paramAux)

        return _params

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('Controls Box')
        self.ui_controls_box_widget = QtGui.QDockWidget(ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        #

        self.slider = []
        self.label = []

        self.slider.append(QtGui.QSlider(QtCore.Qt.Horizontal))
        self.slider[0].setRange(0, 100)
        self.slider[0].setValue(0)
        self.slider.append(QtGui.QSlider(QtCore.Qt.Horizontal))
        self.slider[1].setRange(0, 20000)
        self.slider[1].setValue(6500)
        self.slider.append(QtGui.QSlider(QtCore.Qt.Horizontal))
        self.slider[2].setRange(0, 100)
        self.slider[2].setValue(5)
        self.slider.append(QtGui.QSlider(QtCore.Qt.Horizontal))
        self.slider[3].setRange(0, 100)
        self.slider[3].setValue(50)

        self.label.append(QtGui.QLabel())
        self.label[0].setText("Intravenous Glucose: " + str(float(self.slider[0].value()/100)) + " mmol/kg/min")
        self.label.append(QtGui.QLabel())
        self.label[1].setText("Exogenous insulin appearance rate: " + str(float(self.slider[1].value()/100)) + " mU/min")
        self.label.append(QtGui.QLabel())
        self.label[2].setText("Enteral carbohydrate feedrate: " + str(float(self.slider[2].value()/100)) + " mmol/kg min")
        self.label.append(QtGui.QLabel())
        self.label[3].setText("Insulin sensitiviy: " + str(float(self.slider[3].value()/100)) + " {1 normal}")


        ## Create two ParameterTree widgets, both accessing the same data
        self.parameter_tree = ParameterTree()
        __parTr = Parameter.create(name='params', type='group', children=self.createParams())
        self.parameter_tree.setParameters(__parTr, showTop=False)

        #

        self.btnPlayStop = QtGui.QPushButton('Play')
        self.btnNext = QtGui.QPushButton('Next')
        self.btnReset = QtGui.QPushButton('Reset')
        #
        self.house_layout = QtGui.QVBoxLayout()
        self.house_layout.addWidget(self.label[0])
        self.house_layout.addWidget(self.slider[0])
        self.house_layout.addWidget(self.label[1])
        self.house_layout.addWidget(self.slider[1])
        self.house_layout.addWidget(self.label[2])
        self.house_layout.addWidget(self.slider[2])
        self.house_layout.addWidget(self.label[3])
        self.house_layout.addWidget(self.slider[3])

        self.house_layout.addWidget(self.parameter_tree)

        self.house_layout.addWidget(self.btnPlayStop)
        self.house_layout.addWidget(self.btnNext)
        self.house_layout.addWidget(self.btnReset)
        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        #
        self.ui_controls_box_widget.setWidget(self.house_widget)

