__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree
from Controller.main_controller import *

class Ui_PropertiesDockWidget(QtCore.QObject):

    def __init__(self):
        self.indexGr = 0
        self.colors = ['#B38C41', '#8E3469', '#85A73D', '#334977', '#B345A1', '#B345A1', '#B345A1']
        super(Ui_PropertiesDockWidget, self).__init__()

    def setupUi(self, ControlsBox):
        self.parent = ControlsBox
        ControlsBox.setObjectName('Controls Box')
        self.languageHash = self.parent.controller.languageSupport.languageHash
        self.ui_controls_box_widget = QtGui.QDockWidget(self.languageHash.__getitem__("lbl.ModelProperties"), ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)


        self.house_layout = QtGui.QVBoxLayout()

        ## Create ParameterTree for the rest of the parameters
        self.parameter_tree = ParameterTree()
        self.parTr = Parameter.create(name='params', type='group', children=self.createParamsRest()
                                      , showHeader=False)
        self.parameter_tree.setParameters(self.parTr, showTop=False)
        #
        self.house_layout.addWidget(self.parameter_tree)

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.house_layout.addSpacing(10)

    def createParamsRest(self):
        # Tree params
        _params = []
        _i = 0
        _listChildAuxEq = []
        for const in self.parent.controller.model._e:
            _childAuxEq = []
            # if const.simulate:
            _childAuxEq = {'name': const.description + ' (' + "d" +const.name + "/dt" + ')', 'type': 'group', 'expanded': True, 'children': [
                    {'name': "d" + const.name + "/dt" + ' =', 'type': 'str',
                        'value': const.equation,
                        'readonly': True},
                    {'name': 'Visible', 'type': 'bool', 'value': const.simulate, 'readonly': False},
                    {'name': 'Color', 'type': 'color', 'value': self.colors[_i], 'readonly': False},
                    #TODO: agregar mas atributos
                    # {'name': 'Line width', 'type': 'int', 'value': self.pen_size[_i], 'readonly': not const.simulate},
                ]}
            _listChildAuxEq.append(_childAuxEq)
            _i += 1
            # print(const)self.languageHash.__getitem__("lbl.ModelProperties")
        _paramAux = {'name': self.languageHash.__getitem__("lbl.DifferentialEquations"), 'type': 'group', 'children': _listChildAuxEq, 'expanded': True}
        _params.append(_paramAux)

        _listChildAuxFunc = []
        for const in self.parent.controller.model._f:
            _childAuxFunc = {'name': const.name, 'type': 'str', 'value': const.function, 'siPrefix': False,
                             'readonly': True}
            _listChildAuxFunc.append(_childAuxFunc)
            # print(const)
        _paramAux = {'name': self.languageHash.__getitem__("lbl.Functions"), 'type': 'group', 'children': _listChildAuxFunc, 'expanded': True}
        _params.append(_paramAux)

        _listChildAuxConst = []
        for const in self.parent.controller.model._c:
            nomC = const.value1
            # nomC = const.value1 + ' ' + const.operator
            _childAuxConst = {'name': nomC, 'type': 'str', 'value': const.value2, 'readonly': True}
            _listChildAuxConst.append(_childAuxConst)
        _paramAuxConst = {'name': self.languageHash.__getitem__("lbl.Constants"), 'type': 'group', 'children': _listChildAuxConst, 'expanded': True}
        _params.append(_paramAuxConst)

        return _params