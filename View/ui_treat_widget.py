__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor
import types

class Ui_TreatDockWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_TreatDockWidget, self).__init__()

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget("Treatment", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.parent = ControlsBox
        #
        self.house_layout = QtGui.QVBoxLayout()
        self.colors = ['#4F347A', '#B35C41', '#B3A641', '#2E7D55', '#B345A1', '#B345A1', '#B345A1']
        self.pen_size = [3, 3, 3, 3, 3, 3]

        self.init_eq_sliders()
        self.house_layout.addSpacing(10)
        self.init_time_label()

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.addSpacing(10)


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


    def init_eq_sliders(self):
        self.slider = []
        self.label = []
        _i = 0

        self.definite_slider_change_control()

        sliderF = ""
        for userDef in self.parent.controller.model._u:
            if userDef.isSlider:
                vbox = QtGui.QVBoxLayout()
                # vbox.addStretch(1)

                s_aux = QtGui.QSlider(QtCore.Qt.Horizontal)
                s_aux.setRange(float(userDef.sliderMin) * 100, float(userDef.sliderMax) * 100)
                s_aux.setValue(float(userDef.defaultValue) * 100)
                s_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

                l_aux = QtGui.QLabel()
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

                b_aux = QtGui.QPushButton("...")
                b_aux.setMaximumWidth(20)
                b_aux.clicked.connect(eval("self.eqSliderChangeValue_" + str(_i)))

                self.slider.append(s_aux)
                self.label.append(l_aux)
                vbox.addWidget(l_aux)
                vbox.addWidget(b_aux)
                vbox.addWidget(s_aux)
                self.house_layout.addLayout(vbox)
                vbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
                self.house_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
                self.house_layout.addSpacing(20)
                _i += 1


    def get_sliders_vals(self):
        out = []
        for sl in self.slider:
            out.append(sl.value()/100)
        return out


    def definite_slider_change_control(self):
        _i = 0
        for eq in self.parent.controller.model._u:
            # TODO: pasar a DefiniteFunciton la creacion del codigo
            controlFunc = "def eqSliderChangeValue_" + str(_i) + "(self):\n\t" \
                "print(" + str(_i) + ")\n\t" \
                "self.show_slider_att_changing(" + str(_i) + ")\n\t"

            _c_f_aux = "eqSliderChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

    def show_slider_att_changing(self, slider_id):

        color = QColorDialog.getColor()

        if color.isValid():
            self.colors[slider_id] = color.name()
            self.parent.controller.handler_change_graph_color(slider_id, "TREAT", self.colors[slider_id])