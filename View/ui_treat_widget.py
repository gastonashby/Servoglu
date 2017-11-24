__author__ = 'Gastón Ashby & Ignacio Ferrer'
__version__ = '0.0.1'

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QColorDialog, QFrame
from PyQt5.QtGui import QColor
import types
import random

class Ui_TreatDockWidget(QtCore.QObject):

    def __init__(self):
        super(Ui_TreatDockWidget, self).__init__()
        self.slider = []
        self.label = []
        self.treat_vals = []
        self.r = lambda: random.randint(0,255)

    def get_new_color(self):
        return '#%02X%02X%02X' % (self.r(), self.r(), self.r())

    def setupUi(self, ControlsBox):
        ControlsBox.setObjectName('General Controls')
        self.ui_controls_box_widget = QtGui.QDockWidget("Treatment", ControlsBox)
        self.ui_controls_box_widget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.parent = ControlsBox
        #
        self.house_layout = QtGui.QVBoxLayout()
        self.colors = []
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

        _i = 0

        self.definite_slider_change_color()
        self.definite_slider_change_visible()

        sliderF = ""
        for userDef in self.parent.controller.model._u:
            if userDef.isSlider:
                if len(userDef.color) > 0:
                    self.colors.append(userDef.color)
                else:
                    self.colors.append(self.get_new_color())

                vbox = QtGui.QVBoxLayout()
                # vbox.addStretch(1)

                s_aux = QtGui.QSlider(QtCore.Qt.Horizontal)
                s_aux.setRange(float(userDef.sliderMin) * 100, float(userDef.sliderMax) * 100)
                s_aux.setValue(float(userDef.defaultValue) * 100)
                s_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                s_aux.setToolTip(userDef.detailedDescription)

                l_aux = QtGui.QLabel()
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                l_aux.setToolTip(userDef.detailedDescription)

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
                self.treat_vals.append(s_aux.value()/100)
                self.label.append(l_aux)
                vbox.addWidget(l_aux)
                vbox.addLayout(h_box_aux)
                vbox.addWidget(s_aux)

                self.house_layout.addLayout(vbox)
                vbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
                self.house_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
                self.house_layout.addSpacing(5)
                _i += 1

        for userDef in self.parent.controller.model._u:
            if userDef.graphAsTreatment and not userDef.isSlider:
                if len(userDef.color) > 0:
                    self.colors.append(userDef.color)
                else:
                    self.colors.append(self.get_new_color())

                l_aux = QtGui.QLabel()
                l_aux.setText(userDef.description + ' ' + str(float(s_aux.value() / 100)) + ' ' + userDef.unit)
                l_aux.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                l_aux.setToolTip(userDef.detailedDescription)


                self.treat_vals.append(float(userDef.defaultValue))


    def get_sliders_vals(self):
        return self.treat_vals


    def definite_slider_change_color(self):
        _i = 0
        for eq in self.parent.controller.model._u:
            controlFunc, _c_f_aux = self.parent.controller.model.code.definite_slider_change_color(_i)

            exec(controlFunc)
            exec("self." + _c_f_aux + " = self.parent.types.MethodType(" + _c_f_aux + ", self)")

            _i += 1

    def definite_slider_change_visible(self):
        _i = 0
        for eq in self.parent.controller.model._u:
            controlFunc, _c_f_aux = self.parent.controller.model.code.definite_slider_change_visible(_i)

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