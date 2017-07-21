__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt5 import QtCore, QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree
import types

# TODO: No importar Plot2, pasar por parametro
import Plot2 as plt2

class Ui_GeneralControlsWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_GeneralControlsWidget, self).__init__()
        self.colors = ['#B38D42', '#4268B3', '#B345A1', '#42B354', '#B345A1', '#B345A1', '#B345A1']
        self.pen_size = [3, 3, 3, 3, 3, 3]

    def createParamsRest(self):
        # Tree params
        _params = []
        _i = 0
        _listChildAuxEq = []
        for const in plt2._e:
            _childAuxEq = []
            # if const.simulate:
            _childAuxEq = {'name': const.description, 'type': 'group', 'expanded': const.simulate, 'children': [
                    {'name': 'Formula', 'type': 'str',
                        'value': const.name + ' = ' + const.equation,
                        'readonly': True},
                    {'name': 'Simulated', 'type': 'str', 'value': 'Yes', 'readonly': True},
                    {'name': 'Color', 'type': 'color', 'value': self.colors[_i], 'readonly': False},
                    #TODO: agregar mas atributos
                    # {'name': 'Line width', 'type': 'int', 'value': self.pen_size[_i], 'readonly': not const.simulate},
                ]}
            # else:
            #     _childAuxEq = {'name': const.description, 'type': 'group' , 'expanded': const.simulate, 'children': [
            #             {'name': 'Formula', 'type': 'str',
            #                 'value': const.name + ' = ' + const.equation,
            #                 'readonly': True},
            #             {'name': 'Simulated', 'type': 'str', 'value': 'No', 'readonly': True},
            #         ]}
            _listChildAuxEq.append(_childAuxEq)
            _i += 1
            # print(const)
        _paramAux = {'name': 'Equations', 'type': 'group', 'children': _listChildAuxEq, 'expanded': True}
        _params.append(_paramAux)

        _listChildAuxFunc = []
        for const in plt2._f:
            _childAuxFunc = {'name': const.name, 'type': 'str', 'value': const.function, 'siPrefix': False,
                             'readonly': True}
            _listChildAuxFunc.append(_childAuxFunc)
            # print(const)
        _paramAux = {'name': 'Functions', 'type': 'group', 'children': _listChildAuxFunc, 'expanded': False}
        _params.append(_paramAux)

        _listChildAuxConst = []
        for const in plt2._c:
            nomC = const.value1
            # nomC = const.value1 + ' ' + const.operator
            _childAuxConst = {'name': nomC, 'type': 'str', 'value': const.value2, 'readonly': True}
            _listChildAuxConst.append(_childAuxConst)
        _paramAuxConst = {'name': 'Constants', 'type': 'group', 'children': _listChildAuxConst, 'expanded': False}
        _params.append(_paramAuxConst)

        return _params

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget("Model Parameters", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        # self.ui_controls_box_widget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.parent = ControlsBox
        #
        self.house_layout = QtGui.QVBoxLayout()


        ## Create ParameterTree for the rest of the parameters
        self.parameter_tree = ParameterTree()
        self.parTr = Parameter.create(name='params', type='group', children=self.createParamsRest(), showHeader=False)
        self.parameter_tree.setParameters(self.parTr, showTop=False)
        #


        self.eqLblList = []
        self.eqCtrlList = []
        self.eqBtnList = []

        self.init_eq_change_control()

        self.house_layout.addWidget(self.parameter_tree)

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

                #
        self.ui_controls_box_widget.setWidget(self.house_widget)

    def init_eq_change_control(self):
        _i = 0
        for eq in plt2._e:
            hbox = QtGui.QHBoxLayout()
            hbox.addStretch(1)
            self.eqLblList.append(QtGui.QLabel(eq.description + " (" + eq.name + "):"))
            self.eqCtrlList.append(QtGui.QDoubleSpinBox())
            self.eqBtnList.append(QtGui.QPushButton("Cambiar"))
            myFont = QtGui.QFont()
            myFont.setBold(True)
            self.eqCtrlList[_i].setFont(myFont)

            hbox.addWidget(self.eqLblList[_i])
            hbox.addWidget(self.eqCtrlList[_i])
            hbox.addWidget(self.eqBtnList[_i])
            hbox.setAlignment(QtCore.Qt.AlignLeft)

            controlFunc = "def eqCtrlChangeValue_" + str(_i) + "(self):\n\t" \
                                        "print(self.eqCtrlList[" + str(_i) + "].value())\n\t"\
                                        "self.parent.changeActualPoint(" + str(_i) + ", self.eqCtrlList[" + str(_i) + "].value())\n\t" \
                                        "plt2.recalculate()\n"

            _c_f_aux = "eqCtrlChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = types.MethodType(" + _c_f_aux + ", self)")

            self.eqBtnList[_i].clicked.connect(eval("self.eqCtrlChangeValue_" + str(_i)))

            self.house_layout.addLayout(hbox)

            _i += 1
