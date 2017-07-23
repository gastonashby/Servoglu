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

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget("Model Parameters", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        # self.ui_controls_box_widget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.parent = ControlsBox
        #
        self.house_layout = QtGui.QVBoxLayout()

        self.eqLblList = []
        self.eqCtrlList = []
        self.eqBtnList = []
        self.init_eq_change_control()
        self.house_layout.addSpacing(10)
        self.init_eq_sliders()
        self.house_layout.addSpacing(10)
        self.init_time_label()

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

                #
        self.ui_controls_box_widget.setWidget(self.house_widget)

    def init_time_label(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        label = QtGui.QLabel("Simulation time (D:HH:MM:SS): ")
        self.timeLbl = QtGui.QLabel("0:00:00:00")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        myFont.setPointSize(11)
        self.timeLbl.setFont(myFont)

        hbox.addWidget(label)
        hbox.addWidget(self.timeLbl)

        self.house_layout.addLayout(hbox)


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
            self.eqCtrlList[_i].setDecimals(self.parent.round)
            hbox.addWidget(self.eqLblList[_i])
            hbox.addWidget(self.eqCtrlList[_i])
            hbox.addWidget(self.eqBtnList[_i])

            controlFunc = "def eqCtrlChangeValue_" + str(_i) + "(self):\n\t" \
                                        "#print(self.eqCtrlList[" + str(_i) + "].value())\n\t"\
                                        "self.parent.changeActualPoint(" + str(_i) + ", self.eqCtrlList[" + str(_i) + "].value())\n\t"

            _c_f_aux = "eqCtrlChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = types.MethodType(" + _c_f_aux + ", self)")

            self.eqBtnList[_i].clicked.connect(eval("self.eqCtrlChangeValue_" + str(_i)))

            self.house_layout.addLayout(hbox)
            self.house_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

            _i += 1

    def init_eq_sliders(self):
        self.slider = []
        self.label = []

        _i = 1
        sliderF = ""
        for userDef in plt2._u:
            if userDef.isSlider:

                s_aux = QtGui.QSlider(QtCore.Qt.Horizontal)
                s_aux.setRange(float(userDef.sliderMin) * 100, float(userDef.sliderMax) * 100)
                s_aux.setValue(float(userDef.defaultValue) * 100)
                s_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

                # sliderF = """def sliderValueChanged""" + str(_i) + """(self, value):\n\tprint(value/100)\n\n"""

                l_aux = QtGui.QLabel()
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

                self.slider.append(s_aux)
                self.label.append(l_aux)
                self.house_layout.addWidget(l_aux)
                self.house_layout.addWidget(s_aux)
                _i += 1

