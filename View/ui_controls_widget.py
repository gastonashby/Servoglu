__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
import types

class Ui_ControlsDockWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_ControlsDockWidget, self).__init__()

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget("Actual values", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.parent = ControlsBox
        #
        self.house_layout = QtGui.QVBoxLayout()

        self.eqLblList = []
        self.eqCtrlList = []
        self.eqBtnList = []
        self.init_eq_change_control()

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.addSpacing(10)

    def init_eq_change_control(self):
        _i = 0
        self.definite_equation_change_control()
        for eq in self.parent.controller.model._e:
            hbox = QtGui.QHBoxLayout()
            # hbox.addStretch(1)
            self.eqLblList.append(QtGui.QLabel(eq.description + " (" + eq.name + "):"))
            self.eqLblList[_i].setToolTip(eq.detailedDescription)
            self.eqCtrlList.append(QtGui.QDoubleSpinBox())
            self.eqBtnList.append(QtGui.QPushButton(">"))
            myFont = QtGui.QFont()
            myFont.setBold(True)
            self.eqBtnList[_i].setMaximumWidth(20)
            self.eqCtrlList[_i].setFont(myFont)
            self.eqCtrlList[_i].setDecimals(self.parent.round)
            self.eqCtrlList[_i].setSuffix(" " + eq.unit)
            self.eqCtrlList[_i].setMaximum(10000000)
            hbox.addWidget(self.eqLblList[_i])
            hbox.addWidget(self.eqCtrlList[_i])
            hbox.addWidget(self.eqBtnList[_i])

            self.eqBtnList[_i].clicked.connect(eval("self.eqCtrlChangeValue_" + str(_i)))

            self.house_layout.addLayout(hbox)
            hbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
            self.house_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)

            _i += 1

    def definite_equation_change_control(self):
        _i = 0
        for eq in self.parent.controller.model._e:
            # TODO: pasar a DefiniteFunciton la creacion del codigo
            controlFunc = "def eqCtrlChangeValue_" + str(_i) + "(self):\n\t" \
                "#print(self.eqCtrlList[" + str(_i) + "].value())\n\t" \
                "self.parent.controller.handler_change_simulated_value(" + str(_i) + \
                ", self.parent.ui.dck_model_param_controls.eqCtrlList[" + str(_i) + "].value())\n\t"

            _c_f_aux = "eqCtrlChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

