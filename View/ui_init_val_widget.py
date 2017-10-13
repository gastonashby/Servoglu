__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree

class Ui_InitialValuesDockWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_InitialValuesDockWidget, self).__init__()
        self.ui_controls_box_widget = []
        self.parent = []
        self.house_layout = []
        self.parameter_tree1 = []

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('Controls Box')
        self.ui_controls_box_widget = QtGui.QDockWidget("Initial Values", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.parent = ControlsBox

        self.house_layout = QtGui.QVBoxLayout()

        ## Create ParameterTree for user def parameters
        self.parameter_tree1 = ParameterTree()
        __parTr1 = Parameter.create(name='params1', type='group', children=self.createParamsUserDef())
        self.parameter_tree1.setParameters(__parTr1, showTop=False)

        __parTr1.sigTreeStateChanged.connect(self.handler_change_model_parameter)

        self.house_layout.addWidget(self.parameter_tree1)

        ## Create ParameterTree for the rest of the parameters
        # self.parameter_tree = ParameterTree()
        # self.parTr = Parameter.create(name='params', type='group', children=self.parent.controller.createParamsRest()
        #                               , showHeader=False)
        # self.parameter_tree.setParameters(self.parTr, showTop=False)
        # #
        # self.house_layout.addSpacing(10)
        # self.house_layout.addWidget(self.parameter_tree)

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.addSpacing(10)

    def handler_change_model_parameter(self, param, changes):
            print("tree changes:")
            for param, change, data in changes:
                # path = __parTr1.childPath(param)
                # if path is not None:
                #     childName = '.'.join(path)
                # else:
                childName = param.name()
                print('  parameter: %s' % childName)
                print('  change:    %s' % change)
                print('  data:      %s' % str(data))
                print('  ----------')
                print(eval("self.parent.controller.model." + childName))
                print("self.parent.controller.model." + childName + " = " + data + "")
                exec("self.parent.controller.model." + childName + " = " + data + "")
                print(eval("self.parent.controller.model." + childName))
                self.parent.controller.model.recalculate(self.parent.step)

    def createParamsUserDef(self):
        # Tree params
        _listChildUsrDef = []
        _params = []
        for userDef in self.parent.controller.model._u:
            # nomC = const.value1 + ' ' + const.operator
            if not userDef.isSlider:
                _childAuxUsrDef = {'name': userDef.name, 'value': userDef.defaultValue, 'type': 'str',
                                   'readonly': False,
                                   'title': userDef.description + " (" + userDef.unit + ") "}#, 'suffix': userDef.unit, 'siPrefix': True}
                _listChildUsrDef.append(_childAuxUsrDef)
        _paramAuxUsrDef = {'name': 'User Defined', 'type': 'group', 'children': _listChildUsrDef, 'expanded': True}
        _params.append(_paramAuxUsrDef)

        return _params