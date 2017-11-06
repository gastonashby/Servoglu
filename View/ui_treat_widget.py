__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QColorDialog, QFrame
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
        self.color_buttons = []
        self.tr_checks = []
        self.pen_size = [3, 3, 3, 3, 3, 3]

        self.init_eq_sliders()
        self.house_layout.addSpacing(10)
        # self.init_time_label()

        self.house_widget = QtGui.QWidget()
        self.house_widget.setLayout(self.house_layout)

        self.ui_controls_box_widget.setWidget(self.house_widget)
        self.house_layout.addSpacing(10)


    def init_eq_sliders(self):
        self.slider = []
        self.label = []
        _i = 0

        self.definite_slider_change_color()
        self.definite_slider_change_visible()

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
                l_aux.setToolTip(userDef.detailedDescription)

                hbox = QtGui.QHBoxLayout()

                b_aux = QtGui.QPushButton("")
                b_aux.setMaximumWidth(15)
                b_aux.setMaximumHeight(15)
                b_aux.setStyleSheet('QPushButton {background-color:' + self.colors[_i] + ';}')
                b_aux.clicked.connect(eval("self.eqSliderChangeValue_" + str(_i)))
                self.color_buttons.append(b_aux)

                ch_aux = QtGui.QCheckBox("Visible")
                ch_aux.setChecked(1)
                ch_aux.stateChanged.connect(eval("self.eqSliderChangeVisibleValue_" + str(_i)))
                self.tr_checks.append(ch_aux)

                h_box_aux = QtGui.QHBoxLayout()
                h_box_aux.addWidget(b_aux)
                h_box_aux.addWidget(ch_aux)

                self.slider.append(s_aux)
                self.label.append(l_aux)
                vbox.addWidget(l_aux)
                vbox.addLayout(h_box_aux)
                vbox.addWidget(s_aux)

                self.house_layout.addLayout(vbox)
                vbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
                self.house_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
                self.house_layout.addSpacing(5)
                _i += 1


    def get_sliders_vals(self):
        out = []
        for sl in self.slider:
            out.append(sl.value()/100)
        return out


    def definite_slider_change_color(self):
        _i = 0
        for eq in self.parent.controller.model._u:
            # TODO: pasar a DefiniteFunciton la creacion del codigo
            controlFunc = "def eqSliderChangeValue_" + str(_i) + "(self, int):\n\t" \
                "print(" + str(_i) + ")\n\t" \
                "self.show_slider_att_changing(" + str(_i) + ", 'COLOR')\n\t"

            _c_f_aux = "eqSliderChangeValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

    def definite_slider_change_visible(self):
        _i = 0
        for eq in self.parent.controller.model._u:
            # TODO: pasar a DefiniteFunciton la creacion del codigo
            controlFunc = "def eqSliderChangeVisibleValue_" + str(_i) + "(self):\n\t" \
                "print(" + str(_i) + ")\n\t" \
                "self.show_slider_att_changing(" + str(_i) + ", 'VISIBLE')\n\t"

            _c_f_aux = "eqSliderChangeVisibleValue_" + str(_i)
            exec(controlFunc)
            exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

    def show_slider_att_changing(self, slider_id, type):

        if type == 'COLOR':
            color = QColorDialog.getColor()

            if color.isValid():
                self.colors[slider_id] = color.name()
                self.parent.controller.handler_change_graph_color(slider_id, "TREAT", self.colors[slider_id])
                self.color_buttons[slider_id].setStyleSheet('QPushButton {background-color:' + self.colors[slider_id] + ';}')
        elif type == 'VISIBLE':
            print(self.tr_checks[slider_id].isChecked(), slider_id)

            self.parent.simulated_tr[slider_id] = self.tr_checks[slider_id].isChecked()

            if self.tr_checks[slider_id].isChecked():
                self.parent.all_treat_curves[slider_id] = self.parent.create_treat_curve(slider_id, self.parent.controller.model._u[slider_id].name)
                self.parent.all_treat_curves[slider_id].setData(self.parent.xDataGraf[:self.parent.indexGr + 1],
                                                   self.parent.treatment[slider_id])
            else:
                self.parent.all_treat_curves[slider_id].clear()