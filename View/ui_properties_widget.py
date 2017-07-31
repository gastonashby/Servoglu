__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree

class Ui_PropertiesDockWidget(QtCore.QObject):

    def __init__(self):
        self.indexGr = 0
        self.colors = ['#B38D42', '#4268B3', '#B345A1', '#42B354', '#B345A1', '#B345A1', '#B345A1']
        self.pen_size = [3, 3, 3, 3, 3, 3]
        super(Ui_PropertiesDockWidget, self).__init__()

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('Controls Box')
        self.ui_controls_box_widget = QtGui.QDockWidget("Model Controlls", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.parent = ControlsBox

        self.house_layout = QtGui.QVBoxLayout()

        ## Create ParameterTree for user def parameters
        self.parameter_tree1 = ParameterTree()
        __parTr1 = Parameter.create(name='params1', type='group', children=self.parent.controller.createParamsUserDef())
        self.parameter_tree1.setParameters(__parTr1, showTop=False)

        __parTr1.sigTreeStateChanged.connect(self.parent.controller.handler_change_model_parameter)

        self.house_layout.addWidget(self.parameter_tree1)

        ## Create ParameterTree for the rest of the parameters
        self.parameter_tree = ParameterTree()
        self.parTr = Parameter.create(name='params', type='group', children=self.parent.controller.createParamsRest()
                                      , showHeader=False)
        self.parameter_tree.setParameters(self.parTr, showTop=False)
        #
        self.house_layout.addSpacing(10)
        self.house_layout.addWidget(self.parameter_tree)

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)
        self.ui_controls_box_widget.setWidget(self.house_widget)
