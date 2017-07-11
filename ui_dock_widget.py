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

    def __init__(self):
        self.indexGr = 0
        super(Ui_ControlsBoxDockWidget, self).__init__()

    def createParamsUserDef(self):
        # Tree params
        _listChildUsrDef = []
        _params = []
        _init_timmer = 200
        for userDef in plt2._u:
            # nomC = const.value1 + ' ' + const.operator
            if not userDef.isSlider:
                _childAuxUsrDef = {'name': userDef.name, 'value': userDef.defaultValue, 'type': 'str',
                                   'readonly': False,
                                   'title': userDef.description + " (" + userDef.unit + ") "}#, 'suffix': userDef.unit, 'siPrefix': True}
                _listChildUsrDef.append(_childAuxUsrDef)
        _paramAuxUsrDef = {'name': 'User Defined', 'type': 'group', 'children': _listChildUsrDef, 'expanded': True}
        _params.append(_paramAuxUsrDef)

        return _params

    def createParamsRest(self):
        # Tree params
        _listChildUsrDef = []
        _params = []
        #_init_timmer = 200

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

        self.house_layout = QtGui.QVBoxLayout()

        ## Create ParameterTree for user def parameters
        self.parameter_tree1 = ParameterTree()
        __parTr1 = Parameter.create(name='params1', type='group', children=self.createParamsUserDef())
        self.parameter_tree1.setParameters(__parTr1, showTop=False)
        self.house_layout.addWidget(self.parameter_tree1)

        def change(param, changes):
            print("tree changes:")
            for param, change, data in changes:
                path = __parTr1.childPath(param)
                if path is not None:
                    childName = '.'.join(path)
                else:
                    childName = param.name()
                print('  parameter: %s' % childName)
                print('  change:    %s' % change)
                print('  data:      %s' % str(data))
                print('  ----------')
                print(eval("plt2." + childName.split(".")[1]))
                print("plt2." + childName.split(".")[1] + " = " + data + "")
                exec("plt2." + childName.split(".")[1] + " = " + data + "")
                print(eval("plt2." + childName.split(".")[1]))
                plt2.recalculate(self.indexGr)

        __parTr1.sigTreeStateChanged.connect(change)

        self.slider = []
        self.label = []

        i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:
                s_aux = QtGui.QSlider(QtCore.Qt.Horizontal)
                s_aux.setRange(float(userDef.sliderMin) * 100, float(userDef.sliderMax) * 100)
                s_aux.setValue(float(userDef.defaultValue) * 100)

                # sliderF = """def sliderValueChanged""" + str(i) + """(self, value):\n\tprint(value/100)\n\n"""

                l_aux = QtGui.QLabel()
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)

                self.slider.append(s_aux)
                self.label.append(l_aux)
                self.house_layout.addWidget(l_aux)
                self.house_layout.addWidget(s_aux)
                i += 1

        ## Create ParameterTree for the rest of the parameters
        self.parameter_tree = ParameterTree()
        __parTr = Parameter.create(name='params', type='group', children=self.createParamsRest())
        self.parameter_tree.setParameters(__parTr, showTop=False)

        #

        self.btnPlayStop = QtGui.QPushButton('Play')
        self.btnNext = QtGui.QPushButton('Next')
        self.btnReset = QtGui.QPushButton('Reset')
        #

        self.house_layout.addWidget(self.parameter_tree)

        self.house_layout.addWidget(self.btnPlayStop)
        self.house_layout.addWidget(self.btnNext)
        self.house_layout.addWidget(self.btnReset)
        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        #
        self.ui_controls_box_widget.setWidget(self.house_widget)
